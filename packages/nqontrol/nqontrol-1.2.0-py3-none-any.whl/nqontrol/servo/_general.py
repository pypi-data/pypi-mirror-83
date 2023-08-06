# pylint: disable=protected-access,redefined-outer-name,cyclic-import
import logging as log
import multiprocessing as mp

from ADwin import ADwinError
from openqlab.analysis.servo_design import ServoDesign

from nqontrol.general import settings
from nqontrol.general.errors import ConfigurationError
from nqontrol.general.helpers import convertFrequency2Stepsize

_DONT_SERIALIZE = [
    "_manager",
    "_adw",
    "_subProcess",
    "_fifoBuffer",
    "_tempFeedback",
]
REALTIME_DICTS = ["realtime", "_fifo"]
_JSONPICKLE = ["servoDesign"]
_MIN_REFRESH_TIME = 0.02
_DEFAULT_FILTERS = [
    [1, 0, 0, 0, 0],
    [1, 0, 0, 0, 0],
    [1, 0, 0, 0, 0],
    [1, 0, 0, 0, 0],
    [1, 0, 0, 0, 0],
]
DEFAULT_COLUMNS = ["input", "aux", "output"]
_manager = mp.Manager()
realtime = _manager.dict(
    {"enabled": False, "ydata": DEFAULT_COLUMNS, "ylim": None, "refreshTime": 0.1}
)
DEFAULT_FIFO_STEPSIZE = 10
"""
Control realtime plotting.

.. code:: python

    realtime = {
        'enabled': False,
        'ydata': ['input', 'aux', 'output'],
        'ylim': None,
        'refreshTime': 0.1,
    }
"""

MAX_CHANNELS = 8


@property
def channel(self):
    return self._channel


########################################
# Predefined methods
########################################
def __init__(  # pylint: disable=too-many-arguments
    self,
    channel,
    adw,
    applySettings=None,
    offset=0.0,
    gain=1.0,
    filters=None,
    name=None,
):
    """
    Create the servo object, also on ADwin.

    `readFromFile` overwrites all other parameters.

    Parameters
    ----------
    deviceNumber: Number of the ADwin-Pro device.
    channel:      Channel used for the Servo.
                  Possible is `1..8`
                  Channel number is used for input,
                  output and process number
    offset=0.0:   Overall offset
    filters:      Filter coefficient matrix. Default is a 0.0 matrix.

    """

    if not 1 <= channel <= self.MAX_CHANNELS:
        raise ValueError(f"There are max {self.MAX_CHANNELS} channels.")
    self._channel = channel
    if name is None:
        self.name = "Servo " + str(channel)
    else:
        self.name = name
    if filters is None:
        filters = self._DEFAULT_FILTERS

    # State dictionaries
    self._state = dict(
        {
            # Control parameters
            "offset": offset,
            "gain": gain,
            "filters": filters,
            "inputSensitivity": 0,
            "auxSensitivity": 0,
            # Control flags
            "filtersEnabled": [False] * 5,
            "auxSw": False,
            "offsetSw": False,
            "outputSw": False,
            "inputSw": False,
        }
    )
    self._autolock = dict(
        {
            "search": 0,
            "locked": 0,
            "relock": 0,
            "greater": 1,
            "rampmode": 0,
            "threshold": 0,
            "threshold_break": 0,
            "amplitude": 10,
            "offset": 0,
            "stepsize": convertFrequency2Stepsize(30),
        }
    )
    self._fifo = self._manager.dict({"stepsize": self.DEFAULT_FIFO_STEPSIZE})
    if settings.FIFO_MAXLEN * 2 > settings.FIFO_BUFFER_SIZE:
        raise ConfigurationError(
            "FIFO_BUFFER_SIZE must be at least twice as big as _fifo['maxlen']."
        )
    self._fifoBuffer = None
    self._subProcess = None

    # has to be initalized as None / could maybe include in the loading?
    self._tempFeedback = None
    self._tempFeedbackSettings = self._manager.dict(
        {"dT": None, "mtd": None, "update_interval": 1, "voltage_limit": 5}
    )

    # ServoDesign object
    self.servoDesign: ServoDesign = ServoDesign()

    # Use adwin object
    self._adw = adw

    # initialize lock values

    try:
        if applySettings:
            # loadSettings calls `_sendAllToAdwin()`
            self.loadSettings(applySettings)
        else:
            self._sendAllToAdwin()
    except ADwinError as e:
        log.error(f"{e} Servo {self._channel}: Couldn't write to ADwin.")


def __repr__(self):
    """Name of the object."""
    return f"Name: {self.name}, channel: {self._channel}"
