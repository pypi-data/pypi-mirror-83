# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#  HEBI Core python API - Copyright 2020 HEBI Robotics
#  See https://hebi.us/softwarelicense for license details
#
# ------------------------------------------------------------------------------


import numpy as np
from ._internal.ffi._message_types import GroupCommand, GroupFeedback
from numpy import nan
from math import atan2

from . import robot_model as robot_model_api
from . import trajectory as trajectory_api


class Arm(object):
  """
  """

  __slots__ = (
    '_get_current_time_s', '_last_time', '_group', '_robot_model',
    '_end_effector', '_trajectory', '_trajectory_start_time', '_masses',
    '_aux_times', '_aux', '_feedback', '_command', '_tmp_4x4d', '_plugins',
    '_use_joint_limits', '_min_positions', '_max_positions')

  def __init__(self, time_getter, group, robot_model, end_effector=None, plugins=None):
    self._get_current_time_s = time_getter
    self._group = group
    self._robot_model = robot_model
    self._end_effector = end_effector
    self._plugins = []

    size = group.size

    self._last_time = time_getter()
    self._feedback = GroupFeedback(size)
    self._command = GroupCommand(size)
    self._masses = robot_model.masses

    self._trajectory = None
    self._trajectory_start_time = nan

    self._use_joint_limits = False
    self._min_positions = None
    self._max_positions = None

    self._tmp_4x4d = np.identity(4, dtype=np.float64)

    if plugins is not None:
      for plugin in plugins:
        self.add_plugin(plugin)

  @property
  def size(self):
    """
    The number of modules in the group

    :rtype: int
    """
    return self._group.size

  @property
  def group(self):
    """
    The underlying group of the arm. Guaranteed to be non-null.
    """
    return self._group

  @property
  def robot_model(self):
    """
    The underlying robot description of the arm. Guaranteed to be non-null.

    :rtype: hebi.robot_model.RobotModel
    """
    return self._robot_model

  @property
  def trajectory(self):
    """
    The underlying trajectory object used to move the arm through the prescribed
    waypoints associated with the current goal.

    If there is no currently set goal, this will be ``None``.
    """
    return self._trajectory

  @property
  def end_effector(self):
    """
    The currently set end effector. ``None`` if there is no end effector.
    """
    return self._end_effector

  @property
  def pending_command(self):
    """
    The command which will be send to the modules on :meth:`Arm.send`.
    This object is guaranteed to not change for the lifetime of the arm.

    :rtype: hebi.GroupCommand
    """
    return self._command

  @property
  def last_feedback(self):
    """
    The most recently received feedback from the arm.
    This object is guaranteed to not change for the lifetime of the arm.

    :rtype: hebi.GroupFeedback
    """
    return self._feedback

  @property
  def goal_progress(self):
    """
    Progres towards the current goal; in range of [0.0, 1.0].

    :rtype: float
    """
    trajectory = self._trajectory
    if trajectory is None:
      return 0.0

    duration = trajectory.duration
    t_traj = self._last_time - self._trajectory_start_time
    return min(t_traj, duration) / duration

  @property
  def at_goal(self):
    """
    :rtype: bool
    """
    return self.goal_progress >= 1.0

  def add_plugin(self, plugin):
    """
    Adds the specified plugin to the arm.
    :meth:`ArmPlugin.on_associated` callback is invoked on the plugin specified.

    Additionally, the plugin is explicitly set to enabled,
    *i.e.*, ``plugin.enabled = True``.

    :param plugin: the plugin to add
    :type plugin: .ArmPlugin
    """
    plugin.enabled = True
    plugin.on_associated(self)
    self._plugins.append(plugin)

  def load_gains(self, gains_file, attempts=5):
    """
    Load the gains from the provided file and send the gains to the underlying modules in the group.

    This method requests acknowledgement from all modules in the group that the gains
    were received. Consequently, this method may take a few seconds to execute
    if you are on a network which drops packets (e.g., a suboptimal WiFi network).
    The `attempts` parameter is used to re-send the gains to modules, on the event
    that an ack was not received from each module in the group.

    :param gains_file: The file location of the gains file
    :param attempts: the number of attempts to send the gains to the group.

    :return: ``True`` if gains were successfully sent to the modules; otherwise ``False`` 
    :rtype:  bool
    """
    gains_cmd = GroupCommand(self._group.size)
    gains_cmd.read_gains(gains_file)

    return _repetitive_send_command_with_ack(self._group, gains_cmd, attempts)

  def update(self):
    """
    Receive feedback from the modules, compute pending commands, and update
    state for the end effector and any associated plugins

    :return: ``True`` if feedback was received and all components were able to be updated;
             ``False`` otherwise
    :rtype:  bool
    """
    t = self._get_current_time_s()

    # Time must be monotonically increasing
    if t < self._last_time:
      return False

    self._last_time = t
    group = self._group
    feedback = self._feedback

    if not group.get_next_feedback(reuse_fbk=feedback):
      return False
    
    command = self._command
    trajectory = self._trajectory
    robot_model = self._robot_model
    masses = self._masses
    end_effector = self._end_effector
    aux = []

    if trajectory is not None:
      t_traj = min(t - self._trajectory_start_time, trajectory.duration)
      pos, vel, acc = trajectory.get_state(t_traj)
      aux = self.get_aux(t_traj)
    else:
      pos = nan
      vel = nan
      acc = 0.0

    command.position = pos
    command.velocity = vel

    # this could be done just at arm initialization, but end effector mass/payload may change
    np.copyto(masses, robot_model.masses) # TODO: remove the extra copy from `robot_model.masses`

    command.effort = _get_grav_comp_efforts(robot_model, masses, feedback)
    
    # TODO: Dynamic comp efforts

    res = True

    if end_effector is not None:
      res = res and end_effector.update(aux)

    for plugin in self._plugins:
      if plugin.enabled:
        # Only invoke the plugin if enabled
        res and plugin.update(self)

    return res

  def send(self):
    """
    Send the pending commands to the arm and end effector (if non-null).

    :return: ``True`` if command was successfully sent to all components; ``False`` otherwise
    :rtype:  bool
    """
    res = self._group.send_command(self._command)
    end_effector = self._end_effector
    if end_effector is not None:
      res = res and end_effector.send()

    return res 

  def set_end_effector(self, end_effector):
    """
    Update the currently set end effector for the arm
    """
    self._end_effector = end_effector

  def set_goal(self, goal):
    """
    Sets the current goal of the arm as described by the input waypoints.

    :param goal: Goal object representing waypoints of the goal
    :type goal:  Goal
    """
    self.__set_goal(**goal.build())

  def __set_goal(self, positions, times=None, velocities=None, accelerations=None, aux=None):
    """
    Sets the current goal of the arm as described by the input waypoints.
    
    :param positions: collection of one or more waypoints providing the position at each waypoint
    :type positions:  list, numpy.ndarray

    :param times: list of time points for each waypoint, with initial time being 0.
                  If this is ``None``, a heuristic is used to provide time points for each waypoint.
    :type times:  list, numpy.ndarray

    :param velocities: collection of one or more waypoints providing the velocity at each waypoint.
                       If this is ``None``, the velocities at each waypoint are unconstrained.
    :type velocities:  list, numpy.ndarray

    :param accelerations: collection of one or more waypoints providing the acceleration at each waypoint.
                          If this is ``None``, the accelerations at each waypoint are unconstrained.
    :type accelerations:  list, numpy.ndarray

    :param aux: list of aux values at each waypoint. If not specified, there will be no aux values are
                cleared, and :meth:`Arm.get_aux` will return an empty list.
    :type aux:  list, numpy.ndarray
    """
    input_shape = positions.shape

    num_joints = input_shape[0]

    trajectory = self._trajectory
    if trajectory is None:
      # If there is no current trajectory, there is no goal currently set.
      # Use the current robot state as the initial waypoint for the goal.
      feedback = self._feedback
      curr_pos = feedback.position
      curr_vel = feedback.velocity
      curr_acc = np.zeros(num_joints)
    else:
      # Goal already exists. Use the expected goal locaton at the current time
      # as the initial waypoint for the new goal.
      t_traj = self._last_time - self._trajectory_start_time
      t_traj = min(t_traj, trajectory.duration)
      curr_pos, curr_vel, curr_acc = trajectory.get_state(t_traj)

    if len(input_shape) == 1:
      # Input is a single waypoint
      num_waypoints = 2
    else:
      num_waypoints = input_shape[1] + 1

    dst_positions = np.empty((num_joints, num_waypoints), dtype=np.float64)
    dst_velocities = np.empty((num_joints, num_waypoints), dtype=np.float64)
    dst_accelerations = np.empty((num_joints, num_waypoints), dtype=np.float64)

    # Initial state
    dst_positions[:, 0] = curr_pos
    dst_velocities[:, 0] = curr_vel
    dst_accelerations[:, 0] = curr_acc

    # Copy new waypoints
    dst_positions[:, 1:] = positions.reshape((num_joints, num_waypoints - 1))
    dst_velocities[:, 1:] = velocities.reshape((num_joints, num_waypoints - 1))
    dst_accelerations[:, 1:] = accelerations.reshape((num_joints, num_waypoints - 1))

    waypoint_times = np.empty(num_waypoints)
    # If time is not provided, calculate it using a heuristic
    if times is None:
      _get_waypoint_times(waypoint_times, num_waypoints, dst_positions, dst_velocities, dst_accelerations)
    else:
      waypoint_times[0] = 0.0
      waypoint_times[1:] = times

    # Create new trajectory based off of the goal
    self._trajectory = trajectory_api.create_trajectory(waypoint_times, dst_positions, dst_velocities, dst_accelerations)
    self._trajectory_start_time = self._last_time

    # Update aux state
    if aux is None:
      self._aux = []
      self._aux_times = []
    else:
      goal_aux = np.asarray(aux)
      aux_shape = goal_aux.shape

      # HACK: Figure out a better way to handle logic here...
      if len(aux_shape) == 1:
        # Will occur if the aux provided is an array of scalars (i.e., 1 aux value per waypoint)
        second_dim = num_waypoints
      else:
        # Will occur if the aux provided has more than 1 aux value per waypoint
        second_dim = aux_shape[1] + 1

      first_dim = aux_shape[0]
      if first_dim > 0 and (second_dim == num_waypoints):
        # Update aux
        aux = np.empty((first_dim, second_dim), dtype=np.float64)
        # aux = self._aux
        aux[:, 0] = nan
        aux[:, 1:] = goal_aux
        self._aux_times = waypoint_times
        self._aux = aux
      else:
        self._aux = []
        self._aux_times = []

  def set_aux_state(self, aux_state):
    """
    Replace the current aux state with the provided input.

    :param aux_state: The updated aux state
    :type aux_state: collections.abc.Sequence
    """
    aux_size = len(aux_state)
    if aux_size > 0:
      aux_times = [self._get_current_time_s()]
      aux = np.empty((aux_size, 1), dtype=np.float64)
      for i in range(aux_size):
        aux[i] = aux_state[i]
    else:
      aux = np.empty(0)
      aux_times = np.empty(0)

    self._aux = aux
    self._aux_times = aux_times

  def get_aux(self, t):
    """
    Retrieve the aux value at the given time point.
    If there are no aux values, an empty array is returned.

    :param t: The point in time, intended to be within the interval determined
              by the current goal.

    :rtype: np.ndarray
    """
    aux = self._aux
    aux_times = self._aux_times
    size = len(aux_times)
    t = float(t)

    if size == 0:
      return np.empty(0)

    for i in range(size):
      idx = i - 1
      if t >= aux_times[idx]:
        return aux[:, i].copy()

    return aux[:, 0].copy()

  def cancel_goal(self):
    """
    Removes any currently set goal.
    """
    self._trajectory = None
    self._trajectory_start_time = nan

  def set_joint_limits(self, min_positions, max_positions):
    """
    Replace any currently set joint limits with the limits provided
    
    :param min_positions: The minimum position limits. Must be a list and not a scalar.
    :param max_positions: The maximum position limits. Must be a list and not a scalar.
    :type min_positions: collections.abc.Sequence
    :type max_positions: collections.abc.Sequence
    """
    expected_size = self._robot_model.dof_count
    if len(min_positions) != expected_size or len(max_positions) != expected_size:
      raise ValueError("Input size must be equal to degrees of freedom in robot")

    if any(np.isnan(min_positions) or np.isnan(max_positions)):
      raise ValueError("Input must be non-nan")

    self._min_positions = np.asarray(min_positions)
    self._max_positions = np.asarray(max_positions)
    self._use_joint_limits = True

  def clear_joint_limits(self):
    """
    Removes any currently set joint limits.
    """
    self._use_joint_limits = False
    self._min_positions = None
    self._max_positions = None

  def FK(self, positions, **kwargs):
    """
    Retrieves the output frame of the end effector at the provided joint positions.

    The keys provided below show the possible retrievable representations
    of the resulting end effector transform.

    Possible keys:
      * `xyz_out`:          Used to store the 3d translation vector of the end effector
                            If this is set, this is also the object returned. 
      * `tip_axis_out`:     Used to store the tip axis of the end effector
      * `orientation_out`:  Used to store the orientation (SO3 matrix) of the end effector

    :param positions: The joint space positions

    :return: The 3d translation vector of the end effector
    """
    out = kwargs.get('xyz_out', None)
    if out is None:
      ret = np.zeros((3,), dtype=np.float64)
    else:
      ret = out

    tmp = self._tmp_4x4d
    self._robot_model.get_end_effector(positions, output=tmp)
    np.copyto(ret, tmp[0:3, 3])

    tip_axis_out = kwargs.get('tip_axis_out', None)
    if tip_axis_out is not None:
      np.copyto(tip_axis_out, tmp[0:3, 2])
    
    orientation_out = kwargs.get('orientation_out', None)
    if orientation_out is not None:
      np.copyto(orientation_out, tmp[0:3, 0:3])

    return ret

  def ik_target_xyz(self, initial_position, target_xyz, out=None):
    """
    Solve for the joint space positions such that the end effector is near
    the target xyz position in space specified.

    If there are any joint limits set, the solver will attempt to respect them.

    :param initial_position: The seed angles for the IK solver
    :param target_xyz: The intended destination coordinate as a 3d vector 
    :param out: The optional output parameter (also always returned)
    """
    if out is None:
      ret = np.zeros(len(initial_position), dtype=np.float64)
    else:
      ret = out

    objective = robot_model_api.endeffector_position_objective(target_xyz)

    if self._use_joint_limits:
      # Add the `joint_limit_constraint` to the list of IK objectives
      joint_objective = robot_model.joint_limit_constraint(
        self._min_positions, self._max_positions)
      self._robot_model.solve_inverse_kinematics(initial_position, objective,
                                                 joint_objective, output=ret)
    else:
      self._robot_model.solve_inverse_kinematics(initial_position, objective,
                                                 output=ret)

    return ret

  def ik_target_xyz_tip_axis(self, initial_position, target_xyz, tip_axis, out=None):
    """
    Solve for the joint space positions such that the end effector is near
    the target xyz position in space and also oriented along the axis specified.

    If there are any joint limits set, the solver will attempt to respect them.

    :param initial_position: The seed angles for the IK solver
    :param target_xyz: The intended destination coordinate as a 3d vector 
    :param tip_axis: The intended destination tip axis as a 3d vector
    :param out: The optional output parameter (also always returned)
    """
    if out is None:
      ret = np.zeros(len(initial_position), dtype=np.float64)
    else:
      ret = out

    objectives = list()
    objectives.append(robot_model_api.endeffector_position_objective(target_xyz))
    objectives.append(robot_model_api.tip_axis_objective(target_xyz))

    if self._use_joint_limits:
      # Add the `joint_limit_constraint` to the list of IK objectives
      objectives.append(robot_model_api.joint_limit_constraint(
        self._min_positions, self._max_positions))

    return self._robot_model.solve_inverse_kinematics(initial_position, *objectives,
                                                      output=ret)

  def ik_target_xyz_so3(self, initial_position, target_xyz, orientation, out=None):
    """
    Solve for the joint space positions such that the end effector is near
    the target xyz position in space with the specified SO3 orientation.

    If there are any joint limits set, the solver will attempt to respect them.

    :param initial_position: The seed angles for the IK solver
    :param target_xyz: The intended destination coordinate as a 3d vector 
    :param orientation: The intended destination orientation as an SO3 matrix
    :param out: The optional output parameter (also always returned)
    """
    if out is None:
      ret = np.zeros(len(initial_position), dtype=np.float64)
    else:
      ret = out

    objectives = list()
    objectives.append(robot_model_api.endeffector_position_objective(target_xyz))
    objectives.append(robot_model_api.endeffector_so3_objective(orientation))

    if self._use_joint_limits:
      # Add the `joint_limit_constraint` to the list of IK objectives
      objectives.append(robot_model_api.joint_limit_constraint(
        self._min_positions, self._max_positions))

    return self._robot_model.solve_inverse_kinematics(initial_position, *objectives,
                                                      output=ret)


