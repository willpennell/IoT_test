from gpiozero import MotionSensor


class PIRSensor:

    def __int__(self):
        self.pir = MotionSensor(4)

    def set_up(self):
        self.pir.wait_for_no_motion(timeout=10)

    def listen(self):
        self.pir.wait_for_motion()

    def package(self, time, ip):
        return str(self.pir.motion_detected, time, ip)


