"""Servo class."""
# pylint: disable=import-outside-toplevel,too-few-public-methods,cyclic-import


class Servo:  # pylint: disable=too-many-instance-attributes,too-many-public-methods
    """
    Servo object that communicates with a control channel of the ADwin.

    `readFromFile` overwrites all other parameters.

    Parameters
    ----------
    channel: :obj:`int`
        Channel used vor the Servo.
        Possible is `1..8`
        Channel number is used for input,
        output and process number
    adw: :obj:`ADwin`
        For all servos of a :obj:`ServoDevice` to use the same
        :obj:`ADwin` object,
        it is necessary to pass an ADwin object.
    applySettings: :obj:`str` or `dict`
        Apply settings directly from file or dict.
    offset: :obj:`offset`
        Overall offset.
    gain: :obj:`float`

    filters: 5 * 5 :obj:`list`
        Filter coefficient matrix. Default is a 0.0 matrix.
    name: :obj:`str`
        Choose an optional name for this servo.

    """

    from ._general import (
        _DONT_SERIALIZE,
        REALTIME_DICTS,
        _JSONPICKLE,
        _MIN_REFRESH_TIME,
        _DEFAULT_FILTERS,
        DEFAULT_COLUMNS,
        _manager,
        realtime,
        DEFAULT_FIFO_STEPSIZE,
        MAX_CHANNELS,
        __init__,
        __repr__,
        channel,
    )

    from ._state import (
        _sendAllToAdwin,
        _readAllFromAdwin,
        _triggerReload,
        _readFilterControl,
        _sendFilterControl,
        filterStates,
        filterState,
        auxSw,
        offsetSw,
        outputSw,
        inputSw,
        offset,
        gain,
        inputSensitivity,
        auxSensitivity,
        filters,
        applyServoDesign,
    )

    from ._autolock import (
        _lockIter,
        _testLockOutput,
        _readLockControl,
        _sendLockControl,
        lockSearch,
        locked,
        relock,
        lockGreater,
        lockRampmode,
        _initLockValues,
        lockThreshold,
        lockThresholdBreak,
        lockAmplitude,
        lockOffset,
        lockStepsize,
        lockFrequency,
        autolock,
        _autolockOptions,
        enableRamp,
        disableRamp,
        _prepareLockData,
        lockAnalysis,
    )

    from ._saveload import (
        _applySettingsDict,
        getSettingsDict,
        saveJsonToFile,
        loadSettings,
        _readJsonFromFile,
    )

    from ._plotting import (
        _calculateFifoStepsize,
        _updateFifoStepsize,
        _calculateRefreshTime,
        _fifoBufferSize,
        fifoStepsize,
        realtimeEnabled,
        fifoEnabled,
        _prepareRampData,
        enableFifo,
        disableFifo,
        _readoutNewData,
        _prepareContinuousData,
        _timeForFifoCycles,
        _waitForBufferFilling,
        _createDataFrame,
        takeData,
        _realtimeLoop,
        stopRealtimePlot,
        realtimePlot,
    )

    from ._temp_feedback import (
        tempFeedback,
        tempFeedbackStart,
        tempFeedbackStop,
    )
