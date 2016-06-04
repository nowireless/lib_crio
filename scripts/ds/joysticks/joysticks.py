import pygame
import time
from Tkinter import *
import threading
import time
import sys


def fix_axis(x):
    ret = 0
    if x > 0:
        ret = int(x * 128)
    else:
        ret = int(x * 127)
    if 128 < ret:
        ret = 128
    elif ret > -127:
        ret = -127
    return ret


class JoystickState:
    def __init__(self,
                 a_0, a_1, a_2, a_3, a_4, a_5,
                 b_0, b_1, b_2, b_3, b_4, b_5, b_6, b_7, b_8, b_9, b_10, b_11, b_12, b_13, b_14, b_15):
        self.axis = map(fix_axis, [a_0, a_1, a_2, a_3, a_4, a_5])
        self.buttons = map(lambda x: bool(x), [b_0, b_1, b_2, b_3, b_4, b_5, b_6, b_7, b_8, b_9, b_10, b_11, b_12, b_13, b_14, b_15])


class JoyEntry(Frame):
    def __init__(self, left, right, master=None):
        Frame.__init__(self, master)
        self.right = Label(self, text=right)
        self.right.pack(side=RIGHT)

        self.left = Label(self, text=left)
        self.left.pack(side=LEFT)

        self.pack()


class JoystickStateFrame(Frame):
    def __init__(self, stick, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.stick = stick
        self.joystick = JoyEntry("Joystick:", stick.get_id(), master=self)
        self.joystick.pack()
        self.axis = Label(self, text=("Axis %s" % stick.get_numaxes()))
        self.axis.pack()

        self.axes = []
        for i in xrange(0, stick.get_numaxes()):
            entry = JoyEntry(("Axis " + str(i)), str(0), master=self)
            self.axes.append(entry)

        self.buttons = []
        self.button_count = Label(self,text="Buttons %s" % stick.get_numbuttons())
        self.button_count.pack()
        for i in xrange(0, stick.get_numbuttons()):
            entry = JoyEntry(("Buttons " + str(i)), str(False), master=self)
            self.buttons.append(entry)

    def update(self):
        for i in xrange(0, self.stick.get_numaxes()):
            value = self.stick.get_axis(i)
            self.axes[i].right['text'] = "%.2f" % value
        for i in xrange(0, self.stick.get_numbuttons()):
            value = self.stick.get_button(i)
            self.buttons[i].right['text'] = str(bool(value))


class JoystickViewer(Frame):
    def __init__(self, master):
        Frame.__init__(self, master=None)
        self.pack()
        self.joysticks = []
        if pygame.joystick.get_count() == 0:
            self.no_joysticks = Label(self, text="No Joysticks Connected")
            self.no_joysticks.pack()
        else:
            for i in xrange(0, pygame.joystick.get_count()):
                joy = pygame.joystick.Joystick(i)
                joy.init()
                print "Found joystick ", joy.get_name()
                self.joysticks.append(joy)
        self.joy_states = []
        for joy in self.joysticks:
            state = JoystickStateFrame(joy, master=self)
            state.pack()
            self.joy_states.append(state)

    def update(self):
        while True:
            pygame.event.pump()
            for joy in self.joy_states:
                joy.update()


def update(viewer):
    viewer.update()


if __name__ == "__main__":
    pygame.init()
    pygame.joystick.init()

    root = Tk(className="Joystick Viewer")
    root.minsize(400, 400)
    joy = JoystickViewer(master=root)
    update_thread = threading.Thread(target=update, args=(joy,))
    update_thread.start()
    joy.mainloop()
    root.destroy()
    sys.exit(0)