class Goal(object):
  """
  Used to construct a goal for an arm. Intended to be passed into :meth:`Arm.set_goal`.
  """
  
  __slots__ = ('_times', '_positions', '_velocities', '_accelerations', '_aux', '_dof_count',
    '_waypoints_valid', '_result', '_user_time', '_user_aux')

  def __init__(self, dof_count):
    self._times = []
    self._positions = []
    self._velocities = []
    self._accelerations = []
    self._aux = []
    self._dof_count = dof_count
    self._waypoints_valid = False
    self._user_time = False
    self._user_aux = False

    res = dict()
    res['times'] = None
    res['positions'] = None
    res['velocities'] = None
    res['accelerations'] = None
    res['aux'] = None
    self._result = res

  @property
  def waypoint_count(self):
    """
    :return: The number of waypoints added to this goal
    :rtype: int
    """
    return len(self._positions)

  @property
  def dof_count(self):
    """
    :return: The number of degrees of freedom in each waypoint
    :rtype: int
    """
    return self._dof_count

  def build(self):
    """
    Return the dictionary depicting the currently specified elements
    """
    if self._waypoints_valid:
      # Already cached results - return it
      return self._result

    num_waypoints = self.waypoint_count
    dof_count = self._dof_count

    if num_waypoints < 1:
      raise ValueError("A goal must have at least 1 waypoint")

    ret = self._result
    positions = np.empty((dof_count, num_waypoints), dtype=np.float64)
    velocities = np.empty((dof_count, num_waypoints), dtype=np.float64)
    accelerations = np.empty((dof_count, num_waypoints), dtype=np.float64)
    aux = self._aux

    last_waypoint = num_waypoints - 1

    in_pos = self._positions
    in_vel = self._velocities
    in_acc = self._accelerations

    for i in range(num_waypoints):
      pos_val = in_pos[i]
      vel_val = in_vel[i]
      acc_val = in_acc[i]

      if pos_val is None:
        if i == 0 or i == last_waypoint:
          pos_val = 0.0
        else:
          pos_val = nan

      if vel_val is None:
        if i == 0 or i == last_waypoint:
          vel_val = 0.0
        else:
          vel_val = nan

      if acc_val is None:
        if i == 0 or i == last_waypoint:
          acc_val = 0.0
        else:
          acc_val = nan

      positions[:, i] = pos_val
      velocities[:, i] = vel_val
      accelerations[:, i] = acc_val

    if self._user_time:
      times = np.asarray(self._times, dtype=np.float64)
    else:
      times = None

    ret['times'] = times
    ret['positions'] = positions
    ret['velocities'] = velocities
    ret['accelerations'] = accelerations
    ret['aux'] = aux

    self._waypoints_valid = True

    return ret

  def clear(self):
    """
    Remove any added waypoints
    """
    self._waypoints_valid = False
    self._times.clear()
    self._positions.clear()
    self._velocities.clear()
    self._accelerations.clear()
    self._aux.clear()
    self._user_time = False
    self._user_aux = False

    return self

  def add_waypoint(self, t=None, position=None, velocity=None, acceleration=None, aux=None, time_relative=True):
    """
    
    :param t: The time point associated with this waypoint. `time_relative`
              parameter dictates whether this is relative or absolute.
              If ``None``, a heuristic will be used to determine time between waypoints.
              ``t`` must be defined for all waypoints or none.
    :type t:  int, float

    :param position: Scalar or vector corresponding to the position of each degree of freedom for the given waypoint.
                     If ``None``, this is interpreted as a "free" constraint (`nan`).
    :type position:  float, numpy.ndarray

    :param velocity: Scalar or vector corresponding to the velocity of each degree of freedom for the given waypoint.
                     If ``None``, this is interpreted as a "free" constraint (`nan`).
    :type velocity:  float, numpy.ndarray

    :param acceleration: Scalar or vector corresponding to the acceleration of each degree of freedom for the given
                         waypoint. If ``None``, this is interpreted as a "free" constraint (`nan`).
    :type acceleration:  float, numpy.ndarray

    :param aux: The aux value for the given waypoint. All other invocations of `add_waypoint` prior to passing this
                to :meth:`Arm.set_goal` must be consistent: either provide an ``aux`` value for each
                waypoint, or do not provide any at all.
    :type aux:  float, numpy.ndarray

    :param time_relative: Specifies whether to interpret `t` as relative or absolute. If this is the first waypoint
                          being added, this is relative to 0.
    :type time_relative:  bool
    """
    times_len = len(self._times)
    waypoint_count = self.waypoint_count
    dof_count = self._dof_count
    user_time = self._user_time
    user_aux = self._user_aux

    if waypoint_count > 0:
      if t is not None and not user_time:
        # ``t`` was not provided previously but now is
        raise ValueError("waypoint times must be defined for all waypoints or none")
      elif t is None and user_time:
        # ``t`` was provided previously but not here
        raise ValueError("waypoint times must be defined for all waypoints or none")

      if aux is not None and not user_aux:
        # ``aux`` was not provided previously but now is
        raise ValueError("waypoint aux must be defined for all waypoints or none")
      elif aux is None and user_aux:
        # ``aux`` was provided previously but not here
        raise ValueError("waypoint aux must be defined for all waypoints or none")

    if user_time:
      if time_relative:
        t = self._times[-1] + t
      # Check edge cases with time
      if self._times[-1] >= t:
        raise ValueError("waypoint times must be monotonically increasing")
      elif not np.isfinite(t):
        raise ValueError("waypoint times must be finite")

    if position is None and velocity is None and acceleration is None:
      # At least one derivative of position, or position itself must be passed in for each waypoint
      raise ValueError("At least one of the following arguments must be non-null: position, velocity, acceleration")

    if position is not None:
      pos_val = position
      if len(position) != dof_count:
        raise ValueError("length of position input must be equal to dof_count")
    else:
      pos_val = None

    if velocity is not None:
      vel_val = velocity
      if len(velocity) != dof_count:
        raise ValueError("length of velocity input must be equal to dof_count")
    else:
      vel_val = None

    if acceleration is not None:
      acc_val = acceleration
      if len(acceleration) != dof_count:
        raise ValueError("length of acceleration input must be equal to dof_count")
    else:
      acc_val = None

    self._waypoints_valid = False
    self._positions.append(pos_val)
    self._velocities.append(vel_val)
    self._accelerations.append(acc_val)

    if waypoint_count == 0:
      # Set the rule for any additional waypoints
      user_time = t is not None
      user_aux = aux is not None
      self._user_time = user_time
      self._user_aux = user_aux

    if user_time:
      self._times.append(t)

    if user_aux:
      self._aux.append(aux)

    return self


