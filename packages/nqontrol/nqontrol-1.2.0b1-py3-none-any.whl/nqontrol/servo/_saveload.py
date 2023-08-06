# pylint: disable=protected-access,redefined-outer-name,cyclic-import
import json
import multiprocessing as mp

import jsonpickle


########################################
# Save and load settings
########################################
def _applySettingsDict(self, data):
    # Don't import the channel because it isn't possible to change it.
    DONT_SERIALIZE = self._DONT_SERIALIZE + ["_channel"] + ["name"]
    # overwrite name from save file only if no other name has been set specifically in settings
    if data.get("name") is not None and data.get("name") != f"Servo {self._channel}":
        self.name = data.get("name")
    for d in self.__dict__:
        value = data.get(d.__str__())
        if (d.__str__() not in DONT_SERIALIZE) and (value is not None):
            if d.__str__() in self._JSONPICKLE:
                self.__dict__[d.__str__()] = jsonpickle.decode(value)
            elif isinstance(value, dict):
                self.__dict__[d.__str__()].update(value)
            else:
                self.__dict__[d.__str__()] = value


def getSettingsDict(self):
    """
    Get a dict with all servo settings.

    Returns
    -------
    :obj:`dict`
        Return all important settings for the current servo state.
    """
    # load state from adwin
    self._readAllFromAdwin()

    # save settings
    data = {}
    for d in self.__dict__:
        if d.__str__() not in self._DONT_SERIALIZE:
            value = self.__dict__[d.__str__()]
            # Convert dicts from multiprocessing
            if isinstance(value, (dict, mp.managers.DictProxy)):
                value = dict(value)
            elif d.__str__() in self._JSONPICKLE:
                value = jsonpickle.encode(value)
            data[d.__str__()] = value
    return data


def saveJsonToFile(self, filename):
    """
    Save this single servo as json to a file.

    Parameters
    ----------
    filename: :obj:`str`
        Filename to save the json file.

    """
    data = {self.__class__.__name__: self.getSettingsDict()}
    with open(filename, "w+") as file:
        json.dump(data, file, indent=2)


def loadSettings(self, applySettings):
    """
    Load settings from file or dict.

    Not reading the channel, it can only be set on creating a servo object.

    Parameters
    ----------
    applySettings: :obj:`str` or :obj:`dict`
        Settings to load for this servo.

    """
    if isinstance(applySettings, dict):
        load_settings = applySettings
    elif isinstance(applySettings, str):
        load_settings = self._readJsonFromFile(applySettings)
    else:
        raise TypeError("You can only apply settings from a file or a dict.")

    self._applySettingsDict(load_settings)
    self._sendAllToAdwin()


def _readJsonFromFile(self, filename):
    """
    Read settings from a single servo file.

    return: dict with only the servo settings
    """
    try:
        with open(filename, "r") as file:
            data = json.load(file)
    except FileNotFoundError as e:
        raise e

    if not data.get(self.__class__.__name__):
        raise SyntaxError("Invalid file.")

    return data[self.__class__.__name__]
