# pylint: disable=protected-access,redefined-outer-name,cyclic-import

from nqontrol.general import settings

from ._feedbackController import FeedbackController


########################################
# Temperature feedback
########################################
@property
def tempFeedback(self):
    """Return or set temperature feedback server associated with the servo.

    :getter: Return the :obj:`FeedbackController`.
    :setter: Set a new :obj:`FeedbackController`.
    :type: :obj:`FeedbackController`.
    """
    return self._tempFeedback


def tempFeedbackStart(  # pylint: disable=too-many-arguments
    self,
    dT=None,
    mtd=None,
    voltage_limit=None,
    server=settings.DEFAULT_TEMP_HOST,
    port=settings.DEFAULT_TEMP_PORT,
    update_interval=None,
):
    """Start the temperature feedback server. Setup a server if it hasn't been previously set.

    Parameters
    ----------
    dT : :obj:`float`
        Description of parameter `dT`.
    mtd : :obj:`tuple`
        (1, 1)
    voltage_limit : :obj:`float`
        The maximum voltage to which one can go using the temperature control (the default is 5).
    server : type
        Description of parameter `server` (the default is settings.DEFAULT_TEMP_HOST).
    port : type
        Description of parameter `port` (the default is settings.DEFAULT_TEMP_PORT).
    update_interval : :obj:`float`
        Description of parameter `update_interval` (the default is 1).

    """
    if dT is None:
        dT = self._tempFeedbackSettings["dT"]
    if mtd is None:
        mtd = self._tempFeedbackSettings["mtd"]
    if voltage_limit is None:
        voltage_limit = self._tempFeedbackSettings["voltage_limit"]
    if update_interval is None:
        update_interval = self._tempFeedbackSettings["update_interval"]

    self._tempFeedback = FeedbackController(
        self, dT, mtd, voltage_limit, server, port, update_interval
    )
    self.tempFeedback.start()


def tempFeedbackStop(self):
    """Stop the tempFeedback server."""
    self.tempFeedback.enabled = False
    self.tempFeedback.join()
    self._tempFeedback = None
