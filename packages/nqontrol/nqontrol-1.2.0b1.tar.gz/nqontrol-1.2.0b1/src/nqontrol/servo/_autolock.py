# pylint: disable=protected-access,redefined-outer-name,cyclic-import
import logging as log

import numpy as np

from nqontrol.general import helpers, settings
from nqontrol.general.errors import AutoLockAnalysisError, DeviceError
from nqontrol.general.helpers import (
    convertFloat2Volt,
    convertFrequency2Stepsize,
    convertStepsize2Frequency,
    convertVolt2Float,
)

##############################################################
#####################   Autolock   ###########################
##############################################################

###################   Lock helpers   #########################


def _lockIter(self):
    # just a helper method to expose the lockIterator for testing

    lockIter = self._adw.GetData_Double(settings.DATA_LOCK_ITER, self._channel, 1)[0]
    return lockIter


def _testLockOutput(self):
    # a helper to expose the last output used in locking
    # specifically, when locked this is the output value added to the lockIter of where the lock was found, meaning the new output is set as
    # out_new = lockIter + out_old
    # it is this out_old we wish to expose
    testOutput = self._adw.GetData_Long(settings.DATA_LOCK_OUTPUT, self._channel, 1)[0]
    testOutput = convertFloat2Volt(testOutput, self.auxSensitivity, signed=False)
    return testOutput


###################   Lock control   #########################


def _readLockControl(self):
    # boolean values
    lcr = self._adw.Get_Par(settings.PAR_LCR)
    gcr = self._adw.Get_Par(settings.PAR_GCR)
    log.debug(bin(lcr))
    bitoffset = self._channel - 1
    self._autolock["search"] = helpers.readBit(lcr, bitoffset)
    self._autolock["locked"] = helpers.readBit(lcr, bitoffset + 8)
    self._autolock["relock"] = helpers.readBit(lcr, bitoffset + 16)
    self._autolock["greater"] = helpers.readBit(gcr, self._channel - 1)
    self._autolock["rampmode"] = helpers.readBit(gcr, 8 + self._channel - 1)
    log.debug(
        f"Read out lock pars on servo {self._channel}: lcr {bin(lcr)} and {bin(gcr)}."
    )


def _sendLockControl(self):
    # this send the control register and greater boolean
    lcr = self._adw.Get_Par(settings.PAR_LCR)
    gcr = self._adw.Get_Par(settings.PAR_GCR)
    bitoffset = self._channel - 1
    # search bit
    lcr = helpers.changeBit(lcr, bitoffset, self._autolock["search"])
    # locked bit
    lcr = helpers.changeBit(lcr, bitoffset + 8, self._autolock["locked"])
    # relock bit
    lcr = helpers.changeBit(lcr, bitoffset + 16, self._autolock["relock"])
    # greater bit
    gcr = helpers.changeBit(gcr, (self._channel - 1), self._autolock["greater"])
    # rampmode bit
    gcr = helpers.changeBit(gcr, 8 + (self._channel - 1), self._autolock["rampmode"])
    log.debug(
        f"Sending lock pars on servo {self._channel}: lcr {bin(lcr)} and gcr {bin(gcr)}."
    )
    self._adw.Set_Par(settings.PAR_LCR, lcr)
    self._adw.Set_Par(settings.PAR_GCR, gcr)


@property
def lockSearch(self):
    """Return the lock search state. Don't confuse with `locked`.

    `0`: off
    `1`: search

    :getter: Trigger a read from ADwin. Return current value.
    :setter: Set new lock state. Will convert given value to bool and then back to int.
    :type: :obj:`int`

    """
    self._readLockControl()
    return self._autolock["search"]


@lockSearch.setter
def lockSearch(self, search):
    if not isinstance(search, (int, bool)):
        raise TypeError("Must be given as either an integer or a boolean.")
    search = int(bool(search))
    if search:
        # disabling input, output and aux while searching
        self.outputSw = False
        self.inputSw = False
        self.auxSw = False
        self._autolock["locked"] = 0
    self._autolock["search"] = search
    self._sendLockControl()


@property
def locked(self):
    """Return the locked state. Whether the servo is currently in locked state.

    `0`: not locked
    `1`: locked

    :getter: Trigger a read from ADwin. Return current value.
    :setter: Set new locked state. Will convert given value to bool and then back to int. Really only makes sense to turn this off manually, not on. Still, when manually switching on, will make sure to turn off lock search.
    :type: :obj:`int`

    """
    self._readLockControl()
    return self._autolock["locked"]


