from .ffi._message_types import GroupCommand, GroupFeedback


_btn_state_str_to_enum_map = {
  'Off'   : 0,
  'On'    : 1,
  'ToOff' : 2,
  'ToOn'  : 3
}

def _state_repr(name, obj):
  def btn_repr(btn):
    ret = '  Button {0}:'.format(btn)
    return ret + ' {0} ({1})\n'.format(obj.get_button_state(btn), obj.get_button_diff(btn))

  def axis_repr(axis):
    ret = '  Axis {0}:'.format(axis)
    return ret + '   {0}\n'.format(obj.get_axis_state(axis))

  ret = '{0}:\n'.format(name)
  ret += btn_repr(1)
  ret += btn_repr(2)
  ret += btn_repr(3)
  ret += btn_repr(4)
  ret += btn_repr(5)
  ret += btn_repr(6)
  ret += btn_repr(7)
  ret += btn_repr(8)
  ret += axis_repr(1)
  ret += axis_repr(2)
  ret += axis_repr(3)
  ret += axis_repr(4)
  ret += axis_repr(5)
  ret += axis_repr(6)
  ret += axis_repr(7)
  ret += axis_repr(8)

  return ret


def _transition_button_state(new_value, button):
  prev_button_value = button._value
  current_button_value = bool(new_value)

  if prev_button_value == 0 and current_button_value:
    # Off -> ToOn
    button._set_value(3)
  elif prev_button_value == 1 and not current_button_value:
    # On -> ToOff
    button._set_value(2)
  elif prev_button_value == 2:
    if current_button_value:
      # ToOff -> ToOn
      button._set_value(3)
    else:
      # ToOff -> Off
      button._set_value(0)
  elif prev_button_value == 3:
    if current_button_value:
      # ToOn -> On
      button._set_value(1)
    else:
      # ToOn -> ToOff
      button._set_value(2)


class ButtonState(object):
  """
  Represents the state of a button.

  The defined values for this class are:

    * ``0``; corresponding to the state ``Off``
    * ``1``; corresponding to the state ``On``
    * ``2``; corresponding to the state ``ToOff``
    * ``3``; corresponding to the state ``ToOn``
  """

  def __init__(self, value=0):
    self._value = value

  def __int__(self):
    return self._value

  def __bool__(self):
    """
    :return: ``True`` if the enum corresponds to ``On`` or ``ToOn``; ``False`` otherwise
    """
    if self._value == 1 or self._value == 3:
      return True
    return False

  def __eq__(self, o):
    if isinstance(o, str):
      if o in _btn_state_str_to_enum_map:
        return self._value == _btn_state_str_to_enum_map[o]
      return False
    else:
      return self._value == o

  def __ne__(self, o):
    if isinstance(o, str):
      if o in _btn_state_str_to_enum_map:
        return self._value != _btn_state_str_to_enum_map[o]
      return False
    else:
      return self._value != o

  def __str__(self):
    return self.__repr__()

  def __repr__(self):
    if self._value == 0:
      return 'Off'
    elif self._value == 1:
      return 'On'
    elif self._value == 2:
      return 'ToOff'
    elif self._value == 3:
      return 'ToOn'
    else:
      return super().__repr__()

  def _set_value(self, value):
    value = int(value)
    if value < 0 or value > 3:
      raise ValueError("value not 0 <= x <= 3")
    self._value = value


class MobileIOState(object):

  def __init__(self):
    self._buttons = [ButtonState() for _ in range(8)]
    self._axes = [0.0] * 8

  def __repr__(self):
    return _state_repr('MobileIOState', self)

  @property
  def buttons(self):
    """
    Retrieve a list of all button states
    """
    return self._buttons

  @property
  def axes(self):
    """
    Retrieve a list of all axis values
    """
    return self._axes

  def get_button_diff(self, index):
    """
    Returns the diff state of the chosen button
    """
    if index < 1 or index > 8:
      raise IndexError("index must be between 1 and 8")
    return self._buttons[index - 1]

  def get_button_state(self, index):
    """
    Returns a boolean representing if the chosen button is pressed or not
    """
    if index < 1 or index > 8:
      raise IndexError("index must be between 1 and 8")
    return bool(self._buttons[index - 1])

  def get_axis_state(self, index):
    """
    Returns the value of the selected axis
    """
    if index < 1 or index > 8:
      raise IndexError("index must be between 1 and 8")
    return self._axes[index - 1]


