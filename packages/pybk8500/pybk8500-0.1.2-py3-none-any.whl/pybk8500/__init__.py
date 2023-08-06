from pybk8500.__meta__ import version as __version__

from pybk8500.parser import ChecksumError, MessageTypeError, Parser

# Why bother giving top level access to these classes?
# from pybk8500.field_types import Field, BytesField, StrField, \
#     IntField, Int8Field, Int16Field, Int32Field, FloatField, ScalarFloatField

from pybk8500.commands import \
    Message, CC_Commands, CV_Commands, CW_Commands, CR_Commands, \
    CommandStatus, SetRemoteOperation, LoadSwitch, SetMaxVoltage, ReadMaxVoltage, SetMaxCurrent, \
    ReadMaxCurrent, SetMaxPower, ReadMaxPower, SetMode, ReadMode, SetCCModeCurrent, ReadCCModeCurrent, \
    SetCVModeVoltage, ReadCVModeVoltage, SetCWModePower, ReadCWModePower, SetCRModeResistance, \
    ReadCRModeResistance, SetCCModeTransientCurrentAndTiming, ReadCCModeTransientParameters, \
    SetCVModeTransientVoltageAndTiming, ReadCVModeTransientParameters, SetCWModeTransientPowerAndTiming, \
    ReadCWModeTransientParameters, SetCRModeTransientResistanceAndTiming, ReadCRModeTransientParameters, \
    SelectListOperation, ReadListOperation, SetHowListsRepeat, ReadHowListsRepeat, SetNumberOfSteps, \
    ReadNumberOfSteps, SetOneStepCurrentAndTime, ReadOneStepCurrentAndTime, SetOneStepVoltageAndTime, \
    ReadOneStepVoltageAndTime, SetOneStepPowerAndTime, ReadOneStepPowerAndTime, SetOneStepResistanceAndTime, \
    ReadOneStepResistanceAndTime, SetListFileName, ReadListFileName, SetMemoryPartition, ReadMemoryPartition, \
    SaveListFile, RecallListFile, SetMinimumVoltage, ReadMinimumVoltage, SetTimerValueForLoadOn, \
    ReadTimerValueForLoadOn, SetTimerStateLoadOn, ReadTimerStateLoadOn, SetCommunicationAddress, \
    SetLocalControlState, SetRemoteSensingState, ReadRemoteSensingState, SelectTriggerSource, \
    ReadTriggerSource, TriggerElectronicLoad, SaveDCLoadSettings, RecallDCLoadSettings, SelectFunctionType, \
    GetFunctionType, ReadInputVoltageCurrentPowerState, GetProductInfo, ReadBarCode


try:
    from pybk8500.send_cmd import CommunicationManager
except (ImportError, Exception) as err:
    class CommunicationManager(object):
        error = err

        def __new__(cls, *args, **kwargs):
            raise EnvironmentError('Missing dependent "pyserial" or "continuous_threading" library! {}'
                                   .format(cls.error)) from cls.error