@locked.setter
def locked(self, locked):
    if not isinstance(locked, (int, bool)):
        raise TypeError(
            f"Must be given as either an integer or a boolean, was {locked}."
        )
    locked = int(bool(locked))
    if locked:
        self._autolock["search"] = 0
    self._autolock["locked"] = locked
    self._sendLockControl()


@property
def relock(self):
    """
    Set the lock to trigger a relock automatically when falling below or above threshold (according to `greater` setting). The `relock` parameter is either 0 or 1, can also be passed as a boolean.

    :getter: Return the current value.
    :setter: Set the condition.
    :type: :obj:`int`
    """
    self._readLockControl()
    return self._autolock["relock"]


@relock.setter
def relock(self, relock):
    if not isinstance(relock, (int, bool)):
        raise TypeError(
            f"Must be given as either an integer or a boolean, was {relock}."
        )
    relock = int(bool(relock))
    self._autolock["relock"] = relock
    self._sendLockControl()


@property
def lockGreater(self):
    """
    Set the lock direction to either greater (True) or lesser (False) than the threshold.

    :getter: Return the current value.
    :setter: Set the condition.
    :type: :obj:`bool`
    """
    self._readLockControl()
    return self._autolock["greater"]


@lockGreater.setter
def lockGreater(self, greater):
    if not isinstance(greater, (int, bool)):
        raise TypeError(
            f"Must be given as either an integer or a boolean, was {greater}."
        )
    greater = int(bool(greater))
    self._autolock["greater"] = greater
    self._sendLockControl()


@property
def lockRampmode(self):
    """Enable rampmode bit for lock function. If in ramp mode, the autolock will keep searching even if a lock is found. This replaces the previous ramp.

    :getter: Return current rampmode bit.
    :setter: Set rampmode bit True or False.
    :type: :obj:`bool`
    """
    self._readLockControl()
    return self._autolock["rampmode"]


@lockRampmode.setter
def lockRampmode(self, ramp):
    if not isinstance(ramp, (int, bool)):
        raise TypeError(f"Must be given as either an integer or a boolean, was {ramp}.")
    ramp = int(bool(ramp))
    self._autolock["rampmode"] = ramp
    self._sendLockControl()


###################   Lock values   #########################


def _initLockValues(self):
    # split from _sendLockControl to avoid recursion
    # voltage values for the lock parameters
    self.lockThreshold = self._autolock["threshold"]
    self.lockThresholdBreak = self._autolock["threshold_break"]
    self.lockStepsize = self._autolock["stepsize"]
    self.lockAmplitude = self._autolock["amplitude"]
    self.lockOffset = self._autolock["offset"]


@property
def lockThreshold(self):
    """Get or set the autolock threshold.

    :getter: Trigger a read from ADwin. Return the threshold.
    :setter: Set the threshold.
    :type: :obj:`float`
    """
    # voltage values
    self._autolock["threshold"] = convertFloat2Volt(
        self._adw.GetData_Double(settings.DATA_LOCK, self._channel, 1)[0],
        self.auxSensitivity,
        signed=False,
    )
    return self._autolock["threshold"]


@lockThreshold.setter
def lockThreshold(self, threshold):
    try:
        threshold = float(threshold)
    except (ValueError, TypeError):
        raise TypeError(f"threshold must be a float or int, was {type(threshold)}.")
    self._autolock["threshold"] = threshold
    threshold = convertVolt2Float(threshold, self.auxSensitivity, signed=False)
    # Sending values to ADwin
    # threshold
    self._adw.SetData_Double([threshold], settings.DATA_LOCK, self._channel, 1)


@property
def lockThresholdBreak(self):
    """Get or set the autolock threshold break. This is the tolerance value for falling out of lock.

    :getter: Trigger a read from ADwin. Return the threshold break.
    :setter: Set the threshold break value.
    :type: :obj:`float`
    """
    # voltage values
    self._autolock["threshold_break"] = convertFloat2Volt(
        self._adw.GetData_Double(settings.DATA_LOCK, self._channel + 8, 1)[0],
        self.auxSensitivity,
        signed=False,
    )
    return self._autolock["threshold_break"]


@lockThresholdBreak.setter
def lockThresholdBreak(self, threshold):
    try:
        threshold = float(threshold)
    except (ValueError, TypeError):
        raise TypeError(
            f"threshold break must be a float or int, was {type(threshold)}."
        )
    self._autolock["threshold_break"] = threshold
    threshold = convertVolt2Float(threshold, self.auxSensitivity, signed=False)
    # Sending values to ADwin
    self._adw.SetData_Double([threshold], settings.DATA_LOCK, self._channel + 8, 1)


