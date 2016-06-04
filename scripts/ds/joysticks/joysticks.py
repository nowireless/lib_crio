from threading import Thread
from threading import RLock
import pygame
import time


def fix_axis(x):
    ret = 0
    if x > 0:
        ret = int(x * 128)
    else:
        ret = int(x * 127)
    if 128 < ret:
        ret = 128
    elif ret < -127:
        ret = -127
    return ret


class JoystickState:
    def __init__(self, axis, buttons):
        self.axis = map(fix_axis, axis)
        self.buttons = map(lambda x: bool(x), buttons)


def make_state(stick):
    #print "Make"
    axes = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    buttons = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    if stick is not None:
        for i in xrange(0, stick.get_numaxes()):
            if i == len(axes):
                break
            axes[i] = stick.get_axis(i)
            print axes
        for i in xrange(0, stick.get_numbuttons()):
            if i == len(buttons):
                break
            buttons[i] = stick.get_button(i)
    return JoystickState(axes, buttons)

class JoystickUpdateThread(Thread):
    def __init__(self):
        super(JoystickUpdateThread, self).__init__()
        self.running = True
        self.__lock = RLock()
        self.__joysticks = []
        self.joysticks = []

    def run(self):
        pygame.init()
        pygame.joystick.init()
        if pygame.joystick.get_count() == 0:
            print "No joysticks found"
        else:
            for i in xrange(0, pygame.joystick.get_count()):
                joy = pygame.joystick.Joystick(i)
                joy.init()
                self.__joysticks.append(joy)
                self.joysticks = make_state(None)
        self.running = True
        while self.running:
            pygame.event.pump()
            self.lock()
            self.joysticks = []
            for joy in self.__joysticks:
                self.joysticks.append(make_state(joy))

            self.unlock()
            time.sleep(0.01)

    def stop(self):
        self.running = False

    def lock(self):
        self.__lock.acquire()

    def unlock(self):
        self.__lock.release()

