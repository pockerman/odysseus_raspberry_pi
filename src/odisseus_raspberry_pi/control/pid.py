"""
PID controller implementation
"""


class PIDControl:
    """
    Simple implementation of PID controller
    """

    NAMES = ["Kp", "Ki", "Kd"]

    def __init__(self, Kp, Ki, Kd):
        self._properties = dict()
        self._error = 0.0

        if Kp is not None:
            self.set_property('Kp', Kp)

        if Ki is not None:
            self.set_property('Ki', Ki)

        if Kd is not None:
            self.set_property('Kd', Kd)

    def execute_from_cmd(self, cmd, **kwargs):

        if cmd.get_name() == 'PropulsionCmd':
            cmd_speed_value = cmd.speed_value()
            actual_speed = kwargs['odisseus_speed']
            rslt = self.execute(cmd_speed_value - actual_speed, **kwargs)

    def execute(self, error, **kwargs):

        rslt = 0.0

        if self.has_property('Kd') and 'dt' in kwargs.keys():
            delta_error = error - self._error
            dt = kwargs['dt'] # what happens here if dt = 0.0
            rslt += self.get_property('Kd') * (delta_error/dt)

        if self.has_property('Kp'):
            rslt += self.get_property('Kp')*error

        # accumulate  the error
        self._error += error

        if self.has_property('Ki'):
            rslt += self.get_property('Ki') * self._error

        return rslt

    def get_property(self, name):
        return self._properties[name]

    def set_property(self, name, item):
        self._properties[name] = item

    def has_property(self, name):
        return name in self._properties.keys()

    def __getitem__(self, item):
        self.get_property(name=item)

    def __setitem__(self, key, value):
        self.set_property(name=key, item=value)