class EndEffector(object):
  """
  Abstract base class representing an end effector to be used with an Arm object.
  """
  
  def __init__(self): pass

  def update(self, aux_state):
    """
    Update the aux state of the end effector.

    :param aux_state: a scalar number (`int` or `float`) or list of numbers.
    :type aux_state:  int, float, list

    :return: ``True`` on success, otherwise ``False``
    """
    return True

  def send(self):
    """
    Sends the currently pending command to the end effector.

    :return: ``True`` on success; otherwise ``False``
    :rtype: bool
    """
    return True


class Gripper(EndEffector):
  """
  End effector implementation which is intended to be used to provide
  gripper functionality.
  """

  __slots__ = ('_state', '_close_effort', '_open_effort', '_group', '_command')

  def __init__(self, group, close_effort, open_effort):
    self._group = group
    self._close_effort = close_effort
    self._open_effort = open_effort
    self._command = GroupCommand(1)
    self._state = 0.0

  @property
  def state(self):
    """
    The current state of the gripper. Range of the value is [0.0, 1.0].

    :rtype: float
    """
    return self._state

  @property
  def command(self):
    """
    The underlying command to be sent to the gripper. Can be modified
    to extend functionality.

    :rtype: hebi.GroupCommand
    """
    return self._command

  def close(self):
    """
    Sets the gripper to be fully closed
    """
    self.update(1.0)

  def open(self):
    """
    Sets the gripper to be fully open
    """
    self.update(0.0)

  def toggle(self):
    """
    Toggle the state of the gripper.

    If the gripper was fully closed, it will become fully open.
    If the gripper was fully open, it will become fully closed.
    Otherwise, this method is a no-op.
    """
    if self._state == 0.0:
      self.update(1.0)
    elif self._state == 1.0:
      self.update(0.0)

  def send(self):
    """
    Send the command to the gripper.

    :return: the result of :meth:`hebi._internal.group.Group.send_command`
    """
    return self._group.send_command(self._command)

  def update(self, aux):
    """
    Update the state of the gripper

    :param aux: The aux data. Can be a scalar value or a list of values.
                If a list, it is expected to contain only one element.
                Values be finite.
    :type aux:  int, float, numpy.ndarray

    :return: ``True`` on success; ``False`` otherwise
    """
    if isinstance(aux, (int, float)):
      val = aux
    elif hasattr(aux, '__len__'):
      if len(aux) == 1:
        val = aux[0]
      else:
        return False
    else:
      return False

    if not np.isfinite(val):
      return False

    self._command.effort = (val * self._close_effort + (1.0 - val) * self._open_effort)
    self._state = val
    return True

  def load_gains(self, gains_file, attempts=5):
    """
    Load the gains from the provided file and send the gains to the gripper.

    This method requests acknowledgement from the gripper that the gains
    were received. Consequently, this method may take a few seconds to execute
    if you are on a network which drops packets (e.g., a suboptimal WiFi network).
    The `attempts` parameter is used to re-send the gains, in the event
    that an ack was not received from the gripper.

    :param gains_file: The file location of the gains file
    :param attempts: the number of attempts to send the gains to the gripper.

    :return: ``True`` if gains were successfully sent to the gripper; otherwise ``False`` 
    :rtype:  bool
    """
    gains_cmd = GroupCommand(self._group.size)
    gains_cmd.read_gains(gains_file)

    return _repetitive_send_command_with_ack(self._group, gains_cmd, attempts)


