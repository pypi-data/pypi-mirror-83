# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Code to simulate systems in various statistical ensembles.

  This file contains a number of different methods that can be used to
  simulate systems in a variety of ensembles.

  In general, simulation code follows the same overall structure as optimizers
  in JAX. Simulations are tuples of two functions:
    init_fn: function that initializes the  state of a system. Should take
      positions as an ndarray of shape [n, output_dimension]. Returns a state
      which will be a namedtuple.
    apply_fn: function that takes a state and produces a new state after one
      step of optimization.

  One question that we need to think about is whether the simulations should
  also return a function that computes the invariant for that ensemble. This
  can be used for testing purposes, but is not often used otherwise.
"""

from collections import namedtuple

from typing import Callable, TypeVar, Union, Tuple

from jax import ops
from jax import random
import jax.numpy as np

from jax_md import quantity, interpolate, util, space, dataclasses

static_cast = util.static_cast


# Types


Array = util.Array
f32 = util.f32
f64 = util.f64

ShiftFn = space.ShiftFn

T = TypeVar('T')
InitFn = Callable[..., T]
ApplyFn = Callable[[T], T]
Simulator = Tuple[InitFn, ApplyFn]

Schedule = Union[Callable[..., float], float]


# Constant Energy Simulations


@dataclasses.dataclass
class NVEState:
  """A struct containing the state of an NVE simulation.

  This tuple stores the state of a simulation that samples from the
  microcanonical ensemble in which the (N)umber of particles, the (V)olume, and
  the (E)nergy of the system are held fixed.

  Attributes:
    position: An ndarray of shape [n, spatial_dimension] storing the position
      of particles.
    velocity: An ndarray of shape [n, spatial_dimension] storing the velocity
      of particles.
    acceleration: An ndarray of shape [n, spatial_dimension] storing the
      acceleration of particles from the previous step.
    mass: A float or an ndarray of shape [n] containing the masses of the
      particles.
  """
  position: Array
  velocity: Array
  acceleration: Array
  mass: Array


# pylint: disable=invalid-name
def nve(energy_or_force: Callable[..., Array],
        shift_fn: ShiftFn,
        dt: float) -> Simulator:
  """Simulates a system in the NVE ensemble.

  Samples from the microcanonical ensemble in which the number of particles (N),
  the system volume (V), and the energy (E) are held constant. We use a standard
  velocity verlet integration scheme.

  Args:
    energy_or_force: A function that produces either an energy or a force from
      a set of particle positions specified as an ndarray of shape
      [n, spatial_dimension].
    shift_fn: A function that displaces positions, R, by an amount dR. Both R
      and dR should be ndarrays of shape [n, spatial_dimension].
    dt: Floating point number specifying the timescale (step size) of the
      simulation.
    quant: Either a quantity.Energy or a quantity.Force specifying whether
      energy_or_force is an energy or force respectively.
  Returns:
    See above.
  """
  force = quantity.canonicalize_force(energy_or_force)

  dt, = static_cast(dt)
  dt_2, = static_cast(0.5 * dt ** 2)
  def init_fun(key: Array,
               R: Array,
               velocity_scale: float=f32(1.0),
               mass=f32(1.0),
               **kwargs) -> NVEState:
    V = np.sqrt(velocity_scale) * random.normal(key, R.shape, dtype=R.dtype)
    mass = quantity.canonicalize_mass(mass)
    return NVEState(R, V, force(R, **kwargs) / mass, mass)  # pytype: disable=wrong-arg-count
  def apply_fun(state: NVEState, t: float=f32(0), **kwargs) -> NVEState:
    R, V, A, mass = dataclasses.astuple(state)
    R = shift_fn(R, V * dt + A * dt_2, t=t, **kwargs)
    A_prime = force(R, t=t, **kwargs) / mass
    V = V + f32(0.5) * (A + A_prime) * dt
    return NVEState(R, V, A_prime, mass)  # pytype: disable=wrong-arg-count
  return init_fun, apply_fun


# Constant Temperature Simulations


@dataclasses.dataclass
class NVTNoseHooverState:
  """A tuple containing state information for the Nose-Hoover chain thermostat.

  Attributes:
    position: The current position of particles. An ndarray of floats
      with shape [n, spatial_dimension].
    velocity: The velocity of particles. An ndarray of floats
      with shape [n, spatial_dimension].
    mass: The mass of the particles. Can either be a float or an ndarray
      of floats with shape [n].
    kinetic_energy: A float that stores the current kinetic energy of the
      system.
    xi: An ndarray of shape [chain_length] that stores the "positional" degrees
      of freedom for the Nose-Hoover thermostat.
    v_xi: An ndarray of shape [chain_length] that stores the "velocity" degrees
      of freedom for the Nose-Hoover thermostat.
    Q: An ndarray of shape [chain_length] that stores the mass of the
      Nose-Hoover chain.
  """
  position: Array
  velocity: Array
  mass: Array
  kinetic_energy: Array
  xi: Array
  v_xi: Array
  Q: Array


def nvt_nose_hoover(energy_or_force: Callable[..., Array],
                    shift_fn: ShiftFn,
                    dt: float,
                    T_schedule: Schedule,
                    chain_length: int=5,
                    tau: float=100.0) -> Simulator:
  """Simulation in the NVT ensemble using a Nose Hoover Chain thermostat.

  Samples from the canonical ensemble in which the number of particles (N),
  the system volume (V), and the temperature (T) are held constant. We use a
  Nose Hoover Chain thermostat described in [1, 2, 3]. We employ a similar
  notation to [2] and the interested reader might want to look at that paper as
  a reference.

  Currently, the implementation only does a single timestep per Nose-Hoover
  step. At some point we should support the multi-step case.

  Args:
    energy_or_force: A function that produces either an energy or a force from
      a set of particle positions specified as an ndarray of shape
      [n, spatial_dimension].
    shift_fn: A function that displaces positions, R, by an amount dR. Both R
      and dR should be ndarrays of shape [n, spatial_dimension].
    dt: Floating point number specifying the timescale (step size) of the
      simulation.
    T_schedule: Either a floating point number specifying a constant temperature
      or a function specifying temperature as a function of time.
    quant: Either a quantity.Energy or a quantity.Force specifying whether
      energy_or_force is an energy or force respectively.
    chain_length: An integer specifying the length of the Nose-Hoover chain.
    tau: A floating point timescale over which temperature equilibration occurs.
      Measured in units of dt. The performance of the Nose-Hoover chain
      thermostat can be quite sensitive to this choice.
  Returns:
    See above.

  [1] Martyna, Glenn J., Michael L. Klein, and Mark Tuckerman.
      "Nose-Hoover chains: The canonical ensemble via continuous dynamics."
      The Journal of chemical physics 97, no. 4 (1992): 2635-2643.
  [2] Martyna, Glenn, Mark Tuckerman, Douglas J. Tobias, and Michael L. Klein.
      "Explicit reversible integrators for extended systems dynamics."
      Molecular Physics 87. (1998) 1117-1157.
  [3] Tuckerman, Mark E., Jose Alejandre, Roberto Lopez-Rendon,
      Andrea L. Jochim, and Glenn J. Martyna.
      "A Liouville-operator derived measure-preserving integrator for molecular
      dynamics simulations in the isothermal-isobaric ensemble."
      Journal of Physics A: Mathematical and General 39, no. 19 (2006): 5629.
  """

  force = quantity.canonicalize_force(energy_or_force)

  tau = tau * dt
  dt_2 = dt / 2.0
  dt_4 = dt_2 / 2.0
  dt_8 = dt_4 / 2.0
  dt, dt_2, dt_4, dt_8, tau = static_cast(dt, dt_2, dt_4, dt_8, tau)

  T_schedule = interpolate.canonicalize(T_schedule)

  def init_fun(key, R, mass=f32(1.0), T_initial=None):
    if T_initial is None:
      T_initial = T_schedule(0.0)

    mass = quantity.canonicalize_mass(mass)
    V = np.sqrt(T_initial / mass) * random.normal(key, R.shape, dtype=R.dtype)
    V = V - np.mean(V, axis=0, keepdims=True)
    KE = quantity.kinetic_energy(V, mass)

    # Nose-Hoover parameters.
    xi = np.zeros(chain_length, R.dtype)
    v_xi = np.zeros(chain_length, R.dtype)

    # TODO(schsam): Really, it seems like Q should be set by the goal
    # temperature rather than the initial temperature.
    DOF, = static_cast(R.shape[0] * R.shape[1])
    Q = T_initial * tau ** f32(2) * np.ones(chain_length, dtype=R.dtype)
    Q = ops.index_update(Q, 0, Q[0] * DOF)

    return NVTNoseHooverState(R, V, mass, KE, xi, v_xi, Q)  # pytype: disable=wrong-arg-count
  def step_chain(KE, V, xi, v_xi, Q, DOF, T):
    """Applies a single update to the chain parameters and rescales velocity."""
    M = chain_length - 1
    # TODO(schsam): We can probably cache the G parameters from the previous
    # update.

    t = xi.dtype
    G = np.concatenate((np.array([(KE * f32(2) - DOF * T) / Q[0]], dtype=t),
                        (Q[:-1] * v_xi[:-1] ** f32(2) - T) / Q[1:],))
    scale = np.concatenate((np.exp(-dt_8 * v_xi[1:]), np.ones((1,), dtype=t)))
    v_xi = scale * (scale * v_xi + dt_4 * G)

    scale = np.exp(-dt_2 * v_xi[0])
    KE = KE * scale ** f32(2)
    V = V * scale

    xi = xi + dt_2 * v_xi

    scale = np.concatenate((np.exp(-dt_8 * v_xi[1:]), np.ones((1,), dtype=t)))
    v_xi = scale ** 2 * v_xi
    G = (f32(2) * KE - DOF * T) / Q[0]
    for m in range(M):
      v_xi = ops.index_add(v_xi, m, scale[m] * dt_4 * G)
      G = (Q[m] * v_xi[m] ** f32(2) - T) / Q[m + 1]
    v_xi = ops.index_add(v_xi, M, dt_4 * G)

    return KE, V, xi, v_xi
  def apply_fun(state, t=f32(0), **kwargs):
    T = T_schedule(t)

    R, V, mass, KE, xi, v_xi, Q = dataclasses.astuple(state)

    DOF, = static_cast(R.shape[0] * R.shape[1])

    Q = T * tau ** f32(2) * np.ones(chain_length, dtype=R.dtype)
    Q = ops.index_update(Q, 0, Q[0] * DOF)

    KE, V, xi, v_xi = step_chain(KE, V, xi, v_xi, Q, DOF, T)
    R = shift_fn(R, V * dt_2, t=t, **kwargs)

    F = force(R, t=t, **kwargs)

    V = V + dt * F / mass
    # NOTE(schsam): Do we need to mean subtraction here?
    V = V - np.mean(V, axis=0, keepdims=True)
    KE = quantity.kinetic_energy(V, mass)
    R = shift_fn(R, V * dt_2, t=t, **kwargs)

    KE, V, xi, v_xi = step_chain(KE, V, xi, v_xi, Q, DOF, T)

    return NVTNoseHooverState(R, V, mass, KE, xi, v_xi, Q)  # pytype: disable=wrong-arg-count

  return init_fun, apply_fun


@dataclasses.dataclass
class NVTLangevinState:
  """A struct containing state information for the Langevin thermostat.

  Attributes:
    position: The current position of the particles. An ndarray of floats with
      shape [n, spatial_dimension].
    velocity: The velocity of particles. An ndarray of floats with shape
      [n, spatial_dimension].
    force: The (non-stochistic) force on particles. An ndarray of floats with
      shape [n, spatial_dimension].
    mass: The mass of particles. Will either be a float or an ndarray of floats
      with shape [n].
    rng: The current state of the random number generator.
  """
  position: Array
  velocity: Array
  force: Array
  mass: Array
  rng: Array

def nvt_langevin(energy_or_force: Callable[..., Array],
                 shift: ShiftFn,
                 dt: float,
                 T_schedule: Schedule,
                 gamma: float=0.1) -> Simulator:
  """Simulation in the NVT ensemble using the Langevin thermostat.

  Samples from the canonical ensemble in which the number of particles (N),
  the system volume (V), and the temperature (T) are held constant. Langevin
  dynamics are stochastic and it is supposed that the system is interacting with
  fictitious microscopic degrees of freedom. An example of this would be large
  particles in a solvent such as water. Thus, Langevin dynamics are a stochastic
  ODE described by a friction coefficient and noise of a given covariance.

  Our implementation follows the excellent set of lecture notes by Carlon,
  Laleman, and Nomidis [1].

  Args:
    energy_or_force: A function that produces either an energy or a force from
      a set of particle positions specified as an ndarray of shape
      [n, spatial_dimension].
    shift_fn: A function that displaces positions, R, by an amount dR. Both R
      and dR should be ndarrays of shape [n, spatial_dimension].
    dt: Floating point number specifying the timescale (step size) of the
      simulation.
    T_schedule: Either a floating point number specifying a constant temperature
      or a function specifying temperature as a function of time.
    quant: Either a quantity.Energy or a quantity.Force specifying whether
      energy_or_force is an energy or force respectively.
    gamma: A float specifying the friction coefficient between the particles
      and the solvent.
  Returns:
    See above.

    [1] E. Carlon, M. Laleman, S. Nomidis. "Molecular Dynamics Simulation."
        http://itf.fys.kuleuven.be/~enrico/Teaching/molecular_dynamics_2015.pdf
        Accessed on 06/05/2019.
  """

  force_fn = quantity.canonicalize_force(energy_or_force)

  dt_2 = dt / 2
  dt2 = dt ** 2 / 2
  dt32 = dt ** (3.0 / 2.0) / 2

  dt, dt_2, dt2, dt32, gamma = static_cast(dt, dt_2, dt2, dt32, gamma)

  T_schedule = interpolate.canonicalize(T_schedule)

  def init_fn(key, R, mass=f32(1), T_initial=None, **kwargs):
    if T_initial is None:
      T_initial = T_schedule(0.0)

    mass = quantity.canonicalize_mass(mass)

    key, split = random.split(key)

    V = np.sqrt(T_initial / mass) * random.normal(split, R.shape, dtype=R.dtype)
    V = V - np.mean(V, axis=0, keepdims=True)

    return NVTLangevinState(R, V, force_fn(R, t=f32(0), **kwargs), mass, key)  # pytype: disable=wrong-arg-count

  def apply_fn(state, t=f32(0), **kwargs):
    R, V, F, mass, key = dataclasses.astuple(state)

    N, dim = R.shape

    key, xi_key, theta_key = random.split(key, 3)
    xi = random.normal(xi_key, (N, dim), dtype=R.dtype)
    theta = random.normal(theta_key, (N, dim), dtype=R.dtype) / np.sqrt(f32(3))

    # NOTE(schsam): We really only need to recompute sigma if the temperature
    # is nonconstant. @Optimization
    # TODO(schsam): Check that this is really valid in the case that the masses
    # are non identical for all particles.
    sigma = np.sqrt(f32(2) * T_schedule(t) * gamma / mass)
    C = dt2 * (F - gamma * V) + sigma * dt32 * (xi + theta)

    R = shift(R, dt * V + F + C, t=t, **kwargs)
    F_new = force_fn(R, t=t, **kwargs)
    V = (f32(1) - dt * gamma) * V + dt_2 * (F_new + F)
    V = V + sigma * np.sqrt(dt) * xi - gamma * C

    return NVTLangevinState(R, V, F_new, mass, key)  # pytype: disable=wrong-arg-count
  return init_fn, apply_fn


@dataclasses.dataclass
class BrownianState:
  """A tuple containing state information for Brownian dynamics.

  Attributes:
    position: The current position of the particles. An ndarray of floats with
      shape [n, spatial_dimension].
    mass: The mmass of particles. Will either be a float or an ndarray of floats
      with shape [n].
    rng: The current state of the random number generator.
  """
  position: Array
  mass: Array
  rng: Array


def brownian(energy_or_force: Callable[..., Array],
             shift: ShiftFn,
             dt: float,
             T_schedule: Schedule,
             gamma: float=0.1) -> Simulator:
  """Simulation of Brownian dynamics.

  This code simulates Brownian dynamics which are synonymous with the overdamped
  regime of Langevin dynamics. However, in this case we don't need to take into
  account velocity information and the dynamics simplify. Consequently, when
  Brownian dynamics can be used they will be faster than Langevin. As in the
  case of Langevin dynamics our implementation follows [1].

  Args:
    See nvt_langevin.

  Returns:
    See above.

    [1] E. Carlon, M. Laleman, S. Nomidis. "Molecular Dynamics Simulation."
        http://itf.fys.kuleuven.be/~enrico/Teaching/molecular_dynamics_2015.pdf
        Accessed on 06/05/2019.
  """

  force_fn = quantity.canonicalize_force(energy_or_force)

  dt, gamma = static_cast(dt, gamma)

  T_schedule = interpolate.canonicalize(T_schedule)

  def init_fn(key, R, mass=f32(1)):
    mass = quantity.canonicalize_mass(mass)

    return BrownianState(R, mass, key)  # pytype: disable=wrong-arg-count

  def apply_fn(state, t=f32(0), **kwargs):

    R, mass, key = dataclasses.astuple(state)

    key, split = random.split(key)

    F = force_fn(R, t=t, **kwargs)
    xi = random.normal(split, R.shape, R.dtype)

    nu = f32(1) / (mass * gamma)

    dR = F * dt * nu + np.sqrt(f32(2) * T_schedule(t) * dt * nu) * xi
    R = shift(R, dR, t=t, **kwargs)

    return BrownianState(R, mass, key)  # pytype: disable=wrong-arg-count

  return init_fn, apply_fn
