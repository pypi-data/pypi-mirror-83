# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#  HEBI Core python API - Copyright 2018 HEBI Robotics
#  See https://hebi.us/softwarelicense for license details
#
# ------------------------------------------------------------------------------


from ctypes import c_size_t, c_char_p, byref
import numpy as np

from .ffi._message_types import GroupFeedback
from .ffi import ctypes_func_defs as api
from .ffi.enums import StatusSuccess
from .ffi.wrappers import UnmanagedObject, WeakReferenceContainer
from .type_utils import decode_string_buffer as decode_str
from .type_utils import create_string_buffer_compat as create_str


class LogFile(UnmanagedObject):
  """
  Represents a file which contains previously recorded group messages.
  """

  __slots__ = ['_beginning_time', '_feedbacks_read', '_next_feedback', '_number_of_modules', '_time', '__weakref__']

  def __calculate_time(self):
    np.subtract(self._next_feedback.receive_time, self._beginning_time, self._time)

  def __read_first_feedback(self):
    feedback = GroupFeedback(self._number_of_modules)
    if api.hebiLogFileGetNextFeedback(self, feedback) != StatusSuccess:
      raise RuntimeError('Log file is corrupt or has no feedback')

    self._next_feedback = feedback
    start_time = self._next_feedback.receive_time.min()

    # Cached arrays
    self._beginning_time = np.array([start_time] * self._number_of_modules)
    self._time = np.empty(self._number_of_modules, np.float64)
    self.__calculate_time()

  def __init__(self, internal):
    """
    This is created internally. Do not instantiate directly.
    """
    super(LogFile, self).__init__(internal, on_delete=api.hebiLogFileRelease)
    self._feedbacks_read = 0
    self._number_of_modules = api.hebiLogFileGetNumberOfModules(internal)
    if self._number_of_modules < 1:
      raise RuntimeError('Log file is corrupt')

    self.__read_first_feedback()

  @property
  def feedback_iterate(self):
    """
    Retrieves an iterator over feedback from the LogFile, sequentially in order from the beginning of the file.

    Note: The object returned from this method is only valid for the duration of the enclosing LogFile (`self`).
    If one attempts to use this iterator after the LogFile has been disposed, an exception will be raised.

    :return: A feedback iterator for this LogFile.
    """
    return LogFileFeedbackIterator(self)

  @property
  def filename(self):
    """
    :return: The file name of the log file.
    :rtype:  str
    """
    str_len = c_size_t(0)
    if api.hebiLogFileGetFileName(self, c_char_p(None), byref(str_len)) != StatusSuccess:
      return None

    str_buffer = create_str(str_len.value)

    if api.hebiLogFileGetFileName(self, str_buffer, byref(str_len)) != StatusSuccess:
      return None

    return decode_str(str_buffer.value)

  @property
  def number_of_modules(self):
    """
    :return: The number of modules in the group.
    :rtype:  int
    """
    return self._number_of_modules

  def get_next_feedback(self, reuse_fbk=None):
    """
    Retrieves the next group feedback from the log file, if any exists.
    This function acts as a forward sequential iterator over the data
    in the file. Each subsequent call to this function moves farther
    into the file. When the end of the file is reached, all subsequent calls
    to this function returns ``None``

    **Warning:** any preexisting data in the provided Feedback object is erased.

    :param reuse_fbk: An optional parameter which can be used to reuse
                      an existing :class:`~hebi.GroupFeedback` instance.
                      It is recommended to provide this parameter inside a
                      repetitive loop, as reusing feedback instances results
                      in substantially
                      fewer heap allocations.

    :return: The most recent feedback, provided one is available.
             ``None`` is returned if there is no available feedback.
    :rtype:  TimedGroupFeedback
    """
    next_fbk = self._next_feedback

    if next_fbk is None:
      return None

    t = self._time.copy()
    if reuse_fbk is not None:
      ret = TimedGroupFeedback(reuse_fbk, t)
    else:
      ret = TimedGroupFeedback(GroupFeedback(next_fbk.size), t)

    ret.copy_from(next_fbk)
    if api.hebiLogFileGetNextFeedback(self, next_fbk) != StatusSuccess:
      self._next_feedback = None
    else:
      self.__calculate_time()

    self._feedbacks_read += 1
    return ret


class LogFileFeedbackIterator(object):
  """
  Iterator for feedback in a log file
  """

  __slots__ = ['_current_feedback', '_log_file']

  def __init__(self, logfile):
    self._log_file = WeakReferenceContainer(logfile)
    self._current_feedback = GroupFeedback(logfile.number_of_modules)
    self.__get_next()

  def __iter__(self):
    return self

  def __next__(self):
    if not self.__has_current():
      raise StopIteration()
    ret = self._current_feedback
    self.__get_next()
    return ret

  def __get_next(self):
    logfile = self._log_file._get_ref()
    self._current_feedback = logfile.get_next_feedback(reuse_fbk=self._current_feedback)

  def __has_current(self):
    return self._current_feedback is not None


class TimedGroupFeedback(GroupFeedback):
  """
  A feedback object with a time field. Represents feedback returned
  from a log file. This class inherits all fields and functionality from :class:`~hebi.GroupFeedback`.
  """

  __slots__ = ['_time']

  def __init__(self, group_feedback, time):
    super(TimedGroupFeedback, self).__init__(group_feedback.size, group_feedback)
    self._time = time

  @property
  def time(self):
    """
    :return: The time, relative to the start of the log file (in seconds).
    :rtype:  numpy.ndarray
    """
    return self._time.copy()