class ArmPlugin(object):
  """
  Abstract base class representing a plugin to be used for an Arm object.
  """

  __slots__ = ('_enabled')

  @property
  def enabled(self):
    """
    Determines if the plugin should be invoked by the owning arm.
    If ``False``, this plugin will not be invoked on :meth:`Arm.update`.

    :rtype: bool
    """
    return self._enabled

  @enabled.setter
  def enabled(self, value):
    self._enabled = bool(value)

  def update(self, arm):
    """
    Callback which updates state on the arm. Invoked by :meth:`Arm.update`.

    An implementation must return a boolean denoting ``True`` on success
    and ``False`` otherwise.
    """
    pass

  def on_associated(self, arm):
    """
    Override to update any state based on the associated arm.

    Invoked when the instance is added to an arm via :meth:`Arm.add_plugin`
    """
    pass


class EffortOffset(ArmPlugin):
  """
  Plugin implementation used to offset the effort to be sent to the group.

  This offset can be scalar or a vector of length equal to the size of the group.
  """

  __slots__ = ('_offset')

  def __init__(self, offset):
    self._offset = offset

  @property
  def offset(self):
    return self._offset

  @offset.setter
  def offset(self, value):
    self._offset = value

  def update(self, arm):
    cmd = arm.pending_command
    cmd.effort = cmd.effort + self._offset

    return True