class MobileIO(object):
  """
  Wrapper around a mobile IO controller
  """

  __slots__ = (
    '_group', '_cmd', '_fbk', '_state')

  def __init__(self, group):
    self._group = group
    self._cmd = GroupCommand(group.size)
    self._fbk = GroupFeedback(group.size)
    self._state = MobileIOState()

  def __repr__(self):
    return _state_repr('MobileIO', self)

  def update(self, timeout_ms=None):
    """
    Updates the button and axis values and state. Returns ``False`` if feedback could not be received.

    :rtype:  bool
    :return: ``True`` on success; ``False`` otherwise
    """
    fbk = self._fbk
    if self._group.get_next_feedback(timeout_ms=timeout_ms, reuse_fbk=fbk) is None:
      return False

    current_button_state = self._state._buttons
    current_slider_state = self._state._axes
    for i in range(8):
      in_idx = i+1

      # Button update
      _transition_button_state(fbk.io.b.get_int(in_idx), current_button_state[i])

      # Slider update
      io_a = fbk.io.a
      if io_a.has_int(in_idx):
        current_slider_state[i] = float(io_a.get_int(in_idx))
      elif io_a.has_float(in_idx):
        current_slider_state[i] = io_a.get_float(in_idx)[0]
      else:
        current_slider_state[i] = None

    return True

  def get_button_diff(self, index):
    """
    Retrieve the current diff of the specified button.

    Note that this method uses 1-indexing.

    :param index: The index of the button (indices starting at 1).
    :type index:  int

    :rtype: ButtonState
    """
    return self._state.get_button_diff(index)

  def get_button_state(self, index):
    """
    Retrieve the current (pressed/unpressed) state of the specified button.

    Note that this method uses 1-indexing.

    :param index: The index of the button (indices starting at 1).
    :type index:  int

    :rtype: bool
    """
    return self._state.get_button_state(index)

  def get_axis_state(self, index):
    """
    Retrieve the current state of the specified axis.

    Note that this method uses 1-indexing.

    :param index: The index of the axis (indices starting at 1).
    :type index:  int

    :rtype: float
    """
    return self._state.get_axis_state(index)

  @property
  def state(self):
    """
    Retrieve the current state of all buttons and sliders

    :rtype: MobileIOState
    """
    return self._state

  def set_snap(self, slider, value):
    """
    Set the snap position on a slider.

    Note that this method uses 1-indexing.

    :param slider: The index of the slider to modify (indices starting at 1)
    :type slider:  int

    :param value: The value to set. Note that this will be converted to a `float`.
    :type value:  int, float

    :rtype: bool
    :return: ``True`` if the device received the command and successfully sent an acknowledgement; ``False`` otherwise.
    """
    self._cmd.io.a.set_float(slider, value)
    return self._group.send_command_with_acknowledgement(self._cmd)

  def set_axis_value(self, slider, value):
    """
    Set the position on a slider.

    Note that this method uses 1-indexing.

    :param slider: The index of the slider to modify (indices starting at 1)
    :type slider:  int

    :param value: The value to set. Note that this will be converted to a `float`.
    :type value:  int, float

    :rtype: bool
    :return: ``True`` if the device received the command and successfully sent an acknowledgement; ``False`` otherwise.
    """
    self._cmd.io.f.set_float(slider, value)
    return self._group.send_command_with_acknowledgement(self._cmd)

  def set_button_mode(self, button, value):
    """
    Set the mode of the specified button to momentary or toggle.

    Note that this method uses 1-indexing.

    :param button: The index of the button to modify (indices starting at 1).
    :type button:  int

    :param value: The value to set.
                  Momentary corresponds to ``0`` (default) and toggle corresponds to ``1``.
                  This parameter allows the strings 'momentary' and 'toggle'
    :type value:  int, str

    :raises ValueError: If `value` is an unrecognized string

    :rtype: bool
    :return: ``True`` if the device received the command and successfully sent an acknowledgement; ``False`` otherwise.
    """
    if isinstance(value, str):
      if value == 'momentary':
        value = 0
      elif value == 'toggle':
        value = 1
      else:
        raise ValueError("Unrecognized string value {0}".format(value))
    self._cmd.io.b.set_int(button, value)
    return self._group.send_command_with_acknowledgement(self._cmd)

  def set_button_output(self, button, value):
    """
    Set the button output behavior (indicator ring on or off).

    Note that this method uses 1-indexing.

    :param button: The index of the button to modify (indices starting at 1).
    :type button:  int

    :param value: The value to set.
                  To illuminate the indicator ring, use ``1``. To hide it, use ``0``.
    :type value:  int

    :rtype: bool
    :return: ``True`` if the device received the command and successfully sent an acknowledgement; ``False`` otherwise.
    """
    self._cmd.io.e.set_int(button, value)
    return self._group.send_command_with_acknowledgement(self._cmd)

  def set_led_color(self, color, blocking=True):
    """
    Set the edge led color

    :param color: The color to which the edge color is set. Certain strings are recognized as colors.
                  Reference :py:attr:`~hebi.GroupCommand.led` for a complete list of allowed colors.
    :type color:  int, str

    :param blocking: If ``True``, block for acknowledgement from the device. Otherwise, return as quickly as possible.
    :type blocking:  bool

    :rtype: bool
    :return: ``True`` if the device received the command and successfully sent an acknowledgement; ``False`` otherwise.
    """
    self._cmd.led.color = color
    if blocking:
      return self._group.send_command_with_acknowledgement(self._cmd)
    return self._group.send_command(self._cmd)

  def set_text(self, message, blocking=True):
    """
    Append a message to the text display.

    :param message: The string to append to the display
    :type message:  str

    :param blocking: If ``True``, block for acknowledgement from the device. Otherwise, return as quickly as possible.
    :type blocking:  bool

    :rtype: bool
    :return: ``True`` if the device received the command and successfully sent an acknowledgement; ``False`` otherwise.
    """
    self._cmd.append_log = message
    if blocking:
      return self._group.send_command_with_acknowledgement(self._cmd)
    return self._group.send_command(self._cmd)

  def clear_text(self, blocking=True):
    """
    Clear the text display.

    :param blocking: If ``True``, block for acknowledgement from the device. Otherwise, return as quickly as possible.
    :type blocking:  bool

    :rtype: bool
    :return: ``True`` if the device received the command and successfully sent an acknowledgement; ``False`` otherwise.
    """
    self._cmd.clear_log = True
    if blocking:
      return self._group.send_command_with_acknowledgement(self._cmd)
    return self._group.send_command(self._cmd)

  def send_vibrate(self, blocking=True):
    """
    Send a command to vibrate the device. Note that this feature depends on device support.
    If the device does not support programmatic vibrating, then this will be a no-op.

    :param blocking: If ``True``, block for acknowledgement from the device. Otherwise, return as quickly as possible.
    :type blocking:  bool

    :rtype: bool
    :return: ``True`` if the device received the command and successfully sent an acknowledgement; ``False`` otherwise.
    """
    self._cmd.effort = 1
    if blocking:
      return self._group.send_command_with_acknowledgement(self._cmd)
    return self._group.send_command(self._cmd)

  def get_last_feedback(self):
    """
    Retrieve the last receieved feedback from the mobile IO device.

    :rtype: hebi._internal.ffi._message_types.Feedback
    """
    return self._fbk[0]

  @property
  def position(self):
    """
    Retrieve the AR position of the mobile IO device.

    Note that this will only return valid data if the device supports an AR framework.

    :rtype: numpy.ndarray
    """
    return self._fbk[0].ar_position

  @property
  def orientation(self):
    """
    Retrieve the AR orientation of the mobile IO device.

    Note that this will only return valid data if the device supports an AR framework.

    :rtype: numpy.ndarray
    """
    return self._fbk[0].ar_orientation
