import ctypes
from .ctypes_defs import HebiMacAddress, HebiVector3f, HebiQuaternionf, HebiRobotModelElementMetadata, HebiRobotModelElementTopology, HebiHighResAngleStruct, HebiIoBankPinStruct, HebiCommandRef, HebiCommandMetadata, HebiFeedbackRef, HebiFeedbackMetadata, HebiInfoRef, HebiInfoMetadata


def populate_hebi_funcs(lib):
  """
  Populates all API functions from the HEBI Core library
  """
  
  if hasattr(lib, 'hebiLookupCreate'):
    lib_func = getattr(lib, 'hebiLookupCreate')
    lib_func.argtypes = [ctypes.POINTER(ctypes.c_char_p),ctypes.c_size_t]
    lib_func.restype = ctypes.c_void_p
  else:
    raise RuntimeWarning('Could not load function hebiLookupCreate')

  if hasattr(lib, 'hebiLookupRelease'):
    lib_func = getattr(lib, 'hebiLookupRelease')
    lib_func.argtypes = [ctypes.c_void_p]
    lib_func.restype = None
  else:
    raise RuntimeWarning('Could not load function hebiLookupRelease')

  if hasattr(lib, 'hebiLookupSetLookupFrequencyHz'):
    lib_func = getattr(lib, 'hebiLookupSetLookupFrequencyHz')
    lib_func.argtypes = [ctypes.c_void_p,ctypes.c_double]
    lib_func.restype = ctypes.c_int
  else:
    raise RuntimeWarning('Could not load function hebiLookupSetLookupFrequencyHz')

  if hasattr(lib, 'hebiLookupGetLookupFrequencyHz'):
    lib_func = getattr(lib, 'hebiLookupGetLookupFrequencyHz')
    lib_func.argtypes = [ctypes.c_void_p]
    lib_func.restype = ctypes.c_double
  else:
    raise RuntimeWarning('Could not load function hebiLookupGetLookupFrequencyHz')

  if hasattr(lib, 'hebiCreateLookupEntryList'):
    lib_func = getattr(lib, 'hebiCreateLookupEntryList')
    lib_func.argtypes = [ctypes.c_void_p]
    lib_func.restype = ctypes.c_void_p
  else:
    raise RuntimeWarning('Could not load function hebiCreateLookupEntryList')

  if hasattr(lib, 'hebiLookupEntryListGetSize'):
    lib_func = getattr(lib, 'hebiLookupEntryListGetSize')
    lib_func.argtypes = [ctypes.c_void_p]
    lib_func.restype = ctypes.c_size_t
  else:
    raise RuntimeWarning('Could not load function hebiLookupEntryListGetSize')

  if hasattr(lib, 'hebiLookupEntryListGetName'):
    lib_func = getattr(lib, 'hebiLookupEntryListGetName')
    lib_func.argtypes = [ctypes.c_void_p,ctypes.c_size_t,ctypes.c_char_p,ctypes.POINTER(ctypes.c_size_t)]
    lib_func.restype = ctypes.c_int
  else:
    raise RuntimeWarning('Could not load function hebiLookupEntryListGetName')

  if hasattr(lib, 'hebiLookupEntryListGetFamily'):
    lib_func = getattr(lib, 'hebiLookupEntryListGetFamily')
    lib_func.argtypes = [ctypes.c_void_p,ctypes.c_size_t,ctypes.c_char_p,ctypes.POINTER(ctypes.c_size_t)]
    lib_func.restype = ctypes.c_int
  else:
    raise RuntimeWarning('Could not load function hebiLookupEntryListGetFamily')

  if hasattr(lib, 'hebiLookupEntryListGetMacAddress'):
    lib_func = getattr(lib, 'hebiLookupEntryListGetMacAddress')
    lib_func.argtypes = [ctypes.c_void_p,ctypes.c_size_t,ctypes.POINTER(HebiMacAddress)]
    lib_func.restype = ctypes.c_int
  else:
    raise RuntimeWarning('Could not load function hebiLookupEntryListGetMacAddress')

  if hasattr(lib, 'hebiLookupEntryListRelease'):
    lib_func = getattr(lib, 'hebiLookupEntryListRelease')
    lib_func.argtypes = [ctypes.c_void_p]
    lib_func.restype = None
  else:
    raise RuntimeWarning('Could not load function hebiLookupEntryListRelease')

  if hasattr(lib, 'hebiGroupCreateImitation'):
    lib_func = getattr(lib, 'hebiGroupCreateImitation')
    lib_func.argtypes = [ctypes.c_size_t]
    lib_func.restype = ctypes.c_void_p
  else:
    raise RuntimeWarning('Could not load function hebiGroupCreateImitation')

  if hasattr(lib, 'hebiGroupCreateFromMacs'):
    lib_func = getattr(lib, 'hebiGroupCreateFromMacs')
    lib_func.argtypes = [ctypes.c_void_p,ctypes.POINTER(ctypes.POINTER(HebiMacAddress)),ctypes.c_size_t,ctypes.c_int32]
    lib_func.restype = ctypes.c_void_p
  else:
    raise RuntimeWarning('Could not load function hebiGroupCreateFromMacs')

  if hasattr(lib, 'hebiGroupCreateFromNames'):
    lib_func = getattr(lib, 'hebiGroupCreateFromNames')
    lib_func.argtypes = [ctypes.c_void_p,ctypes.POINTER(ctypes.c_char_p),ctypes.c_size_t,ctypes.POINTER(ctypes.c_char_p),ctypes.c_size_t,ctypes.c_int32]
    lib_func.restype = ctypes.c_void_p
  else:
    raise RuntimeWarning('Could not load function hebiGroupCreateFromNames')

  if hasattr(lib, 'hebiGroupCreateFromFamily'):
    lib_func = getattr(lib, 'hebiGroupCreateFromFamily')
    lib_func.argtypes = [ctypes.c_void_p,ctypes.c_char_p,ctypes.c_int32]
    lib_func.restype = ctypes.c_void_p
  else:
    raise RuntimeWarning('Could not load function hebiGroupCreateFromFamily')

  if hasattr(lib, 'hebiGroupCreateConnectedFromMac'):
    lib_func = getattr(lib, 'hebiGroupCreateConnectedFromMac')
    lib_func.argtypes = [ctypes.c_void_p,ctypes.POINTER(HebiMacAddress),ctypes.c_int32]
    lib_func.restype = ctypes.c_void_p
  else:
    raise RuntimeWarning('Could not load function hebiGroupCreateConnectedFromMac')

  if hasattr(lib, 'hebiGroupCreateConnectedFromName'):
    lib_func = getattr(lib, 'hebiGroupCreateConnectedFromName')
    lib_func.argtypes = [ctypes.c_void_p,ctypes.c_char_p,ctypes.c_char_p,ctypes.c_int32]
    lib_func.restype = ctypes.c_void_p
  else:
    raise RuntimeWarning('Could not load function hebiGroupCreateConnectedFromName')

  if hasattr(lib, 'hebiGroupGetSize'):
    lib_func = getattr(lib, 'hebiGroupGetSize')
    lib_func.argtypes = [ctypes.c_void_p]
    lib_func.restype = ctypes.c_size_t
  else:
    raise RuntimeWarning('Could not load function hebiGroupGetSize')

  if hasattr(lib, 'hebiGroupSendCommandWithAcknowledgement'):
    lib_func = getattr(lib, 'hebiGroupSendCommandWithAcknowledgement')
    lib_func.argtypes = [ctypes.c_void_p,ctypes.c_void_p,ctypes.c_int32]
    lib_func.restype = ctypes.c_int
  else:
    raise RuntimeWarning('Could not load function hebiGroupSendCommandWithAcknowledgement')

  if hasattr(lib, 'hebiGroupSendCommand'):
    lib_func = getattr(lib, 'hebiGroupSendCommand')
    lib_func.argtypes = [ctypes.c_void_p,ctypes.c_void_p]
    lib_func.restype = ctypes.c_int
  else:
    raise RuntimeWarning('Could not load function hebiGroupSendCommand')

  if hasattr(lib, 'hebiGroupSetCommandLifetime'):
    lib_func = getattr(lib, 'hebiGroupSetCommandLifetime')
    lib_func.argtypes = [ctypes.c_void_p,ctypes.c_int32]
    lib_func.restype = ctypes.c_int
  else:
    raise RuntimeWarning('Could not load function hebiGroupSetCommandLifetime')

  if hasattr(lib, 'hebiGroupGetCommandLifetime'):
    lib_func = getattr(lib, 'hebiGroupGetCommandLifetime')
    lib_func.argtypes = [ctypes.c_void_p]
    lib_func.restype = ctypes.c_int32
  else:
    raise RuntimeWarning('Could not load function hebiGroupGetCommandLifetime')

  if hasattr(lib, 'hebiGroupSetFeedbackFrequencyHz'):
    lib_func = getattr(lib, 'hebiGroupSetFeedbackFrequencyHz')
    lib_func.argtypes = [ctypes.c_void_p,ctypes.c_float]
    lib_func.restype = ctypes.c_int
  else:
    raise RuntimeWarning('Could not load function hebiGroupSetFeedbackFrequencyHz')

  if hasattr(lib, 'hebiGroupGetFeedbackFrequencyHz'):
    lib_func = getattr(lib, 'hebiGroupGetFeedbackFrequencyHz')
    lib_func.argtypes = [ctypes.c_void_p]
    lib_func.restype = ctypes.c_float
  else:
    raise RuntimeWarning('Could not load function hebiGroupGetFeedbackFrequencyHz')

  if hasattr(lib, 'hebiGroupRegisterFeedbackHandler'):
    lib_func = getattr(lib, 'hebiGroupRegisterFeedbackHandler')
    lib_func.argtypes = [ctypes.c_void_p,ctypes.CFUNCTYPE(None,ctypes.c_void_p,ctypes.c_void_p),ctypes.c_void_p]
    lib_func.restype = ctypes.c_int
  else:
    raise RuntimeWarning('Could not load function hebiGroupRegisterFeedbackHandler')

  if hasattr(lib, 'hebiGroupClearFeedbackHandlers'):
    lib_func = getattr(lib, 'hebiGroupClearFeedbackHandlers')
    lib_func.argtypes = [ctypes.c_void_p]
    lib_func.restype = None
  else:
    raise RuntimeWarning('Could not load function hebiGroupClearFeedbackHandlers')

  if hasattr(lib, 'hebiGroupSendFeedbackRequest'):
    lib_func = getattr(lib, 'hebiGroupSendFeedbackRequest')
    lib_func.argtypes = [ctypes.c_void_p]
    lib_func.restype = ctypes.c_int
  else:
    raise RuntimeWarning('Could not load function hebiGroupSendFeedbackRequest')

  if hasattr(lib, 'hebiGroupGetNextFeedback'):
    lib_func = getattr(lib, 'hebiGroupGetNextFeedback')
    lib_func.argtypes = [ctypes.c_void_p,ctypes.c_void_p,ctypes.c_int32]
    lib_func.restype = ctypes.c_int
  else:
    raise RuntimeWarning('Could not load function hebiGroupGetNextFeedback')

  if hasattr(lib, 'hebiGroupRequestInfo'):
    lib_func = getattr(lib, 'hebiGroupRequestInfo')
    lib_func.argtypes = [ctypes.c_void_p,ctypes.c_void_p,ctypes.c_int32]
    lib_func.restype = ctypes.c_int
  else:
    raise RuntimeWarning('Could not load function hebiGroupRequestInfo')

  if hasattr(lib, 'hebiGroupStartLog'):
    lib_func = getattr(lib, 'hebiGroupStartLog')
    lib_func.argtypes = [ctypes.c_void_p,ctypes.c_char_p,ctypes.c_char_p,ctypes.POINTER(ctypes.c_void_p)]
    lib_func.restype = ctypes.c_int
  else:
    raise RuntimeWarning('Could not load function hebiGroupStartLog')

  if hasattr(lib, 'hebiGroupStopLog'):
    lib_func = getattr(lib, 'hebiGroupStopLog')
    lib_func.argtypes = [ctypes.c_void_p]
    lib_func.restype = ctypes.c_void_p
  else:
    raise RuntimeWarning('Could not load function hebiGroupStopLog')

  if hasattr(lib, 'hebiGroupRelease'):
    lib_func = getattr(lib, 'hebiGroupRelease')
    lib_func.argtypes = [ctypes.c_void_p]
    lib_func.restype = None
  else:
    raise RuntimeWarning('Could not load function hebiGroupRelease')

  if hasattr(lib, 'hebiGroupCommandCreate'):
    lib_func = getattr(lib, 'hebiGroupCommandCreate')
    lib_func.argtypes = [ctypes.c_size_t]
    lib_func.restype = ctypes.c_void_p
  else:
    raise RuntimeWarning('Could not load function hebiGroupCommandCreate')

  if hasattr(lib, 'hebiGroupCommandGetSize'):
    lib_func = getattr(lib, 'hebiGroupCommandGetSize')
    lib_func.argtypes = [ctypes.c_void_p]
    lib_func.restype = ctypes.c_size_t
  else:
    raise RuntimeWarning('Could not load function hebiGroupCommandGetSize')

  if hasattr(lib, 'hebiGroupCommandReadGains'):
    lib_func = getattr(lib, 'hebiGroupCommandReadGains')
    lib_func.argtypes = [ctypes.c_void_p,ctypes.c_char_p]
    lib_func.restype = ctypes.c_int
  else:
    raise RuntimeWarning('Could not load function hebiGroupCommandReadGains')

  if hasattr(lib, 'hebiGroupCommandWriteGains'):
    lib_func = getattr(lib, 'hebiGroupCommandWriteGains')
    lib_func.argtypes = [ctypes.c_void_p,ctypes.c_char_p]
    lib_func.restype = ctypes.c_int
  else:
    raise RuntimeWarning('Could not load function hebiGroupCommandWriteGains')

  if hasattr(lib, 'hebiGroupCommandReadSafetyParameters'):
    lib_func = getattr(lib, 'hebiGroupCommandReadSafetyParameters')
    lib_func.argtypes = [ctypes.c_void_p,ctypes.c_char_p]
    lib_func.restype = ctypes.c_int
  else:
    raise RuntimeWarning('Could not load function hebiGroupCommandReadSafetyParameters')

  if hasattr(lib, 'hebiGroupCommandWriteSafetyParameters'):
    lib_func = getattr(lib, 'hebiGroupCommandWriteSafetyParameters')
    lib_func.argtypes = [ctypes.c_void_p,ctypes.c_char_p]
    lib_func.restype = ctypes.c_int
  else:
    raise RuntimeWarning('Could not load function hebiGroupCommandWriteSafetyParameters')

  if hasattr(lib, 'hebiGroupCommandGetModuleCommand'):
    lib_func = getattr(lib, 'hebiGroupCommandGetModuleCommand')
    lib_func.argtypes = [ctypes.c_void_p,ctypes.c_size_t]
    lib_func.restype = ctypes.c_void_p
  else:
    raise RuntimeWarning('Could not load function hebiGroupCommandGetModuleCommand')

  if hasattr(lib, 'hebiGroupCommandCopy'):
    lib_func = getattr(lib, 'hebiGroupCommandCopy')
    lib_func.argtypes = [ctypes.c_void_p,ctypes.c_void_p]
    lib_func.restype = ctypes.c_int
  else:
    raise RuntimeWarning('Could not load function hebiGroupCommandCopy')

  if hasattr(lib, 'hebiGroupCommandClear'):
    lib_func = getattr(lib, 'hebiGroupCommandClear')
    lib_func.argtypes = [ctypes.c_void_p]
    lib_func.restype = None
  else:
    raise RuntimeWarning('Could not load function hebiGroupCommandClear')

  if hasattr(lib, 'hebiGroupCommandRelease'):
    lib_func = getattr(lib, 'hebiGroupCommandRelease')
    lib_func.argtypes = [ctypes.c_void_p]
    lib_func.restype = None
  else:
    raise RuntimeWarning('Could not load function hebiGroupCommandRelease')

  if hasattr(lib, 'hebiGroupFeedbackCreate'):
    lib_func = getattr(lib, 'hebiGroupFeedbackCreate')
    lib_func.argtypes = [ctypes.c_size_t]
    lib_func.restype = ctypes.c_void_p
  else:
    raise RuntimeWarning('Could not load function hebiGroupFeedbackCreate')

  if hasattr(lib, 'hebiGroupFeedbackGetSize'):
    lib_func = getattr(lib, 'hebiGroupFeedbackGetSize')
    lib_func.argtypes = [ctypes.c_void_p]
    lib_func.restype = ctypes.c_size_t
  else:
    raise RuntimeWarning('Could not load function hebiGroupFeedbackGetSize')

  if hasattr(lib, 'hebiGroupFeedbackGetModuleFeedback'):
    lib_func = getattr(lib, 'hebiGroupFeedbackGetModuleFeedback')
    lib_func.argtypes = [ctypes.c_void_p,ctypes.c_size_t]
    lib_func.restype = ctypes.c_void_p
  else:
    raise RuntimeWarning('Could not load function hebiGroupFeedbackGetModuleFeedback')

  if hasattr(lib, 'hebiGroupFeedbackCopy'):
    lib_func = getattr(lib, 'hebiGroupFeedbackCopy')
    lib_func.argtypes = [ctypes.c_void_p,ctypes.c_void_p]
    lib_func.restype = ctypes.c_int
  else:
    raise RuntimeWarning('Could not load function hebiGroupFeedbackCopy')

  if hasattr(lib, 'hebiGroupFeedbackClear'):
    lib_func = getattr(lib, 'hebiGroupFeedbackClear')
    lib_func.argtypes = [ctypes.c_void_p]
    lib_func.restype = None
  else:
    raise RuntimeWarning('Could not load function hebiGroupFeedbackClear')

  if hasattr(lib, 'hebiGroupFeedbackRelease'):
    lib_func = getattr(lib, 'hebiGroupFeedbackRelease')
    lib_func.argtypes = [ctypes.c_void_p]
    lib_func.restype = None
  else:
    raise RuntimeWarning('Could not load function hebiGroupFeedbackRelease')

  if hasattr(lib, 'hebiGroupInfoCreate'):
    lib_func = getattr(lib, 'hebiGroupInfoCreate')
    lib_func.argtypes = [ctypes.c_size_t]
    lib_func.restype = ctypes.c_void_p
  else:
    raise RuntimeWarning('Could not load function hebiGroupInfoCreate')

  if hasattr(lib, 'hebiGroupInfoGetSize'):
    lib_func = getattr(lib, 'hebiGroupInfoGetSize')
    lib_func.argtypes = [ctypes.c_void_p]
    lib_func.restype = ctypes.c_size_t
  else:
    raise RuntimeWarning('Could not load function hebiGroupInfoGetSize')

  if hasattr(lib, 'hebiGroupInfoWriteGains'):
    lib_func = getattr(lib, 'hebiGroupInfoWriteGains')
    lib_func.argtypes = [ctypes.c_void_p,ctypes.c_char_p]
    lib_func.restype = ctypes.c_int
  else:
    raise RuntimeWarning('Could not load function hebiGroupInfoWriteGains')

  if hasattr(lib, 'hebiGroupInfoWriteSafetyParameters'):
    lib_func = getattr(lib, 'hebiGroupInfoWriteSafetyParameters')
    lib_func.argtypes = [ctypes.c_void_p,ctypes.c_char_p]
    lib_func.restype = ctypes.c_int
  else:
    raise RuntimeWarning('Could not load function hebiGroupInfoWriteSafetyParameters')

  if hasattr(lib, 'hebiGroupInfoGetModuleInfo'):
    lib_func = getattr(lib, 'hebiGroupInfoGetModuleInfo')
    lib_func.argtypes = [ctypes.c_void_p,ctypes.c_size_t]
    lib_func.restype = ctypes.c_void_p
  else:
    raise RuntimeWarning('Could not load function hebiGroupInfoGetModuleInfo')

  if hasattr(lib, 'hebiGroupInfoCopy'):
    lib_func = getattr(lib, 'hebiGroupInfoCopy')
    lib_func.argtypes = [ctypes.c_void_p,ctypes.c_void_p]
    lib_func.restype = ctypes.c_int
  else:
    raise RuntimeWarning('Could not load function hebiGroupInfoCopy')

  if hasattr(lib, 'hebiGroupInfoClear'):
    lib_func = getattr(lib, 'hebiGroupInfoClear')
    lib_func.argtypes = [ctypes.c_void_p]
    lib_func.restype = None
  else:
    raise RuntimeWarning('Could not load function hebiGroupInfoClear')

  if hasattr(lib, 'hebiGroupInfoRelease'):
    lib_func = getattr(lib, 'hebiGroupInfoRelease')
    lib_func.argtypes = [ctypes.c_void_p]
    lib_func.restype = None
  else:
    raise RuntimeWarning('Could not load function hebiGroupInfoRelease')

  if hasattr(lib, 'hebiCommandGetString'):
    lib_func = getattr(lib, 'hebiCommandGetString')
    lib_func.argtypes = [ctypes.c_void_p,ctypes.c_int,ctypes.c_char_p,ctypes.POINTER(ctypes.c_size_t)]
    lib_func.restype = ctypes.c_int
  else:
    raise RuntimeWarning('Could not load function hebiCommandGetString')

  if hasattr(lib, 'hebiCommandSetString'):
    lib_func = getattr(lib, 'hebiCommandSetString')
    lib_func.argtypes = [ctypes.c_void_p,ctypes.c_int,ctypes.c_char_p,ctypes.POINTER(ctypes.c_size_t)]
    lib_func.restype = None
  else:
    raise RuntimeWarning('Could not load function hebiCommandSetString')

  if hasattr(lib, 'hebiCommandGetReference'):
    lib_func = getattr(lib, 'hebiCommandGetReference')
    lib_func.argtypes = [ctypes.c_void_p,ctypes.POINTER(HebiCommandRef)]
    lib_func.restype = None
  else:
    raise RuntimeWarning('Could not load function hebiCommandGetReference')

  if hasattr(lib, 'hebiCommandGetMetadata'):
    lib_func = getattr(lib, 'hebiCommandGetMetadata')
    lib_func.argtypes = [ctypes.POINTER(HebiCommandMetadata)]
    lib_func.restype = None
  else:
    raise RuntimeWarning('Could not load function hebiCommandGetMetadata')

  if hasattr(lib, 'hebiFeedbackGetReference'):
    lib_func = getattr(lib, 'hebiFeedbackGetReference')
    lib_func.argtypes = [ctypes.c_void_p,ctypes.POINTER(HebiFeedbackRef)]
    lib_func.restype = None
  else:
    raise RuntimeWarning('Could not load function hebiFeedbackGetReference')

  if hasattr(lib, 'hebiFeedbackGetMetadata'):
    lib_func = getattr(lib, 'hebiFeedbackGetMetadata')
    lib_func.argtypes = [ctypes.POINTER(HebiFeedbackMetadata)]
    lib_func.restype = None
  else:
    raise RuntimeWarning('Could not load function hebiFeedbackGetMetadata')

  if hasattr(lib, 'hebiInfoGetString'):
    lib_func = getattr(lib, 'hebiInfoGetString')
    lib_func.argtypes = [ctypes.c_void_p,ctypes.c_int,ctypes.c_char_p,ctypes.POINTER(ctypes.c_size_t)]
    lib_func.restype = ctypes.c_int
  else:
    raise RuntimeWarning('Could not load function hebiInfoGetString')

  if hasattr(lib, 'hebiInfoGetReference'):
    lib_func = getattr(lib, 'hebiInfoGetReference')
    lib_func.argtypes = [ctypes.c_void_p,ctypes.POINTER(HebiInfoRef)]
    lib_func.restype = None
  else:
    raise RuntimeWarning('Could not load function hebiInfoGetReference')

  if hasattr(lib, 'hebiInfoGetMetadata'):
    lib_func = getattr(lib, 'hebiInfoGetMetadata')
    lib_func.argtypes = [ctypes.POINTER(HebiInfoMetadata)]
    lib_func.restype = None
  else:
    raise RuntimeWarning('Could not load function hebiInfoGetMetadata')

  if hasattr(lib, 'hebiRobotModelElementCreateJoint'):
    lib_func = getattr(lib, 'hebiRobotModelElementCreateJoint')
    lib_func.argtypes = [ctypes.c_int]
    lib_func.restype = ctypes.c_void_p
  else:
    raise RuntimeWarning('Could not load function hebiRobotModelElementCreateJoint')

  if hasattr(lib, 'hebiRobotModelElementCreateRigidBody'):
    lib_func = getattr(lib, 'hebiRobotModelElementCreateRigidBody')
    lib_func.argtypes = [ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double),ctypes.c_double,ctypes.c_size_t,ctypes.POINTER(ctypes.c_double),ctypes.c_int]
    lib_func.restype = ctypes.c_void_p
  else:
    raise RuntimeWarning('Could not load function hebiRobotModelElementCreateRigidBody')

  if hasattr(lib, 'hebiRobotModelElementCreateEndEffector'):
    lib_func = getattr(lib, 'hebiRobotModelElementCreateEndEffector')
    lib_func.argtypes = [ctypes.c_int,ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double),ctypes.c_double,ctypes.POINTER(ctypes.c_double),ctypes.c_int]
    lib_func.restype = ctypes.c_void_p
  else:
    raise RuntimeWarning('Could not load function hebiRobotModelElementCreateEndEffector')

  if hasattr(lib, 'hebiRobotModelElementCreateActuator'):
    lib_func = getattr(lib, 'hebiRobotModelElementCreateActuator')
    lib_func.argtypes = [ctypes.c_int]
    lib_func.restype = ctypes.c_void_p
  else:
    raise RuntimeWarning('Could not load function hebiRobotModelElementCreateActuator')

  if hasattr(lib, 'hebiRobotModelElementCreateBracket'):
    lib_func = getattr(lib, 'hebiRobotModelElementCreateBracket')
    lib_func.argtypes = [ctypes.c_int]
    lib_func.restype = ctypes.c_void_p
  else:
    raise RuntimeWarning('Could not load function hebiRobotModelElementCreateBracket')

  if hasattr(lib, 'hebiRobotModelElementCreateLink'):
    lib_func = getattr(lib, 'hebiRobotModelElementCreateLink')
    lib_func.argtypes = [ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_double,ctypes.c_double]
    lib_func.restype = ctypes.c_void_p
  else:
    raise RuntimeWarning('Could not load function hebiRobotModelElementCreateLink')

  if hasattr(lib, 'hebiRobotModelElementRelease'):
    lib_func = getattr(lib, 'hebiRobotModelElementRelease')
    lib_func.argtypes = [ctypes.c_void_p]
    lib_func.restype = None
  else:
    raise RuntimeWarning('Could not load function hebiRobotModelElementRelease')

  if hasattr(lib, 'hebiRobotModelImport'):
    lib_func = getattr(lib, 'hebiRobotModelImport')
    lib_func.argtypes = [ctypes.c_char_p]
    lib_func.restype = ctypes.c_void_p
  else:
    raise RuntimeWarning('Could not load function hebiRobotModelImport')

  if hasattr(lib, 'hebiRobotModelImportBuffer'):
    lib_func = getattr(lib, 'hebiRobotModelImportBuffer')
    lib_func.argtypes = [ctypes.c_char_p,ctypes.c_size_t]
    lib_func.restype = ctypes.c_void_p
  else:
    raise RuntimeWarning('Could not load function hebiRobotModelImportBuffer')

  if hasattr(lib, 'hebiRobotModelGetImportError'):
    lib_func = getattr(lib, 'hebiRobotModelGetImportError')
    lib_func.argtypes = []
    lib_func.restype = ctypes.c_char_p
  else:
    raise RuntimeWarning('Could not load function hebiRobotModelGetImportError')

  if hasattr(lib, 'hebiRobotModelGetImportWarningCount'):
    lib_func = getattr(lib, 'hebiRobotModelGetImportWarningCount')
    lib_func.argtypes = []
    lib_func.restype = ctypes.c_size_t
  else:
    raise RuntimeWarning('Could not load function hebiRobotModelGetImportWarningCount')

  if hasattr(lib, 'hebiRobotModelGetImportWarning'):
    lib_func = getattr(lib, 'hebiRobotModelGetImportWarning')
    lib_func.argtypes = [ctypes.c_size_t]
    lib_func.restype = ctypes.c_char_p
  else:
    raise RuntimeWarning('Could not load function hebiRobotModelGetImportWarning')

  if hasattr(lib, 'hebiRobotModelCreate'):
    lib_func = getattr(lib, 'hebiRobotModelCreate')
    lib_func.argtypes = []
    lib_func.restype = ctypes.c_void_p
  else:
    raise RuntimeWarning('Could not load function hebiRobotModelCreate')

  if hasattr(lib, 'hebiRobotModelSetBaseFrame'):
    lib_func = getattr(lib, 'hebiRobotModelSetBaseFrame')
    lib_func.argtypes = [ctypes.c_void_p,ctypes.POINTER(ctypes.c_double),ctypes.c_int]
    lib_func.restype = ctypes.c_int
  else:
    raise RuntimeWarning('Could not load function hebiRobotModelSetBaseFrame')

  if hasattr(lib, 'hebiRobotModelGetBaseFrame'):
    lib_func = getattr(lib, 'hebiRobotModelGetBaseFrame')
    lib_func.argtypes = [ctypes.c_void_p,ctypes.POINTER(ctypes.c_double),ctypes.c_int]
    lib_func.restype = ctypes.c_int
  else:
    raise RuntimeWarning('Could not load function hebiRobotModelGetBaseFrame')

  if hasattr(lib, 'hebiRobotModelGetNumberOfFrames'):
    lib_func = getattr(lib, 'hebiRobotModelGetNumberOfFrames')
    lib_func.argtypes = [ctypes.c_void_p,ctypes.c_int]
    lib_func.restype = ctypes.c_size_t
  else:
    raise RuntimeWarning('Could not load function hebiRobotModelGetNumberOfFrames')

  if hasattr(lib, 'hebiRobotModelGetNumberOfDoFs'):
    lib_func = getattr(lib, 'hebiRobotModelGetNumberOfDoFs')
    lib_func.argtypes = [ctypes.c_void_p]
    lib_func.restype = ctypes.c_size_t
  else:
    raise RuntimeWarning('Could not load function hebiRobotModelGetNumberOfDoFs')

  if hasattr(lib, 'hebiRobotModelGetNumberOfElements'):
    lib_func = getattr(lib, 'hebiRobotModelGetNumberOfElements')
    lib_func.argtypes = [ctypes.c_void_p]
    lib_func.restype = ctypes.c_size_t
  else:
    raise RuntimeWarning('Could not load function hebiRobotModelGetNumberOfElements')

  if hasattr(lib, 'hebiRobotModelGetElementMetadata'):
    lib_func = getattr(lib, 'hebiRobotModelGetElementMetadata')
    lib_func.argtypes = [ctypes.c_void_p,ctypes.c_size_t,ctypes.POINTER(HebiRobotModelElementMetadata)]
    lib_func.restype = ctypes.c_int
  else:
    raise RuntimeWarning('Could not load function hebiRobotModelGetElementMetadata')

  if hasattr(lib, 'hebiRobotModelAdd'):
    lib_func = getattr(lib, 'hebiRobotModelAdd')
    lib_func.argtypes = [ctypes.c_void_p,ctypes.c_void_p,ctypes.c_size_t,ctypes.c_void_p]
    lib_func.restype = ctypes.c_int
  else:
    raise RuntimeWarning('Could not load function hebiRobotModelAdd')

  if hasattr(lib, 'hebiRobotModelGetForwardKinematics'):
    lib_func = getattr(lib, 'hebiRobotModelGetForwardKinematics')
    lib_func.argtypes = [ctypes.c_void_p,ctypes.c_int,ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double),ctypes.c_int]
    lib_func.restype = ctypes.c_int
  else:
    raise RuntimeWarning('Could not load function hebiRobotModelGetForwardKinematics')

  if hasattr(lib, 'hebiRobotModelGetJacobians'):
    lib_func = getattr(lib, 'hebiRobotModelGetJacobians')
    lib_func.argtypes = [ctypes.c_void_p,ctypes.c_int,ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double),ctypes.c_int]
    lib_func.restype = ctypes.c_int
  else:
    raise RuntimeWarning('Could not load function hebiRobotModelGetJacobians')

  if hasattr(lib, 'hebiRobotModelGetMasses'):
    lib_func = getattr(lib, 'hebiRobotModelGetMasses')
    lib_func.argtypes = [ctypes.c_void_p,ctypes.POINTER(ctypes.c_double)]
    lib_func.restype = ctypes.c_int
  else:
    raise RuntimeWarning('Could not load function hebiRobotModelGetMasses')

  if hasattr(lib, 'hebiRobotModelGetTreeTopology'):
    lib_func = getattr(lib, 'hebiRobotModelGetTreeTopology')
    lib_func.argtypes = [ctypes.c_void_p,ctypes.c_int,ctypes.POINTER(HebiRobotModelElementTopology)]
    lib_func.restype = ctypes.c_int
  else:
    raise RuntimeWarning('Could not load function hebiRobotModelGetTreeTopology')

  if hasattr(lib, 'hebiRobotModelRelease'):
    lib_func = getattr(lib, 'hebiRobotModelRelease')
    lib_func.argtypes = [ctypes.c_void_p]
    lib_func.restype = None
  else:
    raise RuntimeWarning('Could not load function hebiRobotModelRelease')

  if hasattr(lib, 'hebiIKCreate'):
    lib_func = getattr(lib, 'hebiIKCreate')
    lib_func.argtypes = []
    lib_func.restype = ctypes.c_void_p
  else:
    raise RuntimeWarning('Could not load function hebiIKCreate')

  if hasattr(lib, 'hebiIKAddObjectiveEndEffectorPosition'):
    lib_func = getattr(lib, 'hebiIKAddObjectiveEndEffectorPosition')
    lib_func.argtypes = [ctypes.c_void_p,ctypes.c_double,ctypes.c_size_t,ctypes.c_double,ctypes.c_double,ctypes.c_double]
    lib_func.restype = ctypes.c_int
  else:
    raise RuntimeWarning('Could not load function hebiIKAddObjectiveEndEffectorPosition')

  if hasattr(lib, 'hebiIKAddObjectiveEndEffectorSO3'):
    lib_func = getattr(lib, 'hebiIKAddObjectiveEndEffectorSO3')
    lib_func.argtypes = [ctypes.c_void_p,ctypes.c_double,ctypes.c_size_t,ctypes.POINTER(ctypes.c_double),ctypes.c_int]
    lib_func.restype = ctypes.c_int
  else:
    raise RuntimeWarning('Could not load function hebiIKAddObjectiveEndEffectorSO3')

  if hasattr(lib, 'hebiIKAddObjectiveEndEffectorTipAxis'):
    lib_func = getattr(lib, 'hebiIKAddObjectiveEndEffectorTipAxis')
    lib_func.argtypes = [ctypes.c_void_p,ctypes.c_double,ctypes.c_size_t,ctypes.c_double,ctypes.c_double,ctypes.c_double]
    lib_func.restype = ctypes.c_int
  else:
    raise RuntimeWarning('Could not load function hebiIKAddObjectiveEndEffectorTipAxis')

  if hasattr(lib, 'hebiIKAddConstraintJointAngles'):
    lib_func = getattr(lib, 'hebiIKAddConstraintJointAngles')
    lib_func.argtypes = [ctypes.c_void_p,ctypes.c_double,ctypes.c_size_t,ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double)]
    lib_func.restype = ctypes.c_int
  else:
    raise RuntimeWarning('Could not load function hebiIKAddConstraintJointAngles')

  if hasattr(lib, 'hebiIKAddObjectiveCustom'):
    lib_func = getattr(lib, 'hebiIKAddObjectiveCustom')
    lib_func.argtypes = [ctypes.c_void_p,ctypes.c_double,ctypes.c_size_t,ctypes.CFUNCTYPE(None,ctypes.c_void_p,ctypes.c_size_t,ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double)),ctypes.c_void_p]
    lib_func.restype = ctypes.c_int
  else:
    raise RuntimeWarning('Could not load function hebiIKAddObjectiveCustom')

  if hasattr(lib, 'hebiIKClearAll'):
    lib_func = getattr(lib, 'hebiIKClearAll')
    lib_func.argtypes = [ctypes.c_void_p]
    lib_func.restype = None
  else:
    raise RuntimeWarning('Could not load function hebiIKClearAll')

  if hasattr(lib, 'hebiIKSolve'):
    lib_func = getattr(lib, 'hebiIKSolve')
    lib_func.argtypes = [ctypes.c_void_p,ctypes.c_void_p,ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double),ctypes.c_void_p]
    lib_func.restype = ctypes.c_int
  else:
    raise RuntimeWarning('Could not load function hebiIKSolve')

  if hasattr(lib, 'hebiIKRelease'):
    lib_func = getattr(lib, 'hebiIKRelease')
    lib_func.argtypes = [ctypes.c_void_p]
    lib_func.restype = None
  else:
    raise RuntimeWarning('Could not load function hebiIKRelease')

  if hasattr(lib, 'hebiTrajectoryCreateUnconstrainedQp'):
    lib_func = getattr(lib, 'hebiTrajectoryCreateUnconstrainedQp')
    lib_func.argtypes = [ctypes.c_size_t,ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double)]
    lib_func.restype = ctypes.c_void_p
  else:
    raise RuntimeWarning('Could not load function hebiTrajectoryCreateUnconstrainedQp')

  if hasattr(lib, 'hebiTrajectoryRelease'):
    lib_func = getattr(lib, 'hebiTrajectoryRelease')
    lib_func.argtypes = [ctypes.c_void_p]
    lib_func.restype = None
  else:
    raise RuntimeWarning('Could not load function hebiTrajectoryRelease')

  if hasattr(lib, 'hebiTrajectoryGetDuration'):
    lib_func = getattr(lib, 'hebiTrajectoryGetDuration')
    lib_func.argtypes = [ctypes.c_void_p]
    lib_func.restype = ctypes.c_double
  else:
    raise RuntimeWarning('Could not load function hebiTrajectoryGetDuration')

  if hasattr(lib, 'hebiTrajectoryGetState'):
    lib_func = getattr(lib, 'hebiTrajectoryGetState')
    lib_func.argtypes = [ctypes.c_void_p,ctypes.c_double,ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double)]
    lib_func.restype = ctypes.c_int
  else:
    raise RuntimeWarning('Could not load function hebiTrajectoryGetState')

  if hasattr(lib, 'hebiLogFileRelease'):
    lib_func = getattr(lib, 'hebiLogFileRelease')
    lib_func.argtypes = [ctypes.c_void_p]
    lib_func.restype = None
  else:
    raise RuntimeWarning('Could not load function hebiLogFileRelease')

  if hasattr(lib, 'hebiLogFileGetFileName'):
    lib_func = getattr(lib, 'hebiLogFileGetFileName')
    lib_func.argtypes = [ctypes.c_void_p,ctypes.c_char_p,ctypes.POINTER(ctypes.c_size_t)]
    lib_func.restype = ctypes.c_int
  else:
    raise RuntimeWarning('Could not load function hebiLogFileGetFileName')

  if hasattr(lib, 'hebiLogFileOpen'):
    lib_func = getattr(lib, 'hebiLogFileOpen')
    lib_func.argtypes = [ctypes.c_char_p]
    lib_func.restype = ctypes.c_void_p
  else:
    raise RuntimeWarning('Could not load function hebiLogFileOpen')

  if hasattr(lib, 'hebiLogFileGetNumberOfModules'):
    lib_func = getattr(lib, 'hebiLogFileGetNumberOfModules')
    lib_func.argtypes = [ctypes.c_void_p]
    lib_func.restype = ctypes.c_size_t
  else:
    raise RuntimeWarning('Could not load function hebiLogFileGetNumberOfModules')

  if hasattr(lib, 'hebiLogFileGetNextFeedback'):
    lib_func = getattr(lib, 'hebiLogFileGetNextFeedback')
    lib_func.argtypes = [ctypes.c_void_p,ctypes.c_void_p]
    lib_func.restype = ctypes.c_int
  else:
    raise RuntimeWarning('Could not load function hebiLogFileGetNextFeedback')

  if hasattr(lib, 'hebiStringGetString'):
    lib_func = getattr(lib, 'hebiStringGetString')
    lib_func.argtypes = [ctypes.c_void_p,ctypes.c_char_p,ctypes.POINTER(ctypes.c_size_t)]
    lib_func.restype = ctypes.c_int
  else:
    raise RuntimeWarning('Could not load function hebiStringGetString')

  if hasattr(lib, 'hebiStringRelease'):
    lib_func = getattr(lib, 'hebiStringRelease')
    lib_func.argtypes = [ctypes.c_void_p]
    lib_func.restype = None
  else:
    raise RuntimeWarning('Could not load function hebiStringRelease')

  if hasattr(lib, 'hebiSafetyParametersGetLastError'):
    lib_func = getattr(lib, 'hebiSafetyParametersGetLastError')
    lib_func.argtypes = []
    lib_func.restype = ctypes.c_char_p
  else:
    raise RuntimeWarning('Could not load function hebiSafetyParametersGetLastError')

  if hasattr(lib, 'hebiGetLibraryVersion'):
    lib_func = getattr(lib, 'hebiGetLibraryVersion')
    lib_func.argtypes = [ctypes.POINTER(ctypes.c_int32),ctypes.POINTER(ctypes.c_int32),ctypes.POINTER(ctypes.c_int32)]
    lib_func.restype = ctypes.c_int
  else:
    raise RuntimeWarning('Could not load function hebiGetLibraryVersion')

  if hasattr(lib, 'hebiCleanup'):
    lib_func = getattr(lib, 'hebiCleanup')
    lib_func.argtypes = []
    lib_func.restype = None
  else:
    raise RuntimeWarning('Could not load function hebiCleanup')