class ImpedanceController(ArmPlugin):
  """
  Plugin implementation which provides an impedance controller for the arm.
  """

  __slots__ = (
    '_desired_tip_fk', '_actual_tip_fk', '_jacobian_end_effector', '_cmd_pos',
    '_cmd_vel', '_fbk_pos', '_cmd_effort', '_fbk_vel', '_impedance_effort',
    '_spring_gains', '_damper_gains', '_gains_in_end_effector_frame')

  def __init__(self, gains_in_end_effector_frame=False):
    self._jacobian_end_effector = None
    self._cmd_pos = None
    self._cmd_vel = None
    self._cmd_effort = None
    self._fbk_pos = None
    self._fbk_vel = None
    self._impedance_effort = None

    self._desired_tip_fk = np.identity(4, dtype=np.float64)
    self._actual_tip_fk = np.identity(4, dtype=np.float64)
    self._spring_gains = np.zeros(6, dtype=np.float64)
    self._damper_gains = np.zeros(6, dtype=np.float64)
    self._gains_in_end_effector_frame = gains_in_end_effector_frame

  @property
  def gains_in_end_effector_frame(self):
    """
    Determines whether the gains are relative to the end effector frame
    """
    return self._gains_in_end_effector_frame

  @gains_in_end_effector_frame.setter
  def gains_in_end_effector_frame(self, value):
    self._gains_in_end_effector_frame = value

  def on_associated(self, arm):
    dof_count = arm.robot_model.dof_count

    self._jacobian_end_effector = np.zeros((6, dof_count), dtype=np.float64)
    self._cmd_pos = np.zeros(dof_count, dtype=np.float64)
    self._cmd_vel = np.zeros(dof_count, dtype=np.float64)
    self._cmd_effort = np.zeros(dof_count, dtype=np.float64)
    self._fbk_pos = np.zeros(dof_count, dtype=np.float64)
    self._fbk_vel = np.zeros(dof_count, dtype=np.float64)
    self._impedance_effort = np.zeros(dof_count, dtype=np.float64)

  def set_spring_gains(self, x, y, z, roll, pitch, yaw):
    """
    Sets the spring gains for the impedance controller.

    :type x:     float
    :type y:     float
    :type z:     float
    :type roll:  float
    :type pitch: float
    :type yaw:   float
    """
    self._spring_gains[0] = x
    self._spring_gains[1] = y
    self._spring_gains[2] = z
    self._spring_gains[3] = roll
    self._spring_gains[4] = pitch
    self._spring_gains[5] = yaw

  def set_damper_gains(self, x, y, z, roll, pitch, yaw):
    """
    Sets the damper gains for the impedance controller.

    :type x:     float
    :type y:     float
    :type z:     float
    :type roll:  float
    :type pitch: float
    :type yaw:   float
    """
    self._damper_gains[0] = x
    self._damper_gains[1] = y
    self._damper_gains[2] = z
    self._damper_gains[3] = roll
    self._damper_gains[4] = pitch
    self._damper_gains[5] = yaw

  def update(self, arm):
    arm_cmd = arm.pending_command
    arm_fbk = arm.last_feedback

    cmd_pos = arm_cmd.position
    cmd_vel = arm_cmd.velocity

    if np.isnan(cmd_pos).any() or np.isnan(cmd_vel).any():
      return

    cmd_eff = arm_cmd.effort
    fbk_pos = arm_fbk.position
    fbk_vel = arm_fbk.velocity

    # instance cached to improve fast-path performance
    jacobian_end_effector = self._jacobian_end_effector
    actual_tip_fk = self._actual_tip_fk
    desired_tip_fk = self._desired_tip_fk

    kin = arm.robot_model
    kin.get_end_effector(cmd_pos, desired_tip_fk)
    kin.get_end_effector(fbk_pos, actual_tip_fk)
    kin.get_jacobian_end_effector(fbk_pos, jacobian_end_effector)

    xyz_error = desired_tip_fk[0:3, 3] - actual_tip_fk[0:3, 3]
    error_rot_mat = desired_tip_fk[0:3, 0:3] * actual_tip_fk[0:3, 0:3].T
    axis, angle = _rot2axisangle(error_rot_mat)
    rot_error_vec = angle * axis

    gains_in_end_effector_frame = self._gains_in_end_effector_frame

    if gains_in_end_effector_frame:
      mat = actual_tip_fk[0:3, 0:3].T
      xyz_error[:] = mat.dot(xyz_error)
      rot_error_vec[:] = mat.dot(rot_error_vec)

    pos_error = np.empty(6, dtype=np.float64)
    pos_error[0:3] = xyz_error
    pos_error[3:6] = rot_error_vec
    vel_error = jacobian_end_effector @ (cmd_vel - fbk_vel)
    vel_error[3:6] = 0.0

    spring_wrench = np.multiply(pos_error, self._spring_gains)

    if gains_in_end_effector_frame:
      spring_wrench[0:3] = actual_tip_fk[0:3, 0:3].dot(spring_wrench[0:3])
      spring_wrench[3:6] = actual_tip_fk[0:3, 0:3].dot(spring_wrench[3:6])

    damper_wrench = np.multiply(vel_error, self._damper_gains)
    impedance_effort = jacobian_end_effector.T @ (spring_wrench + damper_wrench)

    cmd_eff += impedance_effort
    arm_cmd.effort = cmd_eff

    return True