@property
def lockAmplitude(self):
    """Get or set the autolock ramp amplitude. A floating point number from 0 to 10 which will be multiplied to the normalized (-1 to 1 V) ramp.

    ramp_position = amplitude * iterator + offset

    :getter: Trigger a read from ADwin. Return the amplitude.
    :setter: Set the amplitude.
    :type: :obj:`float`
    """
    # voltage values
    self._autolock["amplitude"] = self._adw.GetData_Double(
        settings.DATA_LOCK, 16 + self._channel, 1
    )[0]
    return self._autolock["amplitude"]


@lockAmplitude.setter
def lockAmplitude(self, amplitude):
    try:
        amplitude = float(amplitude)
    except (ValueError, TypeError):
        raise TypeError(f"Amplitude must be a float or int, was {type(amplitude)}.")
    if not 0 <= amplitude <= 10:
        raise ValueError(
            f"Amplitude should be positive and in the range of 0 to 10 V, was {amplitude}."
        )
    self._autolock["amplitude"] = amplitude
    # amplitude is transferred directly and does not have to be converted
    self._adw.SetData_Double([amplitude], settings.DATA_LOCK, self._channel + 16, 1)


@property
def lockOffset(self):
    """Get or set the autolock ramp offset. A floating point number from -10 to 10 V which will be added to the ramp.

    ramp_position = amplitude * iterator + offset

    :getter: Trigger a read from ADwin. Return the offset.
    :setter: Set the offset.
    :type: :obj:`float`
    """
    # voltage values
    self._autolock["offset"] = convertFloat2Volt(
        self._adw.GetData_Double(settings.DATA_LOCK, 24 + self._channel, 1)[0],
        signed=False,
    )
    return self._autolock["offset"]


@lockOffset.setter
def lockOffset(self, offset):
    try:
        offset = float(offset)
    except (ValueError, TypeError):
        raise TypeError(f"Offset must be a float or int, was {type(offset)}.")
    if not -10 <= offset <= 10:
        raise ValueError(f"Offset can't be outside -10 and 10 volts, was {offset}.")
    self._autolock["offset"] = offset
    offset = convertVolt2Float(offset, signed=False)
    # Sending values to ADwin
    self._adw.SetData_Double([offset], settings.DATA_LOCK, self._channel + 24, 1)


@property
def lockStepsize(self):
    """Read out the autolock stepsize.

    Returns
    -------
    :obj:`int`
        Stepsize value.
    """
    self._autolock["stepsize"] = self._adw.GetData_Double(
        settings.DATA_LOCK_STEPSIZE, self._channel, 1
    )[0]
    return self._autolock["stepsize"]


@lockStepsize.setter
def lockStepsize(self, stepsize):
    if not isinstance(stepsize, (float)):
        raise TypeError(f"Ideally, pass the stepsize as a float, was {type(stepsize)}.")
    if (
        not convertFrequency2Stepsize(settings.RAMP_FREQUENCY_MIN)
        <= stepsize
        <= convertFrequency2Stepsize(settings.RAMP_FREQUENCY_MAX)
    ):
        raise ValueError(
            f"Please make sure the stepsize is in the correct range of {convertFrequency2Stepsize(settings.RAMP_FREQUENCY_MIN)} to {convertFrequency2Stepsize(settings.RAMP_FREQUENCY_MAX)}, was {stepsize}."
        )
    self._autolock["stepsize"] = stepsize
    self._adw.SetData_Double([stepsize], settings.DATA_LOCK_STEPSIZE, self._channel, 1)
    self._updateFifoStepsize()


@property
def lockFrequency(self):
    """Rough frequency of the ramp, might contain rounding errors. Calculates the frequency from the stepsize and search range of the lock. If possible, use the stepsize directly!

    :getter: Set the frequency.
    :setter: Get the frequency.
    :type: :obj:`float`
    """
    return convertStepsize2Frequency(self.lockStepsize)


@lockFrequency.setter
def lockFrequency(self, frequency):
    if not isinstance(frequency, (int, float)):
        raise TypeError(
            f"Please pass the frequency as a float (ideally) or integer, was {type(frequency)}."
        )
    if not settings.RAMP_FREQUENCY_MIN <= frequency <= settings.RAMP_FREQUENCY_MAX:
        raise ValueError(
            f"Please make sure the frequency is in the correct range of {settings.RAMP_FREQUENCY_MIN} to {settings.RAMP_FREQUENCY_MAX} Hz, was {frequency}."
        )
    self.lockStepsize = convertFrequency2Stepsize(frequency)