def populate_hebi_wrapper_funcs(lib):
  """
  Populates all API functions from the HEBI Core wrapper library
  """
  
  if hasattr(lib, 'hwInitialize'):
    lib_func = getattr(lib, 'hwInitialize')
    lib_func.argtypes = [ctypes.POINTER(HebiCommandMetadata),ctypes.POINTER(HebiFeedbackMetadata),ctypes.POINTER(HebiInfoMetadata)]
    lib_func.restype = None
  else:
    raise RuntimeWarning('Could not load function hwInitialize')

  if hasattr(lib, 'hwCommandSetFloat'):
    lib_func = getattr(lib, 'hwCommandSetFloat')
    lib_func.argtypes = [ctypes.POINTER(HebiCommandRef),ctypes.POINTER(ctypes.c_float),ctypes.c_uint32,ctypes.c_uint32]
    lib_func.restype = None
  else:
    raise RuntimeWarning('Could not load function hwCommandSetFloat')

  if hasattr(lib, 'hwCommandSetHighResAngle'):
    lib_func = getattr(lib, 'hwCommandSetHighResAngle')
    lib_func.argtypes = [ctypes.POINTER(HebiCommandRef),ctypes.POINTER(ctypes.c_double),ctypes.c_uint32,ctypes.c_uint32]
    lib_func.restype = None
  else:
    raise RuntimeWarning('Could not load function hwCommandSetHighResAngle')

  if hasattr(lib, 'hwCommandSetEnum'):
    lib_func = getattr(lib, 'hwCommandSetEnum')
    lib_func.argtypes = [ctypes.POINTER(HebiCommandRef),ctypes.POINTER(ctypes.c_int32),ctypes.c_uint32,ctypes.c_uint32]
    lib_func.restype = None
  else:
    raise RuntimeWarning('Could not load function hwCommandSetEnum')

  if hasattr(lib, 'hwCommandSetBool'):
    lib_func = getattr(lib, 'hwCommandSetBool')
    lib_func.argtypes = [ctypes.POINTER(HebiCommandRef),ctypes.POINTER(ctypes.c_bool),ctypes.c_uint32,ctypes.c_uint32]
    lib_func.restype = None
  else:
    raise RuntimeWarning('Could not load function hwCommandSetBool')

  if hasattr(lib, 'hwCommandSetNumberedFloat'):
    lib_func = getattr(lib, 'hwCommandSetNumberedFloat')
    lib_func.argtypes = [ctypes.POINTER(HebiCommandRef),ctypes.POINTER(ctypes.c_float),ctypes.c_uint32,ctypes.c_int,ctypes.c_uint32]
    lib_func.restype = None
  else:
    raise RuntimeWarning('Could not load function hwCommandSetNumberedFloat')

  if hasattr(lib, 'hwCommandSetIoPin'):
    lib_func = getattr(lib, 'hwCommandSetIoPin')
    lib_func.argtypes = [ctypes.POINTER(HebiCommandRef),ctypes.POINTER(HebiIoBankPinStruct),ctypes.c_uint32,ctypes.c_int,ctypes.c_uint32]
    lib_func.restype = None
  else:
    raise RuntimeWarning('Could not load function hwCommandSetIoPin')

  if hasattr(lib, 'hwCommandSetIoPinInt'):
    lib_func = getattr(lib, 'hwCommandSetIoPinInt')
    lib_func.argtypes = [ctypes.POINTER(HebiCommandRef),ctypes.POINTER(ctypes.c_int64),ctypes.c_uint32,ctypes.c_int,ctypes.c_uint32]
    lib_func.restype = None
  else:
    raise RuntimeWarning('Could not load function hwCommandSetIoPinInt')

  if hasattr(lib, 'hwCommandSetIoPinFloat'):
    lib_func = getattr(lib, 'hwCommandSetIoPinFloat')
    lib_func.argtypes = [ctypes.POINTER(HebiCommandRef),ctypes.POINTER(ctypes.c_float),ctypes.c_uint32,ctypes.c_int,ctypes.c_uint32]
    lib_func.restype = None
  else:
    raise RuntimeWarning('Could not load function hwCommandSetIoPinFloat')

  if hasattr(lib, 'hwCommandSetLed'):
    lib_func = getattr(lib, 'hwCommandSetLed')
    lib_func.argtypes = [ctypes.POINTER(HebiCommandRef),ctypes.POINTER(ctypes.c_int32),ctypes.c_uint32,ctypes.c_uint32]
    lib_func.restype = None
  else:
    raise RuntimeWarning('Could not load function hwCommandSetLed')

  if hasattr(lib, 'hwCommandSetFlag'):
    lib_func = getattr(lib, 'hwCommandSetFlag')
    lib_func.argtypes = [ctypes.POINTER(HebiCommandRef),ctypes.POINTER(ctypes.c_bool),ctypes.c_uint32,ctypes.c_uint32]
    lib_func.restype = None
  else:
    raise RuntimeWarning('Could not load function hwCommandSetFlag')

  if hasattr(lib, 'hwCommandGetFloat'):
    lib_func = getattr(lib, 'hwCommandGetFloat')
    lib_func.argtypes = [ctypes.POINTER(ctypes.c_float),ctypes.POINTER(HebiCommandRef),ctypes.c_uint32,ctypes.c_uint32]
    lib_func.restype = None
  else:
    raise RuntimeWarning('Could not load function hwCommandGetFloat')

  if hasattr(lib, 'hwCommandGetHighResAngle'):
    lib_func = getattr(lib, 'hwCommandGetHighResAngle')
    lib_func.argtypes = [ctypes.POINTER(ctypes.c_double),ctypes.POINTER(HebiCommandRef),ctypes.c_uint32,ctypes.c_uint32]
    lib_func.restype = None
  else:
    raise RuntimeWarning('Could not load function hwCommandGetHighResAngle')

  if hasattr(lib, 'hwCommandGetVector3f'):
    lib_func = getattr(lib, 'hwCommandGetVector3f')
    lib_func.argtypes = [ctypes.POINTER(HebiVector3f),ctypes.POINTER(HebiCommandRef),ctypes.c_uint32,ctypes.c_uint32]
    lib_func.restype = None
  else:
    raise RuntimeWarning('Could not load function hwCommandGetVector3f')

  if hasattr(lib, 'hwCommandGetQuaternionf'):
    lib_func = getattr(lib, 'hwCommandGetQuaternionf')
    lib_func.argtypes = [ctypes.POINTER(HebiQuaternionf),ctypes.POINTER(HebiCommandRef),ctypes.c_uint32,ctypes.c_uint32]
    lib_func.restype = None
  else:
    raise RuntimeWarning('Could not load function hwCommandGetQuaternionf')

  if hasattr(lib, 'hwCommandGetUInt64'):
    lib_func = getattr(lib, 'hwCommandGetUInt64')
    lib_func.argtypes = [ctypes.POINTER(ctypes.c_uint64),ctypes.POINTER(HebiCommandRef),ctypes.c_uint32,ctypes.c_uint32]
    lib_func.restype = None
  else:
    raise RuntimeWarning('Could not load function hwCommandGetUInt64')

  if hasattr(lib, 'hwCommandGetEnum'):
    lib_func = getattr(lib, 'hwCommandGetEnum')
    lib_func.argtypes = [ctypes.POINTER(ctypes.c_int32),ctypes.POINTER(HebiCommandRef),ctypes.c_uint32,ctypes.c_uint32]
    lib_func.restype = None
  else:
    raise RuntimeWarning('Could not load function hwCommandGetEnum')

  if hasattr(lib, 'hwCommandGetBool'):
    lib_func = getattr(lib, 'hwCommandGetBool')
    lib_func.argtypes = [ctypes.POINTER(ctypes.c_bool),ctypes.POINTER(HebiCommandRef),ctypes.c_uint32,ctypes.c_uint32]
    lib_func.restype = None
  else:
    raise RuntimeWarning('Could not load function hwCommandGetBool')

  if hasattr(lib, 'hwCommandGetNumberedFloat'):
    lib_func = getattr(lib, 'hwCommandGetNumberedFloat')
    lib_func.argtypes = [ctypes.POINTER(ctypes.c_float),ctypes.POINTER(HebiCommandRef),ctypes.c_uint32,ctypes.c_int,ctypes.c_uint32]
    lib_func.restype = None
  else:
    raise RuntimeWarning('Could not load function hwCommandGetNumberedFloat')

  if hasattr(lib, 'hwCommandGetIoPin'):
    lib_func = getattr(lib, 'hwCommandGetIoPin')
    lib_func.argtypes = [ctypes.POINTER(HebiIoBankPinStruct),ctypes.POINTER(HebiCommandRef),ctypes.c_uint32,ctypes.c_int,ctypes.c_uint32]
    lib_func.restype = None
  else:
    raise RuntimeWarning('Could not load function hwCommandGetIoPin')

  if hasattr(lib, 'hwCommandGetIoPinInt'):
    lib_func = getattr(lib, 'hwCommandGetIoPinInt')
    lib_func.argtypes = [ctypes.POINTER(ctypes.c_int64),ctypes.POINTER(HebiCommandRef),ctypes.c_uint32,ctypes.c_int,ctypes.c_uint32]
    lib_func.restype = None
  else:
    raise RuntimeWarning('Could not load function hwCommandGetIoPinInt')

  if hasattr(lib, 'hwCommandGetIoPinFloat'):
    lib_func = getattr(lib, 'hwCommandGetIoPinFloat')
    lib_func.argtypes = [ctypes.POINTER(ctypes.c_float),ctypes.POINTER(HebiCommandRef),ctypes.c_uint32,ctypes.c_int,ctypes.c_uint32]
    lib_func.restype = None
  else:
    raise RuntimeWarning('Could not load function hwCommandGetIoPinFloat')

  if hasattr(lib, 'hwCommandGetLed'):
    lib_func = getattr(lib, 'hwCommandGetLed')
    lib_func.argtypes = [ctypes.POINTER(ctypes.c_int32),ctypes.POINTER(HebiCommandRef),ctypes.c_uint32,ctypes.c_uint32]
    lib_func.restype = None
  else:
    raise RuntimeWarning('Could not load function hwCommandGetLed')

  if hasattr(lib, 'hwCommandGetFlag'):
    lib_func = getattr(lib, 'hwCommandGetFlag')
    lib_func.argtypes = [ctypes.POINTER(ctypes.c_bool),ctypes.POINTER(HebiCommandRef),ctypes.c_uint32,ctypes.c_uint32]
    lib_func.restype = None
  else:
    raise RuntimeWarning('Could not load function hwCommandGetFlag')

  if hasattr(lib, 'hwCommandHasField'):
    lib_func = getattr(lib, 'hwCommandHasField')
    lib_func.argtypes = [ctypes.POINTER(ctypes.c_bool),ctypes.POINTER(HebiCommandRef),ctypes.c_uint32,ctypes.c_uint32]
    lib_func.restype = None
  else:
    raise RuntimeWarning('Could not load function hwCommandHasField')

  if hasattr(lib, 'hwCommandHasIoPinInt'):
    lib_func = getattr(lib, 'hwCommandHasIoPinInt')
    lib_func.argtypes = [ctypes.POINTER(ctypes.c_bool),ctypes.POINTER(HebiCommandRef),ctypes.c_uint32,ctypes.c_int,ctypes.c_uint32]
    lib_func.restype = None
  else:
    raise RuntimeWarning('Could not load function hwCommandHasIoPinInt')

  if hasattr(lib, 'hwCommandHasIoPinFloat'):
    lib_func = getattr(lib, 'hwCommandHasIoPinFloat')
    lib_func.argtypes = [ctypes.POINTER(ctypes.c_bool),ctypes.POINTER(HebiCommandRef),ctypes.c_uint32,ctypes.c_int,ctypes.c_uint32]
    lib_func.restype = None
  else:
    raise RuntimeWarning('Could not load function hwCommandHasIoPinFloat')

  if hasattr(lib, 'hwFeedbackGetFloat'):
    lib_func = getattr(lib, 'hwFeedbackGetFloat')
    lib_func.argtypes = [ctypes.POINTER(ctypes.c_float),ctypes.POINTER(HebiFeedbackRef),ctypes.c_uint32,ctypes.c_uint32]
    lib_func.restype = None
  else:
    raise RuntimeWarning('Could not load function hwFeedbackGetFloat')

  if hasattr(lib, 'hwFeedbackGetHighResAngle'):
    lib_func = getattr(lib, 'hwFeedbackGetHighResAngle')
    lib_func.argtypes = [ctypes.POINTER(ctypes.c_double),ctypes.POINTER(HebiFeedbackRef),ctypes.c_uint32,ctypes.c_uint32]
    lib_func.restype = None
  else:
    raise RuntimeWarning('Could not load function hwFeedbackGetHighResAngle')

  if hasattr(lib, 'hwFeedbackGetVector3f'):
    lib_func = getattr(lib, 'hwFeedbackGetVector3f')
    lib_func.argtypes = [ctypes.POINTER(HebiVector3f),ctypes.POINTER(HebiFeedbackRef),ctypes.c_uint32,ctypes.c_uint32]
    lib_func.restype = None
  else:
    raise RuntimeWarning('Could not load function hwFeedbackGetVector3f')

  if hasattr(lib, 'hwFeedbackGetQuaternionf'):
    lib_func = getattr(lib, 'hwFeedbackGetQuaternionf')
    lib_func.argtypes = [ctypes.POINTER(HebiQuaternionf),ctypes.POINTER(HebiFeedbackRef),ctypes.c_uint32,ctypes.c_uint32]
    lib_func.restype = None
  else:
    raise RuntimeWarning('Could not load function hwFeedbackGetQuaternionf')

  if hasattr(lib, 'hwFeedbackGetUInt64'):
    lib_func = getattr(lib, 'hwFeedbackGetUInt64')
    lib_func.argtypes = [ctypes.POINTER(ctypes.c_uint64),ctypes.POINTER(HebiFeedbackRef),ctypes.c_uint32,ctypes.c_uint32]
    lib_func.restype = None
  else:
    raise RuntimeWarning('Could not load function hwFeedbackGetUInt64')

  if hasattr(lib, 'hwFeedbackGetEnum'):
    lib_func = getattr(lib, 'hwFeedbackGetEnum')
    lib_func.argtypes = [ctypes.POINTER(ctypes.c_int32),ctypes.POINTER(HebiFeedbackRef),ctypes.c_uint32,ctypes.c_uint32]
    lib_func.restype = None
  else:
    raise RuntimeWarning('Could not load function hwFeedbackGetEnum')

  if hasattr(lib, 'hwFeedbackGetBool'):
    lib_func = getattr(lib, 'hwFeedbackGetBool')
    lib_func.argtypes = [ctypes.POINTER(ctypes.c_bool),ctypes.POINTER(HebiFeedbackRef),ctypes.c_uint32,ctypes.c_uint32]
    lib_func.restype = None
  else:
    raise RuntimeWarning('Could not load function hwFeedbackGetBool')

  if hasattr(lib, 'hwFeedbackGetNumberedFloat'):
    lib_func = getattr(lib, 'hwFeedbackGetNumberedFloat')
    lib_func.argtypes = [ctypes.POINTER(ctypes.c_float),ctypes.POINTER(HebiFeedbackRef),ctypes.c_uint32,ctypes.c_int,ctypes.c_uint32]
    lib_func.restype = None
  else:
    raise RuntimeWarning('Could not load function hwFeedbackGetNumberedFloat')

  if hasattr(lib, 'hwFeedbackGetIoPin'):
    lib_func = getattr(lib, 'hwFeedbackGetIoPin')
    lib_func.argtypes = [ctypes.POINTER(HebiIoBankPinStruct),ctypes.POINTER(HebiFeedbackRef),ctypes.c_uint32,ctypes.c_int,ctypes.c_uint32]
    lib_func.restype = None
  else:
    raise RuntimeWarning('Could not load function hwFeedbackGetIoPin')

  if hasattr(lib, 'hwFeedbackGetIoPinInt'):
    lib_func = getattr(lib, 'hwFeedbackGetIoPinInt')
    lib_func.argtypes = [ctypes.POINTER(ctypes.c_int64),ctypes.POINTER(HebiFeedbackRef),ctypes.c_uint32,ctypes.c_int,ctypes.c_uint32]
    lib_func.restype = None
  else:
    raise RuntimeWarning('Could not load function hwFeedbackGetIoPinInt')

  if hasattr(lib, 'hwFeedbackGetIoPinFloat'):
    lib_func = getattr(lib, 'hwFeedbackGetIoPinFloat')
    lib_func.argtypes = [ctypes.POINTER(ctypes.c_float),ctypes.POINTER(HebiFeedbackRef),ctypes.c_uint32,ctypes.c_int,ctypes.c_uint32]
    lib_func.restype = None
  else:
    raise RuntimeWarning('Could not load function hwFeedbackGetIoPinFloat')

  if hasattr(lib, 'hwFeedbackGetLed'):
    lib_func = getattr(lib, 'hwFeedbackGetLed')
    lib_func.argtypes = [ctypes.POINTER(ctypes.c_int32),ctypes.POINTER(HebiFeedbackRef),ctypes.c_uint32,ctypes.c_uint32]
    lib_func.restype = None
  else:
    raise RuntimeWarning('Could not load function hwFeedbackGetLed')

  if hasattr(lib, 'hwFeedbackHasField'):
    lib_func = getattr(lib, 'hwFeedbackHasField')
    lib_func.argtypes = [ctypes.POINTER(ctypes.c_bool),ctypes.POINTER(HebiFeedbackRef),ctypes.c_uint32,ctypes.c_uint32]
    lib_func.restype = None
  else:
    raise RuntimeWarning('Could not load function hwFeedbackHasField')

  if hasattr(lib, 'hwFeedbackHasIoPinInt'):
    lib_func = getattr(lib, 'hwFeedbackHasIoPinInt')
    lib_func.argtypes = [ctypes.POINTER(ctypes.c_bool),ctypes.POINTER(HebiFeedbackRef),ctypes.c_uint32,ctypes.c_int,ctypes.c_uint32]
    lib_func.restype = None
  else:
    raise RuntimeWarning('Could not load function hwFeedbackHasIoPinInt')

  if hasattr(lib, 'hwFeedbackHasIoPinFloat'):
    lib_func = getattr(lib, 'hwFeedbackHasIoPinFloat')
    lib_func.argtypes = [ctypes.POINTER(ctypes.c_bool),ctypes.POINTER(HebiFeedbackRef),ctypes.c_uint32,ctypes.c_int,ctypes.c_uint32]
    lib_func.restype = None
  else:
    raise RuntimeWarning('Could not load function hwFeedbackHasIoPinFloat')

  if hasattr(lib, 'hwInfoGetFloat'):
    lib_func = getattr(lib, 'hwInfoGetFloat')
    lib_func.argtypes = [ctypes.POINTER(ctypes.c_float),ctypes.POINTER(HebiInfoRef),ctypes.c_uint32,ctypes.c_uint32]
    lib_func.restype = None
  else:
    raise RuntimeWarning('Could not load function hwInfoGetFloat')

  if hasattr(lib, 'hwInfoGetHighResAngle'):
    lib_func = getattr(lib, 'hwInfoGetHighResAngle')
    lib_func.argtypes = [ctypes.POINTER(ctypes.c_double),ctypes.POINTER(HebiInfoRef),ctypes.c_uint32,ctypes.c_uint32]
    lib_func.restype = None
  else:
    raise RuntimeWarning('Could not load function hwInfoGetHighResAngle')

  if hasattr(lib, 'hwInfoGetFlag'):
    lib_func = getattr(lib, 'hwInfoGetFlag')
    lib_func.argtypes = [ctypes.POINTER(ctypes.c_bool),ctypes.POINTER(HebiInfoRef),ctypes.c_uint32,ctypes.c_uint32]
    lib_func.restype = None
  else:
    raise RuntimeWarning('Could not load function hwInfoGetFlag')

  if hasattr(lib, 'hwInfoGetBool'):
    lib_func = getattr(lib, 'hwInfoGetBool')
    lib_func.argtypes = [ctypes.POINTER(ctypes.c_bool),ctypes.POINTER(HebiInfoRef),ctypes.c_uint32,ctypes.c_uint32]
    lib_func.restype = None
  else:
    raise RuntimeWarning('Could not load function hwInfoGetBool')

  if hasattr(lib, 'hwInfoGetEnum'):
    lib_func = getattr(lib, 'hwInfoGetEnum')
    lib_func.argtypes = [ctypes.POINTER(ctypes.c_int32),ctypes.POINTER(HebiInfoRef),ctypes.c_uint32,ctypes.c_uint32]
    lib_func.restype = None
  else:
    raise RuntimeWarning('Could not load function hwInfoGetEnum')

  if hasattr(lib, 'hwInfoGetLed'):
    lib_func = getattr(lib, 'hwInfoGetLed')
    lib_func.argtypes = [ctypes.POINTER(ctypes.c_int32),ctypes.POINTER(HebiInfoRef),ctypes.c_uint32,ctypes.c_uint32]
    lib_func.restype = None
  else:
    raise RuntimeWarning('Could not load function hwInfoGetLed')

  if hasattr(lib, 'hwInfoHasField'):
    lib_func = getattr(lib, 'hwInfoHasField')
    lib_func.argtypes = [ctypes.POINTER(ctypes.c_bool),ctypes.POINTER(HebiInfoRef),ctypes.c_uint32,ctypes.c_uint32]
    lib_func.restype = None
  else:
    raise RuntimeWarning('Could not load function hwInfoHasField')