class DoubledJointMirror(ArmPlugin):
  """
  Plugin implementation meant to be used for an arm that has a joint
  which is composed of two modules in series.
  """

  __slots__ = ('_group', '_cmd', '_index')

  def __init__(self, index, group):
    if group.size != 1:
      raise ValueError("Expected a group of size 1")
    if index < 0:
      raise ValueError("index must be non-negative")

    self._group = group
    self._index = index
    self._cmd = GroupCommand(1)

  def update(self, arm):
    arm_cmd = arm.pending_command
    index = self._index

    src = arm_cmd[index]
    dst = self._cmd

    src_pos = src.position
    src_vel = src.velocity
    src_eff = src.effort

    if not np.isnan(src_pos):
      dst.position = -src_pos
    if not np.isnan(src_vel):
      dst.velocity = -src_vel
    if not np.isnan(src_eff):
      # split the effort between the 2 actuators
      new_effort = src_eff * 0.5
      src.effort = src_eff
      dst.effort = -src_eff

    return self._group.send(dst)


################################################################################
# Internal Helper Functions
################################################################################


def _rot2axisangle(R):
  axis = np.empty(3, np.float64)
  axis[0] = R[2, 1] - R[1, 2]
  axis[1] = R[0, 2] - R[2, 0]
  axis[2] = R[1, 0] - R[0, 1]

  y = np.hypot(axis[0], np.hypot(axis[1], axis[2]))
  axis = axis / y
  return axis, atan2(y, R[:3, :3].diagonal().sum()-1)


