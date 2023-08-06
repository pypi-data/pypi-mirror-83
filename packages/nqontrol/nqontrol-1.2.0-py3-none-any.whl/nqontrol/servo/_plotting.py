# pylint: disable=protected-access,redefined-outer-name,cyclic-import
import logging as log
import multiprocessing as mp
from time import sleep, time
from typing import Optional

import numpy as np
from matplotlib import pyplot as plt
from pandas import DataFrame
from scipy.signal import find_peaks

from nqontrol.general import settings
from nqontrol.general.errors import Bug, UserInputError
from nqontrol.general.helpers import convertFloat2Volt

#########################################
# Realtime plotting and fifo
#########################################


def _calculateFifoStepsize(self):
    # in ramp mode, we would like the monitor output to match at least one ramp cycle
    # in reality we will need 2 to make sure it always finds minima
    # so: what fifo stepsize is required for given ramp settings
    factor = 2.2
    fifoStepsize = int(factor * 4 / self._autolock["stepsize"] / settings.FIFO_MAXLEN)
    if fifoStepsize == 0:
        fifoStepsize = 1
    log.debug(
        (
            "Calculated new fifo stepsize",
            fifoStepsize,
            "with lock step",
            self._autolock["stepsize"],
        )
    )
    return fifoStepsize


def _updateFifoStepsize(self):
    if self.fifoEnabled and self._autolock["search"]:
        self.enableFifo(self._calculateFifoStepsize())


def _calculateRefreshTime(self):
    bufferFillingLevel = 0.5
    if self._autolock["search"]:
        bufferFillingLevel = 1

    refreshTime = (
        self._fifo["stepsize"]
        / settings.SAMPLING_RATE
        * bufferFillingLevel
        * settings.FIFO_MAXLEN
    )

    if refreshTime < self._MIN_REFRESH_TIME:
        refreshTime = self._MIN_REFRESH_TIME
    self.realtime["refreshTime"] = refreshTime


@property
def _fifoBufferSize(self) -> int:
    """Get the current size of the fifo buffer on ADwin."""
    return self._adw.Fifo_Full(settings.DATA_FIFO)


@property
def fifoStepsize(self) -> int:
    """
    Setter DEPRECATED: Use :obj:`nqontrol.Servo.enableFifo()`

    Trigger ADwin to write the three channels of this servo to the FIFO buffer to read it with the PC over LAN.

    :code:`input`, :code:`aux` and :code:`output` will be sent.

    :getter: Number of program cycles between each data point.
    :setter: Set the number or choose `None` to disable the FiFo output.
    :type: :obj:`int`
    """
    return self._fifo["stepsize"]


@property
def realtimeEnabled(self) -> bool:
    if self.realtime["enabled"] and self.fifoEnabled:
        return True

    return False


@property
def fifoEnabled(self) -> bool:
    if self._adw.Get_Par(settings.PAR_ACTIVE_CHANNEL) == self._channel:
        return True

    return False


def enableFifo(self, fifo_stepsize: Optional[int] = None):
    """
    Trigger ADwin to write the three channels of this servo to the
    FIFO buffer to read it with the PC over LAN.

    :code:`input`, :code:`aux` and :code:`output` will be sent.

    Parameters
    ----------
        fifo_stepsize: :obj:`int`
            Number of program cycles between each data point.
            If unset it will stay the same or use the default ({})

    """.format(
        self.DEFAULT_FIFO_STEPSIZE
    )
    if fifo_stepsize is None:
        fifo_stepsize = self._fifo["stepsize"]
    if not isinstance(fifo_stepsize, int) or fifo_stepsize < 1:
        raise ValueError(
            f"The stepsize must be a positive integer, but it was: {fifo_stepsize}"
        )

    self._fifo["stepsize"] = fifo_stepsize
    # Enable on adwin
    self._adw.Set_Par(settings.PAR_ACTIVE_CHANNEL, self._channel)
    # stepsize will never be None
    self._adw.Set_Par(settings.PAR_FIFOSTEPSIZE, fifo_stepsize)
    # set refresh time
    self._calculateRefreshTime()
    # Create local buffer
    self._createDataFrame()


