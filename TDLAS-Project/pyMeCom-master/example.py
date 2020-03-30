"""

"""
import logging
from mecom import MeCom, ResponseException, WrongChecksum
from serial import SerialException
import time

# default queries from command table below
DEFAULT_QUERIES = [
    "loop status",
    "object temperature",
    "target object temperature",
    "output current",
    "output voltage"
]

# syntax
# { display_name: [parameter_id, unit], }
COMMAND_TABLE = {
    "loop status": [1200, ""],
    "object temperature": [1000, "degC"],
    "target object temperature": [1010, "degC"],
    "output current": [1020, "A"],
    "output voltage": [1021, "V"],
    "sink temperature": [1001, "degC"],
    "ramp temperature": [1011, "degC"],
}


class MeerstetterTEC(object):
    """
    Controlling TEC devices via serial.
    """

    def _tearDown(self):
        self.session().stop()

    def __init__(self, port="COM4", channel=1, queries=DEFAULT_QUERIES, *args, **kwars):
        assert channel in (1, 2)
        self.channel = channel
        self.port = port
        self.queries = queries
        self._session = None
        self._connect()

    def _connect(self):
        # open session
        self._session = MeCom(serialport=self.port)
        # get device address
        self.address = self._session.identify()
        logging.info("connected to {}".format(self.address))

    def session(self):
        if self._session is None:
            self._connect()
        return self._session

    def get_data(self):
        data = {}
        for description in self.queries:
            id, unit = COMMAND_TABLE[description]
            try:
                value = self.session().get_parameter(parameter_id=id, address=self.address, parameter_instance=self.channel)
                data.update({description: (value, unit)})
            except (ResponseException, WrongChecksum) as ex:
                self.session().stop()
                self._session = None
        return data

    def set_temp(self, value):
        """
        Set object temperature of channel to desired value.
        :param value: float
        :param channel: int
        :return:
        """
        # assertion to explicitly enter floats
        assert type(value) is float
        logging.info("set object temperature for channel {} to {} C".format(self.channel, value))
        return self.session().set_parameter(parameter_id=3000, value=value, address=self.address, parameter_instance=self.channel)



    def set_current(self, value):
        """
        Set object current of channel to desired value.
        :param value: float
        :param channel: float
        :return:
        """
        # assertion to explicitly enter floats
        assert type(value) is float
        logging.info("set object current for channel {} to {} A".format(self.channel, value))
        return self.session().set_parameter(parameter_id=2020, value=value, address=self.address, parameter_instance=self.channel)

    def set_voltage(self, value):
        """
        Set object voltage of channel to desired value.
        :param value: float
        :param channel: float
        :return:
        """
        # assertion to explicitly enter floats
        assert type(value) is float
        logging.info("set object voltage for channel {} to {} A".format(self.channel, value))
        return self.session().set_parameter(parameter_id=2021, value=value, address=self.address, parameter_instance=self.channel)

    def _set_enable(self, enable=True):
        """
        Enable or disable control loop
        :param enable: bool
        :param channel: int
        :return:
        """
        value, description = (1, "on") if enable else (0, "off")
        logging.info("set loop for channel {} to {}".format(self.channel, description))
        return self.session().set_parameter(value=value, parameter_name="Status", address=self.address, parameter_instance=self.channel)

    def _set_enable_current(self, enable=True):
        """
        Enable or disable control loop
        :param enable: bool
        :param channel: int
        :return:
        """
        value, description = (0, "on") if enable else (1, "off")
        logging.info("set loop for channel {} to {}".format(self.channel, description))
        return self.session().set_parameter(value=value, parameter_name="Input Selection", address=self.address, parameter_instance=self.channel)

    def enable(self):
        return self._set_enable(True)

    def disable(self):
        return self._set_enable(False)


# start logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s:%(module)s:%(levelname)s:%(message)s")

# initialize controller
mc = MeerstetterTEC()
mc._tearDown()
mc._connect()
# get the values from DEFAULT_QUERIES
print(mc.get_data())
mc.set_temp(25.0)
mc.enable()

time.sleep(3)
print(mc.get_data())
#mc.set_voltage(10.0)
#mc._set_enable_current(True)
#mc.set_current(0.1)
#mc._set_enable_current(True)
#print(mc.get_data())
mc._tearDown()

