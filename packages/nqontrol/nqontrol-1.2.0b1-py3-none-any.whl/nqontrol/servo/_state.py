# pylint: disable=protected-access,redefined-outer-name,cyclic-import
import logging as log
from math import copysign

from nqontrol.general import helpers, settings
from nqontrol.general.errors import DeviceError
from nqontrol.general.helpers import (
    convertFloat2Volt,
    convertVolt2Float,
    rearrange_filter_coeffs,
)

########################################
# Help methods
########################################


def _sendAllToAdwin(self):
    """Write all settings to ADwin."""

    # Workaround to avoid recursive dependencies
    lockThreshold = self._autolock["threshold"]
    lockThresholdBreak = self._autolock["threshold_break"]
    inputSensitivity = self._state["inputSensitivity"]

    # Control parameters
    self.offset = self._state["offset"]
    self.gain = self._state["gain"]
    self.filters = self._state["filters"]
    self.inputSensitivity = inputSensitivity
    self.auxSensitivity = self._state["auxSensitivity"]

    self._initLockValues()

    self._sendLockControl()
    # Control flags
    self._sendFilterControl()

    self.lockThreshold = lockThreshold
    self.lockThresholdBreak = lockThresholdBreak


def _readAllFromAdwin(self):
    self._readFilterControl()
    _ = self.offset
    _ = self.gain
    _ = self.filters
    _ = self.inputSensitivity
    _ = self.auxSensitivity


def _triggerReload(self):
    """Trigger bit to trigger reloading of parameters."""
    par = self._adw.Get_Par(settings.PAR_RELOADBIT)
    # only trigger if untriggered
    if not helpers.readBit(par, self._channel - 1):
        par = helpers.changeBit(par, self._channel - 1, True)
        self._adw.Set_Par(settings.PAR_RELOADBIT, par)
    else:
        raise DeviceError(
            "ADwin has been triggered to reload the shared RAM within 10µs or the realtime program doesn't run properly."
        )


def _readFilterControl(self):
    c = self._adw.Get_Par(settings.PAR_FCR + self._channel)
    # read control bits
    self._state["auxSw"] = helpers.readBit(c, 9)
    for i in range(5):
        bit = helpers.readBit(c, 4 + i)
        self._state["filtersEnabled"][i] = bit
        assert (
            list(self._state["filtersEnabled"])[i] == bit
        ), f'dict: {list(self._state["filtersEnabled"])[i]}, bit: {bit}'
    # self._state['snapSw'] = helpers.readBit(c, 3)
    self._state["offsetSw"] = helpers.readBit(c, 2)
    self._state["outputSw"] = helpers.readBit(c, 1)
    self._state["inputSw"] = helpers.readBit(c, 0)


def _sendFilterControl(self):
    # read current state
    c = self._adw.Get_Par(settings.PAR_FCR + self._channel)

    # set control bits
    c = helpers.changeBit(c, 9, self._state["auxSw"])
    for i in range(5):
        c = helpers.changeBit(c, 4 + i, self._state["filtersEnabled"][i])
    # c = helpers.changeBit(c, 3, self._state['snapSw'])
    c = helpers.changeBit(c, 2, self._state["offsetSw"])
    c = helpers.changeBit(c, 1, self._state["outputSw"])
    c = helpers.changeBit(c, 0, self._state["inputSw"])

    self._adw.Set_Par(settings.PAR_FCR + self._channel, c)


########################################
# Change servo state
########################################


@property
def filterStates(self):
    """
    List of all filter states.

    :getter: Return the filter states.
    :setter: Set all filter states.
    :type: :obj:`list` of :code:`5*`:obj:`bool`.
    """
    self._readFilterControl()
    return self._state["filtersEnabled"]


@filterStates.setter
def filterStates(self, filtersEnabled):
    self._state["filtersEnabled"] = filtersEnabled
    self._sendFilterControl()


def filterState(self, id_, enabled):
    """Enable or disable the SOS filter with number `id_`.

    Parameters
    ----------
    id_: :obj:`int` index from 0 to 4
        Index of the filter to control.
    enabled: :obj:`bool`
        :obj:`True` to enable.

    """
    filtersEnabled = self._state["filtersEnabled"]
    filtersEnabled[id_] = enabled
    self._state["filtersEnabled"] = filtersEnabled
    self._sendFilterControl()


@property
def auxSw(self):
    """
    Switch for mixing the aux signal to the output.

    :getter: Return the state of aux mixing.
    :setter: Enable or disable the aux mixing.
    :type: :obj:`bool`
    """
    self._readFilterControl()
    return self._state["auxSw"]


@auxSw.setter
def auxSw(self, enabled):
    self._state["auxSw"] = enabled
    self._sendFilterControl()