############   Autolock command line tools   ##############


def autolock(  # pylint: disable=too-many-arguments
    self,
    search=True,
    relock=None,
    rampmode=None,
    amplitude=None,
    offset=None,
    frequency=None,
    analysis=True,
    **args,
):
    """Autolock activation for command line use. The user may pass options as additional arguments. For valid options see the signature of :obj:`Servo.autolockOptions`.

    Parameters
    ----------
    search : :obj:`bool`, optional
        Will trigger a new autolock search. If an integer is passed, it will be interpreted as a boolean value, by default True
    relock : :obj:`bool`, optional
        Whether relock feature should be active or inactive. Also see the documentation for :obj:`Servo.relock`, by default None
    rampmode : :obj:`bool`, optional
        Whether lock search should be in rampmode (won't snap to a lock point).
    amplitude : :obj:`float`, optional
        Autolock ramp amplitude, 0 to 10 V.
    offset : :obj:`float`, optional
        Autolock ramp offset, -10 to 10 V.
    frequency : obj:`int`, optional
        Lock ramp frequency. From {0} to {1}.
    analysis: :obj:`bool`, optional
        Whether to run the threshold analysis, by default True

    Returns
    -------
    :obj:`String`
        Information string as feedback.

    Raises
    ------
    TypeError
        The `search` keyword should be an integer (which translates to boolean) or boolean value.
    """.format(
        settings.RAMP_FREQUENCY_MIN, settings.RAMP_FREQUENCY_MAX
    )
    if not isinstance(search, (bool, int)):
        raise TypeError(
            f"Please make sure the search keyword is an integer or boolean, indicating whether to turn lock searching on or off. {search} was given."
        )
    search = int(bool(search))
    s = ""
    s += self._autolockOptions(relock, rampmode, amplitude, offset, frequency, **args)
    if analysis:
        self.lockAnalysis()
    self.lockSearch = search
    s += f"\nLOCK SEARCH STATUS: {self.lockSearch}."
    return s


def _autolockOptions(  # pylint: disable=too-many-arguments
    self,
    relock=None,
    rampmode=None,
    amplitude=None,
    offset=None,
    frequency=None,
    **args,
):
    s = ""
    if relock is not None:
        self.relock = relock
        s += f"Set relock option: {self.relock}. "
    if rampmode is not None:
        self.lockRampmode = rampmode
        s += f"Set lock rampmode: {self.lockRampmode}. "
    if amplitude is not None:
        self.lockAmplitude = amplitude
        s += f"Changed lock amplitude: {self.lockAmplitude}. "
    if offset is not None:
        self.lockOffset = offset
        s += f"Changed lock offset: {self.lockOffset}. "
    if frequency is not None:
        self.lockFrequency = frequency
        s += f"Changed lock ramp frequency: {self.lockFrequency}. "
    if s == "":
        s += "No options changed. "
    if args:
        s += f"Additional arguments were passed that had no effect: {args}. "
    return s


def enableRamp(self, amplitude=None, offset=None, frequency=None, enableFifo=True):
    """
    Enable the lock ramp on this servo. Intended for command line use.

    Parameters
    ----------
    amplitude : :obj:`float`, optional
        Ramp amplitude from 0 to 10 V. (0 does not make too much sense, though.) Default 1.
    offset : :obj:`float`, optional
        Ramp offset from -10 to 10 V. Default 0.
    frequency : :obj:`float`, optional
        Ramp frequency from 1 to 100 Hz. (Can be changed in settings.)
    enableFifo: :obj:`bool`
        Defaults to :obj:`True`.
        Possible not to enable the FIFO buffering for this servo.

    """
    self._readLockControl()

    if amplitude is not None:
        self.lockAmplitude = amplitude

    if offset is not None:
        self.lockOffset = offset

    if frequency is not None:
        self.lockFrequency = frequency

    self._autolock["rampmode"] = 1
    self._autolock["search"] = 1

    self._sendLockControl()

    if enableFifo:
        self.enableFifo(self._calculateFifoStepsize())


def disableRamp(self):
    """Disable the ramp on this channel. Counterpart to `enableRamp`."""
    self._readLockControl()
    self._autolock["search"] = 0
    self._autolock["rampmode"] = 0
    self._sendLockControl()