def disableFifo(self):
    """Disable the FiFo output if it is enabled on this channel."""
    if self.fifoEnabled:
        # Disable on adwin only if this channel is activated
        self._adw.Set_Par(settings.PAR_ACTIVE_CHANNEL, 0)
        self._adw.Set_Par(settings.PAR_FIFOSTEPSIZE, 0)
        # Destroy local buffer
        self._fifoBuffer = None


def _readoutNewData(self, n: int) -> DataFrame:
    m: int = self._fifoBufferSize
    if n > m:
        n = m

    newData: DataFrame = DataFrame(columns=self.DEFAULT_COLUMNS)

    if n == 0:
        log.warning("I should readout 0 data.")
        return newData

    # Saving 3 16bit channels in a 64bit long variable
    # Byte    | 7 6 | 5 4   | 3 2 | 1 0    |
    # Channel |     | input | aux | output |
    combined = np.array(self._adw.GetFifo_Double(settings.DATA_FIFO, n)[:], dtype="int")

    def extractValue(combined, offset=0):
        shifted = np.right_shift(combined, offset)
        return np.bitwise_and(shifted, 0xFFFF)

    log.debug(extractValue(combined[0], 32))
    log.debug(extractValue(combined[0], 16))
    log.debug(extractValue(combined[0]))

    newData["input"] = convertFloat2Volt(
        extractValue(combined, 32), self._state["inputSensitivity"]
    )
    newData["aux"] = convertFloat2Volt(
        extractValue(combined, 16), self._state["auxSensitivity"]
    )
    newData["output"] = convertFloat2Volt(extractValue(combined))

    log.debug(newData["input"][0])
    log.debug(newData["aux"][0])
    log.debug(newData["output"][0])

    return newData


def _prepareContinuousData(self) -> None:
    n: int = self._fifoBufferSize
    if n == 0:
        return

    maxLen: int = settings.FIFO_MAXLEN
    buf: DataFrame = DataFrame()

    if n >= maxLen:
        n = maxLen
    else:
        # local copy of the `maxlen-n` newest entries.
        if settings.FIFO_MAXLEN < len(buf) + n:
            raise Bug(
                f"That check should not fail. maxlen = {settings.FIFO_MAXLEN}, "
                "len(buf) = {len(DataFrame(self._fifoBuffer[n:]))}, "
                "lenBefore = {len(self._fifoBuffer)}, n = {n}"
            )

    # Read new data
    newData: DataFrame = self._readoutNewData(n)
    # Append to the local DataFrame
    self._fifoBuffer = buf.append(newData, sort=False)

    newLen: int = len(self._fifoBuffer)
    if newLen > settings.FIFO_MAXLEN:
        raise Bug(
            "That is a bug. Please report it. "
            "len(newData): {len(newData)}, len(buf): {len(buf)}"
        )

    dt: float = self._timeForFifoCycles(1)
    self._fifoBuffer.index = np.arange(0, newLen * dt, dt)[:newLen]


def _prepareRampData(self, tries: int = 3) -> None:
    if tries < 1:
        log.warning("tries must be at least 1.")
        tries = 1

    found_min = False

    for _ in range(tries):
        # we used some calculations here before, better to just use a fixed value
        n_data_buffer = settings.FIFO_MAXLEN
        log.debug(f"Buffer points: {n_data_buffer}")
        self._waitForBufferFilling(n=n_data_buffer)
        # Take data
        newData = self._readoutNewData(n_data_buffer)
        log.debug(f"length of readout ramp data {len(newData)}")
        # Find the first minimum
        try:
            minima, _ = find_peaks(-newData["output"])
            log.debug(f"Minima: {minima}")
            _ = minima[0]
            found_min = True
            break
        except IndexError:
            log.warning("Could not find a ramp minimum.")

    if not found_min:
        log.warning(f"Unable to find the ramp minimum in {tries} tries. Giving up...")
        return

    try:
        second_min = minima[1]
    except IndexError:
        log.warning("No second minimum found.")
        # in case you want to test this:

        # newData.to_csv("test123")
        second_min = None
    # Copy data from the first minimum untill the end
    localBuffer = DataFrame(newData[minima[0] : second_min])
    log.debug(f"Local buffer length {len(localBuffer)}")

    # Calculate times for the index
    length = len(localBuffer)
    dt = self._timeForFifoCycles(1)
    localBuffer.index = np.arange(0, length * dt, dt)[:length]

    self._fifoBuffer = DataFrame(localBuffer)