@property
def offsetSw(self):
    """
    Enable or disable offset switch.

    :getter: Return the state of the switch.
    :setter: Enable or disable the offset.
    :type: :obj:`bool`
    """
    self._readFilterControl()
    return self._state["offsetSw"]


@offsetSw.setter
def offsetSw(self, enabled):
    self._state["offsetSw"] = enabled
    self._sendFilterControl()


@property
def outputSw(self):
    """
    Enable or disable output switch.

    :getter: Return the state of the switch.
    :setter: Enable or disable the output.
    :type: :obj:`bool`
    """
    self._readFilterControl()
    return self._state["outputSw"]


@outputSw.setter
def outputSw(self, enabled):
    self._state["outputSw"] = enabled
    self._sendFilterControl()


@property
def inputSw(self):
    """
    Enable or disable input switch.

    :getter: Return the state of the switch.
    :setter: Enable or disable the input.
    :type: :obj:`bool`
    """
    self._readFilterControl()
    return self._state["inputSw"]


@inputSw.setter
def inputSw(self, enabled):
    self._state["inputSw"] = enabled
    self._sendFilterControl()


@property
def offset(self):
    """
    Offset value in volt. (-10 to 10)

    :getter: Return the offset value.
    :setter: Set the offset.
    :type: :obj:`float`
    """
    index = self._channel + 8
    data = self._adw.GetData_Double(settings.DATA_OFFSETGAIN, index, 1)[0]
    offset = convertFloat2Volt(data, self.inputSensitivity, signed=True)
    self._state["offset"] = offset

    return offset


@offset.setter
def offset(self, offset: float):
    limit = round(10 / pow(2, self.inputSensitivity), 2)
    if abs(offset) > limit:
        offset = copysign(limit, offset)
        log.warning(
            f"With the selected mode the offset must be in the limits of ±{limit}V. Adjusting to {offset}V..."
        )
    self._state["offset"] = offset
    index = self._channel + 8
    offsetInt = convertVolt2Float(offset, self.inputSensitivity, signed=True)
    self._adw.SetData_Double([offsetInt], settings.DATA_OFFSETGAIN, index, 1)


@property
def gain(self):
    """
    Overall gain factor.

    :getter: Return the gain value.
    :setter: Set the gain.
    :type: :obj:`float`
    """
    index = self._channel
    data = self._adw.GetData_Double(settings.DATA_OFFSETGAIN, index, 1)[0]
    gain = data * pow(2, self.inputSensitivity)
    self._state["gain"] = gain

    return gain


@gain.setter
def gain(self, gain):
    self._state["gain"] = gain
    index = self._channel
    effectiveGain = gain / pow(2, self.inputSensitivity)
    self._adw.SetData_Double([effectiveGain], settings.DATA_OFFSETGAIN, index, 1)


@property
def inputSensitivity(self):
    r"""
    Input sensitivity mode (0 to 3).

    The input voltage is amplified by :math:`2^\mathrm{mode}`.

    +------+---------------+------------+
    | mode | amplification | limits (V) |
    +======+===============+============+
    | 0    | 1             | 10         |
    +------+---------------+------------+
    | 1    | 2             | 5          |
    +------+---------------+------------+
    | 2    | 4             | 2.5        |
    +------+---------------+------------+
    | 3    | 8             | 1.25       |
    +------+---------------+------------+

    :getter: Return the sensitivity mode.
    :setter: Set the mode.
    :type: :obj:`int`
    """
    data = self._adw.Get_Par(settings.PAR_SENSITIVITY)
    mask = 3
    # bit shifting backwards
    mode = data >> self._channel * 2 - 2 & mask
    self._state["inputSensitivity"] = mode

    return mode


@inputSensitivity.setter
def inputSensitivity(self, mode):
    if not 0 <= mode <= 3:
        raise ValueError("Choose a mode between 0 and 3")
    gain = self.gain
    offset = self.offset

    self._state["inputSensitivity"] = mode

    currentRegister = self._adw.Get_Par(settings.PAR_SENSITIVITY)
    register = helpers.clearBit(currentRegister, self._channel * 2 - 2)
    register = helpers.clearBit(register, self._channel * 2 - 1)

    # bit shifting
    register += mode << self._channel * 2 - 2

    self._adw.Set_Par(settings.PAR_SENSITIVITY, register)

    # Update gain to correct gain change from input sensitivity
    self.gain = gain
    self.offset = offset


