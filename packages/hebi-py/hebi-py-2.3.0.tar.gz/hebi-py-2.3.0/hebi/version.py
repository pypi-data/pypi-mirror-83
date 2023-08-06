def parse_version(s):
  split = s.split('.')
  if len(split) > 3:
    raise ValueError("Period characters are not allowed in the suffix portion of the version string `{0}`".format(s))
  elif len(split) < 3:
    raise ValueError("Malformed version string `{0}`".format(s))

  import re
  r = re.compile(r"^(\d+)([a-zA-Z_0-9-]+)?$")
  patch_str = split[2]
  patch_parts = r.split(patch_str)
  parts = []
  for entry in patch_parts:
    if entry != '':
      parts.append(entry)

  if len(parts) > 2 or len(parts) == 0:
    raise ValueError(s)
  elif len(parts) == 1:
    return Version(int(split[0]), int(split[1]), int(parts[0]))
  return Version(int(split[0]), int(split[1]), int(parts[0]), parts[1])


class Version(object):
  def __init__(self, maj, min, rev, suffix=None):
    """
    Suffix string must only contain the following:
      * Underscore
      * Hyphen
      * alphabetical character (lower or uppercase) as determined by `[a-zA-Z]
      * numbers as determined by `[0-9]` or `\d`
    
    Note that periods (`.`) are not allowed in the suffix.
    """
    self._major_version = maj
    self._minor_version = min
    self._patch_version = rev
    self._suffix = suffix or ''

  def __str__(self):
    return '{0}.{1}.{2}{3}'.format(self.major_version, self.minor_version, self.patch_version, self.suffix)

  def __repr__(self):
    return 'Version(major: {0}, minor: {1}, patch: {2}, suffix: {3})'.format(self.major_version, self.minor_version, self.patch_version, self.suffix)

  def __eq__(self, o):
    if isinstance(o, Version):
      thiz_suffix = self._suffix or ''
      o_suffix = o._suffix or ''
      return o.major_version == self.major_version and \
      o.minor_version == self.minor_version and \
      o.patch_version == self.patch_version and \
      thiz_suffix == o_suffix
    else:
      return self == parse_version(o)

  def __ne__(self, o):
    if isinstance(o, Version):
      thiz_suffix = self._suffix or ''
      o_suffix = o._suffix or ''
      return o.major_version != self.major_version or \
      o.minor_version != self.minor_version or \
      o.patch_version != self.patch_version or \
      thiz_suffix != o_suffix
    else:
      return self != parse_version(o)

  def __gt__(self, o):
    if isinstance(o, Version):
      if self.major_version > o.major_version:
        return True
      elif self.major_version < o.major_version:
        return False
      elif self.minor_version > o.minor_version:
        return True
      elif self.minor_version < o.minor_version:
        return False
      elif self.patch_version > o.patch_version:
        return True
      elif self.patch_version < o.patch_version:
        return False
      thiz_suffix = self._suffix or ''
      o_suffix = o._suffix or ''
      return thiz_suffix > o_suffix
    else:
      return self > parse_version(o)

  def __lt__(self, o):
    if isinstance(o, Version):
      if self.major_version < o.major_version:
        return True
      elif self.major_version > o.major_version:
        return False
      elif self.minor_version < o.minor_version:
        return True
      elif self.minor_version > o.minor_version:
        return False
      elif self.patch_version < o.patch_version:
        return True
      elif self.patch_version > o.patch_version:
        return False
      thiz_suffix = self._suffix or ''
      o_suffix = o._suffix or ''
      return thiz_suffix < o_suffix
    else:
      return self < parse_version(o)

  @property
  def major_version(self):
    return self._major_version

  @property
  def minor_version(self):
    return self._minor_version

  @property
  def patch_version(self):
    return self._patch_version

  @property
  def suffix(self):
    return self._suffix
  


def py_version():
  return parse_version("2.3.0")


def min_c_api_version():
  return parse_version("2.0.0")


def loaded_c_api_version():
  from ._internal.ffi.loader import _handle
  return _handle.version


if __name__ == "__main__":
  import argparse
  def __disp(txt, vfunc):
    print('{0}: {1}'.format(txt, vfunc()))

  parser = argparse.ArgumentParser()
  parser.add_argument("--min-c-api", help="Show minimum required C API version",
                      default=False, action="store_true")
  parser.add_argument("--py-api", help="Show the version of hebi-py",
                      default=False, action="store_true")
  args = parser.parse_args()
  if args.min_c_api:
    __disp('Minimum C API Version', min_c_api_version)
  if args.py_api:
    __disp('hebi-py Version', py_version)
