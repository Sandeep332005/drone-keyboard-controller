import time
import tkinter as tk
from pysimverse import Drone

MOVE_SPEED = 50
YAW_SPEED = 50
UPDATE_INTERVAL_MS = 100

class KeyboardDroneController:
    def __init__(self):
        self.drone = Drone()
        self.drone.connect()
        self.is_flying = False
        self.active_keys = set()
        self.root = tk.Tk()
        self.root.title("Drone Keyboard Control")
        self.root.geometry("520x260")
        self.root.resizable(False, False)
        instructions = (
            "Click this window first, then use the keyboard.\n\n"
            "T = Take off\n"
            "L = Land\n"
            "W/S = Forward/Backward\n"
            "A/D = Left/Right\n"
            "Up/Down = Up/Down\n"
            "Left/Right = Rotate left/right\n"
            "Q = Quit"
        )
        label = tk.Label(self.root, text=instructions, font=("Arial", 14), justify="left", padx=20, pady=20)
        label.pack(fill="both", expand=True)
        self.status_label = tk.Label(self.root, text="Status: Connected, on ground", font=("Arial", 12), anchor="w", padx=20)
        self.status_label.pack(fill="x")
        self.root.bind("<KeyPress>", self.on_key_press)
        self.root.bind("<KeyRelease>", self.on_key_release)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.focus_force()

    def on_key_press(self, event):
        key = event.keysym.lower()
        if key == "t":
            if not self.is_flying:
                self.drone.take_off()
                self.is_flying = True
                self.update_status("Flying")
            return
        if key == "l":
            if self.is_flying:
                self.stop_motion()
                self.drone.land()
                self.is_flying = False
                self.update_status("Landed")
            return
        if key == "q":
            self.on_close()
            return
        self.active_keys.add(key)

    def on_key_release(self, event):
        key = event.keysym.lower()
        self.active_keys.discard(key)

    def get_rc_values(self):
        left_right = forward_backward = up_down = yaw = 0
        if "w" in self.active_keys: forward_backward = MOVE_SPEED
        elif "s" in self.active_keys: forward_backward = -MOVE_SPEED
        if "a" in self.active_keys: left_right = -MOVE_SPEED
        elif "d" in self.active_keys: left_right = MOVE_SPEED
        if "up" in self.active_keys: up_down = MOVE_SPEED
        elif "down" in self.active_keys: up_down = -MOVE_SPEED
        if "left" in self.active_keys: yaw = -YAW_SPEED
        elif "right" in self.active_keys: yaw = YAW_SPEED
        return left_right, forward_backward, up_down, yaw

    def control_loop(self):
        if self.is_flying:
            self.drone.send_rc_control(*self.get_rc_values())
        self.root.after(UPDATE_INTERVAL_MS, self.control_loop)

    def stop_motion(self):
        self.drone.send_rc_control(0, 0, 0, 0)

    def update_status(self, text):
        self.status_label.config(text=f"Status: {text}")

    def on_close(self):
        try:
            if self.is_flying:
                self.stop_motion()
                self.drone.land()
                time.sleep(2)
        finally:
            self.root.destroy()

    def run(self):
        self.control_loop()
        self.root.mainloop()

if __name__ == "__main__":
    controller = KeyboardDroneController()
    controller.run()