##############   Autolock analysis tools   ################


def _prepareLockData(self):
    self._readLockControl()
    # preserve old state
    old_search = self._autolock["search"]
    old_rampmode = self._autolock["rampmode"]
    old_ydata = self.realtime["ydata"]
    # turn everything off in case it's still running
    self.lockSearch = 0
    self.locked = 0
    # turn on the ramp and search again
    self.lockRampmode = 1
    # make sure aux is included
    self.realtime["ydata"] = self.DEFAULT_COLUMNS
    self.lockSearch = 1
    data = self.takeData()
    # set old values again
    self.lockSearch = old_search
    self.lockRampmode = old_rampmode
    self.realtime["ydata"] = old_ydata
    return data


def lockAnalysis(self, testdata=None, raiseErrors: bool = False, tries: int = 10):
    """Analyze the threshold and direction to be used in the autolock feature. Takes in data or reads out automatically if None was provided. Determines the correct peak by analyzing median value of the AUX channel and comparing it to the signal's maxima and minima. A peak is deemed valid if it is sufficiently different from the median value. Generally, one would expect good peaks to be much bigger than white noise, thus we deem the analysis valid using a 3 sigma criteria.

    You can also use this in conjunction with the `autolock` command line method, e.g.

    ```python
    s = DEVICE.servo(1)
    s.lockAmplitude = 3
    s.lockOffset = -4
    s.lockFrequency = 3
    s.lockAnalysis()
    s.autolock()
    ```

    Parameters
    ----------
    testdata : :obj:`pandas.DataFrame`, optional
        For testing purposes one can provide a pandas DataFrame to be analyzed. Please make sure it contains a 'aux' column. If no data is provided, it will be read out from ADwin. (by default None)
    raiseErrors : bool, optional
        Can raise errors instead of logs for testing purposes. (by default False)
    """
    for n in range(tries):
        # take in new data
        if testdata is None:
            data = self._prepareLockData()
        else:
            data = testdata

        log.info(f"data columns {data.columns}")

        if data.empty:
            if n == tries - 1:
                w = "Could not take data. Something might be wrong!"
                if raiseErrors:
                    raise DeviceError(w)
                log.warning(w)
                return
            continue

        aux = data["aux"]
        # how do we check whether there is a meaningful peak?
        # if there is one as we expect it should be pretty simple
        # most values are going to be similar, except for peaks, therefore we use the median:
        median = aux.median()
        # now check the absolute differences of minima and maxima to find peaks
        absmin = np.abs(median - aux.min())
        absmax = np.abs(median - aux.max())
        # in any good signal there should be a significant difference between these distances
        # if not, you're probably looking at white noise
        if np.abs(absmin - absmax) > 5 * aux.std():
            break

        log.warning(f"Try {n+1}...")
        if n == tries - 1:
            log.warning("ABORTING: Could not find reasonable peak in 10 tries.")
            w = f"""Could not find a reasonable threshold, as distances of minimum and maximum are very close (within five standard deviations).
                Values of last try:
                Distance of minimum to median: {absmin:3f}
                Distance of maximum to median: {absmax:3f}
                Difference of the two: {np.abs(absmin - absmax):3f}
                5 Std: {5*aux.std():3f}
                Values remain unchanged: treshold {self._autolock["threshold"]} break {self._autolock["threshold_break"]} greater {self._autolock["greater"]}
                """
            log.warning(w)
            if raiseErrors:
                raise AutoLockAnalysisError(w)
            return

    # check peak direction
    if absmin > absmax:  # the peaks are minima
        # use the minimum as threshold, add some low percentage tolerance to the values
        self.lockGreater = 0
        self.lockThreshold = np.round(
            aux.min() + (1 - settings.LOCK_THRESHOLD) * absmin, 3
        )
        self.lockThresholdBreak = np.round(
            aux.min() + (1 - settings.LOCK_THRESHOLD_BREAK) * absmin, 3
        )
    else:  # the peaks are maxima
        self.lockGreater = 1
        self.lockThreshold = np.round(
            aux.max() - (1 - settings.LOCK_THRESHOLD) * absmax, 3
        )
        self.lockThresholdBreak = np.round(
            aux.max() - (1 - settings.LOCK_THRESHOLD_BREAK) * absmax, 3
        )
    w = f"""
        Found greater {self._autolock["greater"]} with threshold {self._autolock["threshold"]:3f}.
        Median was {median:3f} with min/max {aux.min():3f} and {aux.max():3f}.
        """
    log.warning(w)