def _timeForFifoCycles(self, n):
    log.debug((n, self._fifo["stepsize"]))
    return n * self._fifo["stepsize"] / settings.SAMPLING_RATE


def _waitForBufferFilling(self, n: int = None, refill: bool = True):
    if n is None:
        n = settings.FIFO_MAXLEN
    if refill:
        cycles = n
    else:
        bufferSize = self._fifoBufferSize
        if bufferSize < n:
            cycles = n - bufferSize
        else:
            return
    sleep(self._timeForFifoCycles(cycles))


def _createDataFrame(self):
    data = {"input": [], "aux": [], "output": []}
    self._fifoBuffer = DataFrame(data=data)


def takeData(self) -> DataFrame:
    """Take data from ADwin.

    It will return a DataFrame containing the columns input, aux and output.

    Returns
    -------

    returnVar : DataFrame
    """
    self._readLockControl()
    if not self.fifoEnabled:
        log.warning("The FiFo output was not activated. Enabling now...")
        self.enableFifo()
    if self._autolock["search"] and self._autolock["amplitude"] > 0:
        self._prepareRampData()
    else:
        self._prepareContinuousData()
    return self._fifoBuffer[self.realtime["ydata"]]


def _realtimeLoop(self):
    try:
        gui_breaks = (KeyboardInterrupt,)
        from tkinter import TclError  # pylint: disable=import-outside-toplevel

        gui_breaks += (TclError,)
    except ImportError:
        pass

    # plotting loop
    assert self.realtimeEnabled, "Realtime should be enabled when starting the loop."

    # generate plot
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.ion()  # interactive mode

    try:
        while self.realtimeEnabled:
            timeStart = time()
            ax.clear()
            if self.realtime["ylim"] is None:
                ax.set_ylim(auto=True)
            else:
                ax.set_ylim(self.realtime["ylim"])
            ax.plot(self.takeData())
            ax.legend(self.realtime["ydata"], loc=1)

            timePause = self.realtime["refreshTime"] - time() + timeStart
            if timePause <= 0:
                timePause = 1e-6

            plt.pause(timePause)
    except gui_breaks:
        plt.close("all")
        log.info("Plot closed")
    finally:
        # Ensure that `realtime` is disabled if the plot is closed
        log.info("Stop plotting...")
        self.realtime["enabled"] = False
        self._subProcess = None


def stopRealtimePlot(self):
    """Stop the realtime plot."""
    self.realtime["enabled"] = False
    if self._subProcess is not None:
        self._subProcess.join()
    else:
        log.warning("No subprocess had been started.")
        return
    assert not self._subProcess.is_alive(), "The subprocess should be finished!"


def realtimePlot(self, ydata=None, refreshTime=None, multiprocessing=True):
    """
    Enable parallel realtime plotting.

    To stop the running job call `stopRealtimePlot()`.

    Parameters
    ----------
    ydata: :obj:`list` of :obj:`str`
        Choose the data to be plotted: :code:`['input', 'aux', 'output']`.
    refreshTime: :obj:`float`
        Sleeping time (s) between plot updates.

    """
    if self._subProcess is not None and self._subProcess.is_alive():
        raise UserInputError(
            "Do you really want more than one plot of the same data? It is not implemented..."
        )
    if self._fifoBuffer is None:
        log.info(
            "Enabling the FiFo buffer with a default step size of {}...".format(
                self.DEFAULT_FIFO_STEPSIZE
            )
        )
        self.enableFifo()

    # Update local parameters
    self.realtime["enabled"] = True
    if ydata:
        self.realtime["ydata"] = ydata
    if refreshTime:
        self.realtime["refreshTime"] = refreshTime

    # Start plotting process
    if multiprocessing:
        self._subProcess = mp.Process(target=self._realtimeLoop)
        self._subProcess.start()
    else:
        self._realtimeLoop()