@property
def auxSensitivity(self):
    r"""
    Aux sensitivity mode (0 to 3).

    The input voltage is amplified by :math:`2^\mathrm{mode}`.

    +------+---------------+------------+
    | mode | amplification | limits (V) |
    +======+===============+============+
    | 0    | 1             | 10         |
    +------+---------------+------------+
    | 1    | 2             | 5          |
    +------+---------------+------------+
    | 2    | 4             | 2.5        |
    +------+---------------+------------+
    | 3    | 8             | 1.25       |
    +------+---------------+------------+

    :getter: Return the sensitivity mode.
    :setter: Set the mode.
    :type: :obj:`int`
    """

    data = self._adw.Get_Par(settings.PAR_SENSITIVITY)
    mask = 3
    # bit shifting backwards
    mode = data >> self._channel * 2 + 14 & mask
    self._state["auxSensitivity"] = mode

    return mode


@auxSensitivity.setter
def auxSensitivity(self, mode):
    if not 0 <= mode <= 3:
        raise ValueError(f"Choose a mode between 0 and 3, was {mode}.")

    # saving old lock parameters
    threshold = self.lockThreshold
    threshold_break = self.lockThresholdBreak

    self._state["auxSensitivity"] = mode

    currentRegister = self._adw.Get_Par(settings.PAR_SENSITIVITY)
    register = helpers.clearBit(currentRegister, self._channel * 2 + 14)
    register = helpers.clearBit(register, self._channel * 2 + 15)

    register += mode << self._channel * 2 + 14

    self._adw.Set_Par(settings.PAR_SENSITIVITY, register)

    # setting lock parameters with new sensitivity
    self.lockThreshold = threshold
    self.lockThresholdBreak = threshold_break


@property
def filters(self):
    """
    All second order sections (SOS) of all filters.

    A neutral filter matrix looks like:

    .. code:: python

        [ [1, 0, 0, 0, 0],
          [1, 0, 0, 0, 0],
          [1, 0, 0, 0, 0],
          [1, 0, 0, 0, 0],
          [1, 0, 0, 0, 0] ]

    Use :obj:`ServoDesign` from :obj:`openqlab.analysis` to create your filters.
    That object you can simply pass to a servo using :obj:`applyServoDesign`.

    :getter: Return all filter values.
    :setter: Write all 5 filters to ADwin and trigger reloading.
    :type: :code:`(5, 5)` matrix with filter values (:obj:`float`).
    """
    startIndex = (
        self._channel - 1
    ) * settings.NUMBER_OF_FILTERS * settings.NUMBER_OF_SOS + 1

    data = self._adw.GetData_Double(
        settings.DATA_FILTERCOEFFS,
        startIndex,
        settings.NUMBER_OF_FILTERS * settings.NUMBER_OF_SOS,
    )

    for i in range(settings.NUMBER_OF_FILTERS):
        for j in range(settings.NUMBER_OF_SOS):
            self._state["filters"][i][j] = data[i * settings.NUMBER_OF_FILTERS + j]

    return list(self._state["filters"])


@filters.setter
def filters(self, filters):
    if not len(filters) == settings.NUMBER_OF_FILTERS:
        raise IndexError(
            f"A servo must have exactly {settings.NUMBER_OF_FILTERS} filters!"
        )
    for filter_ in filters:
        if not len(filter_) == settings.NUMBER_OF_SOS:
            raise IndexError(
                f"A servo must have exactly {settings.NUMBER_OF_FILTERS} filters with {settings.NUMBER_OF_SOS} SOS!"
            )

    self._state["filters"] = filters

    startIndex = (
        self._channel - 1
    ) * settings.NUMBER_OF_FILTERS * settings.NUMBER_OF_SOS + 1

    data = []
    for filter_ in filters:
        for i in filter_:
            data.append(i)
    self._adw.SetData_Double(data, settings.DATA_FILTERCOEFFS, startIndex, len(data))
    self._triggerReload()


def applyServoDesign(self, servoDesign=None):
    """
    Apply filters from a :obj:`ServoDesign` object.

    Parameters
    ----------
    servoDesign: :obj:`openqlab.analysis.ServoDesign`
        Object to apply filters from.
    """
    if servoDesign is None:
        servoDesign = self.servoDesign
    else:
        self.servoDesign = servoDesign
    discreteServoDesign = servoDesign.discrete_form(
        sampling_frequency=settings.SAMPLING_RATE
    )
    filters6 = discreteServoDesign["filters"]  # returns a list of dicts
    filters = [[1.0, 0, 0, 0, 0]] * servoDesign.MAX_FILTERS
    filtersEnabled = [False] * servoDesign.MAX_FILTERS

    for f in filters6:
        j = f["index"]
        filters[j] = rearrange_filter_coeffs(f["sos"])
        filtersEnabled[j] = f["enabled"]

    self.gain = discreteServoDesign["gain"]
    self.filters = filters
    self.filterStates = filtersEnabled
