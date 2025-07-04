from pynput.mouse import Button, Controller
from pynput.keyboard import Listener, KeyCode
import time

# Create an instance of the mouse controller
mouse = Controller()

# Define the key bind to start the click loop
start_key = KeyCode(char='e')

# Define the key bind to stop the script
stop_key = KeyCode(char='q')

# Flag to indicate if the click loop should start
should_start = False

# Click loop function
def click_loop():
    # Wait for a few seconds to give you time to position the mouse

    # Simulate 100 left mouse button clicks with 1ms delay between each click
    for _ in range(100000000):
        mouse.click(Button.left)

        # Check if the stop key is pressed, and if so, break the loop
        if keyboard_listener.stop_key_pressed:
            break

# Keyboard listener class
class KeyboardListener:
    def __init__(self):
        self.stop_key_pressed = False

    def on_press(self, key):
        if key == start_key:
            self.stop_key_pressed = False
            click_loop()

        elif key == stop_key:
            self.stop_key_pressed = True
            return False  # Stop the listener

# Create an instance of the keyboard listener
keyboard_listener = KeyboardListener()

# Start the keyboard listener
with Listener(on_press=keyboard_listener.on_press) as listener:
    listener.join()