def _gravity_from_quaternion(quaternion):
  output = np.empty(3, dtype=np.float64)

  X = quaternion[1]
  Y = quaternion[2]
  Z = quaternion[3]
  W = quaternion[0]

  xx = X*X
  xz = X*Z
  xw = X*W
  yy = Y*Y
  yz = Y*Z
  yw = Y*W

  output[0] = -2.0*(xz-yw)
  output[1] = -2.0*(yz+xw)
  output[2] = -1.0+2.0*(xx+yy)

  return output


def _get_grav_comp_efforts(robot, masses, feedback):
  """
  :rtype:  np.ndarray
  """
  positions = feedback.position
  gravity = _gravity_from_quaternion(feedback.orientation[0])
  g_norm = np.linalg.norm(gravity)
  output = np.zeros(robot.dof_count, dtype=np.float64)
  if g_norm > 0.0:
    gravity = gravity/g_norm*-9.81

  jacobians = robot.get_jacobians('CoM', positions)
  wrench = np.zeros(6)
  num_frames = robot.get_frame_count('CoM')
  masses = robot.masses

  for i in range(num_frames):
    # Add the torques for each joint to support the mass at this frame
    wrench[0:3] = gravity*masses[i]
    output += jacobians[i].T @ wrench

  return output


def _get_waypoint_times(times, num_waypoints, positions, velocities, accelerations):
  for i in range(num_waypoints):
    times[i] = 1.2 * i

  return times


