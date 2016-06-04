from Tkinter import Frame
from Tkinter import Button
from Tkinter import Tk
from crio.communication import DS
from joysticks.joysticks import JoystickUpdateThread
import sys


class App(Frame):
    def robot_enable(self):
        print "Enable"
        self.ds.state_lock.acquire()
        self.ds.state.enable()
        self.ds.state_lock.release()

    def robot_disable(self):
        print "Disable"
        self.ds.state_lock.acquire()
        self.ds.state.disable()
        self.ds.state_lock.release()

    def robot_reset(self):
        print "Reset"
        self.ds.state_lock.acquire()
        self.ds.state.reset_robot()
        self.ds.state_lock.release()

    def exit(self):
        self.ds.stop()
        print "Quit"
        self.quit()
        sys.exit(0)

    def create_widgets(self):
        self.QUIT = Button(self)
        self.QUIT["text"] = "QUIT"
        self.QUIT["fg"] = "red"
        self.QUIT["command"] = self.exit

        self.QUIT.pack({"side":"left"})

        self.disable = Button(self)
        self.disable["text"] = "Disable"
        self.disable["command"] = self.robot_disable
        self.disable.pack({"side":"left"})

        self.enable = Button(self)
        self.enable["text"] = "Enable"
        self.enable["command"] = self.robot_enable
        self.enable.pack({"side":"left"})

        self.reset_button = Button(self)
        self.reset_button["text"] = "Reset"
        self.reset_button["command"] = self.robot_reset
        self.reset_button.pack({"side":"left"})

    def __init__(self, master=None):
        Frame.__init__(self, master)

        self.ds = DS(3081, joystick_thread=JoystickUpdateThread())
        self.ds.start()
        self.QUIT = None
        self.enable = None
        self.disable = None
        self.reset_button = None
        self.pack()
        self.create_widgets()


if __name__ == "__main__":
    root = Tk(className="cRIO DS")
    app = App(master=root)
    app.mainloop()
    root.destroy()