def _repetitive_send_command_with_ack(group, cmd, attempts):
  for i in range(attempts):
    try:
      if group.send_command_with_acknowledgement(cmd, timeout):
        return True
    except:
      pass

  return False


################################################################################
# 
################################################################################

from time import time
_start_time = time()


def create(families, names=None, command_lifetime=100, control_frequency=100.0,
           hrdf_file=None, robot_model=None, end_effector=None,
           time_getter=None, lookup=None):
  """
  Create an arm object based off of the provided kinematic representation.

  Examples::

    import hebi
    from hebi import arm as arm_api

    # Create based off of a 6-DoF arm with an HRDF file
    arm1 = arm_api.create(["Example Arm"],
                          names=['J1_base', 'J2_shoulder', 'J3_elbow', 'J4_wrist1', 'J5_wrist2', 'J6_wrist3'],
                          hrdf_file="hrdf/A-2085-06.hrdf")

    # Use some existing objects
    lookup = hebi.Lookup()
    existing_robot_model = get_robot_model()
    families = get_families()
    names = get_names()
    time_function = get_simulator_time_function()

    arm2 = arm_api.create(families=families, names=names,
                          robot_model=existing_robot_model,
                          time_getter=time_function,
                          lookup=lookup)


  :param families: Required parameter.
  :type families:  list, str

  :param names: Names of the modules in the group. If ``None``,
                :meth:`hebi.Lookup.get_group_from_family` will be used
  :type names:  list

  :param command_lifetime: How long a command takes effect for on the robot
                           before expiring.
  :type command_lifetime:  int

  :param control_frequency: Loop rate, in Hz. This is how fast the arm update
                            loop will nominally run.
  :type control_frequency:  float

  :param hrdf_file: The robot description. Cannot be used in combination
                    with ``robot_model``.
  :type hrdf_file:  str

  :param robot_model: The robot description. Cannot be used in combination
                      with ``hrdf_file``.
  :type robot_model:  hebi.robot_model.RobotModel

  :param end_effector: Optionally, supply an end effector to be controlled
                       by the "aux" state of provided goals.
  :type end_effector:  hebi.arm.EndEffector

  :param time_getter: A function pointer which returns a float representing
                      the current time in seconds. Can be overloaded
                      to use, e.g., simulator time
  :type time_getter:  callable

  :param lookup: An optional lookup instance to use to find the group.
                 The default instance will be provided if ``None``
  :type lookup:  hebi.Lookup

  :rtype: hebi.arm.Arm
  """

  command_lifetime = int(command_lifetime)
  control_frequency = float(control_frequency)
  
  if hrdf_file is not None and robot_model is not None:
    raise ValueError("hrdf_file or robot_model must be defined, but not both")
  elif hrdf_file is None and robot_model is None:
    raise ValueError("hrdf_file or robot_model must be defined")

  if time_getter is not None:
    if not callable(time_getter):
      raise TypeError("time_getter must be a callable object")
  elif time_getter is None:
    time_getter = lambda: time() - _start_time

  if lookup is None:
    from . import Lookup
    lookup = Lookup()
    from time import sleep
    # Allow lookup registry to populate
    sleep(2)

  if hrdf_file is not None:
    from .robot_model import import_from_hrdf
    robot = import_from_hrdf(hrdf_file)
  else:
    robot = robot_model

  if names is not None:
    group = lookup.get_group_from_names(families, names)
  else:
    group = lookup.get_group_from_family(families)

  if group is None:
    raise RuntimeError('Could not create arm. Check that family and names match actuators on the network.')

  if group.size != robot.dof_count:
    raise RuntimeError('Robot does not have the same number of actuators as group.')

  group.command_lifetime = command_lifetime
  group.feedback_frequency = control_frequency

  got_feedback = False
  for i in range(10):
    if group.get_next_feedback() is not None:
      got_feedback = True
      break

  if not got_feedback:
    raise RuntimeError("Could not communicate with robot: check your network connection.")

  return Arm(time_getter, group, robot, end_effector)
