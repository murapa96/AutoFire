#!/usr/bin/env python3
"""
RapidFire - Auto Key Presser

This script allows you to automatically press a key repeatedly until a stop
key combination is pressed.
"""

import time
import threading
import logging
import sys
from typing import Optional

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("RapidFire")

# Try different keyboard libraries in order of preference
try:
    import keyboard as kb
    USING_KEYBOARD_LIB = True
    logger.info("Using 'keyboard' library")
except ImportError:
    try:
        from pynput import keyboard
        from pynput.keyboard import Key, KeyCode, Controller
        USING_KEYBOARD_LIB = False
        logger.info("Using 'pynput' library")
    except ImportError:
        logger.critical("No keyboard library available. Please install 'keyboard' or 'pynput'")
        sys.exit(1)

class RapidFire:
    """
    A class to handle automatic key pressing functionality.
    
    Attributes:
        active_key: Currently active key being automatically pressed
        interval (float): Time interval between key presses in seconds
        running (bool): Flag to indicate if auto-pressing is active
    """
    
    def __init__(self, interval: float = 1.0):
        """
        Initialize the RapidFire instance.
        
        Args:
            interval (float): Time between key presses in seconds
        """
        self.interval: float = interval
        self.running: bool = False
        self.press_thread: Optional[threading.Thread] = None
        
        if USING_KEYBOARD_LIB:
            self.active_key = None
            # Define stop combination
            self.stop_combo = "ctrl+esc+w"
        else:
            self.keyboard = Controller()
            self.active_key: Optional[Key | KeyCode] = None
            # Keys that need to be pressed to stop
            self.stop_keys = {Key.ctrl_l, Key.esc, KeyCode.from_char('w')}
            self.current_keys = set()
        
        logger.info("RapidFire initialized. Stop combination: ctrl + esc + w")
    
    def _kb_press_callback(self, e):
        """Callback for keyboard library press events"""
        if kb.is_pressed(self.stop_combo):
            self.stop_autopress()
            return
        
        if not self.running and not any(kb.is_pressed(k) for k in self.stop_combo.split('+')):
            self.start(e.name)
    
    def on_press(self, key):
        """Handle key press events for pynput."""
        try:
            if key in self.stop_keys:
                self.current_keys.add(key)
                
                if all(k in self.current_keys for k in self.stop_keys):
                    self.stop_autopress()
                    return
            
            if not self.running and key not in self.stop_keys:
                self.start(key)
        except Exception as e:
            logger.error(f"Error handling key press: {str(e)}")
    
    def on_release(self, key):
        """Handle key release events for pynput."""
        try:
            if key in self.current_keys:
                self.current_keys.remove(key)
        except Exception as e:
            logger.error(f"Error handling key release: {str(e)}")
    
    def start(self, key):
        """
        Start auto-pressing the specified key.
        
        Args:
            key: The key to auto-press
        """
        if self.running:
            self.stop_autopress()
            
        self.active_key = key
        self.running = True
        logger.info(f"Starting auto-press for key: {key}")
        
        # Start key pressing in a separate thread
        self.press_thread = threading.Thread(target=self._press_key_loop)
        self.press_thread.daemon = True
        self.press_thread.start()
    
    def _press_key_loop(self):
        """Internal method to continuously press the active key."""
        try:
            while self.running:
                if self.active_key:
                    if USING_KEYBOARD_LIB:
                        kb.press_and_release(self.active_key)
                    else:
                        self.keyboard.press(self.active_key)
                        self.keyboard.release(self.active_key)
                    logger.debug(f"Pressed key: {self.active_key}")
                time.sleep(self.interval)
        except Exception as e:
            logger.error(f"Error in key press loop: {str(e)}")
            self.stop_autopress()
    
    def stop_autopress(self):
        """
        Stop the auto-pressing functionality.
        """
        if self.running:
            logger.info(f"Stopping auto-press for key: {self.active_key}")
            self.running = False
            self.active_key = None
    
    def run(self):
        """Run the main application loop."""
        logger.info("RapidFire started. Press any key to begin auto-pressing.")
        logger.info("Press ctrl + esc + w to stop.")
        
        try:
            if USING_KEYBOARD_LIB:
                kb.hook(self._kb_press_callback)
                
                while True:
                    time.sleep(0.1)
            else:
                # Monkey-patch Listener._handle to avoid AttributeError on Xorg systems
                from pynput import keyboard
                if not hasattr(keyboard.Listener, "_handle"):
                    logger.warning("Monkey-patching Listener._handle to avoid callback error")
                    keyboard.Listener._handle = lambda self, display_stop, event, injected: None
                # Create the listener directly without context manager
                listener = keyboard.Listener(
                    on_press=self.on_press,
                    on_release=self.on_release)
                
                listener.start()
                time.sleep(0.5)  # Wait briefly to check listener status
                
                if not listener.is_alive() or not hasattr(listener, "is_alive"):
                    logger.warning("Keyboard listener failed. Switching to command-line interface mode.")
                    self._run_cli_mode()
                else:
                    while listener.is_alive():
                        time.sleep(0.1)
        except KeyboardInterrupt:
            logger.info("RapidFire terminated by user.")
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
        finally:
            self.stop_autopress()
            if USING_KEYBOARD_LIB:
                kb.unhook_all()
    
    def _run_cli_mode(self):
        """Run in command-line interface mode as fallback."""
        print("\n===== RapidFire - Auto Key Presser (CLI Mode) =====")
        print("This fallback mode uses command-line interface.")
        print("To stop at any time, press Ctrl+C in this terminal.\n")
        
        try:
            while True:
                print("\nAvailable commands:")
                print("  start <key> - Start auto-pressing a key (e.g. 'start a' or 'start space')")
                print("  stop        - Stop current auto-pressing")
                print("  interval <seconds> - Change the press interval (e.g. 'interval 0.5')")
                print("  exit/quit   - Exit the program")
                
                cmd = input("\n> ").strip().lower()
                
                if cmd == "exit" or cmd == "quit":
                    break
                    
                elif cmd.startswith("start "):
                    key_str = cmd[6:].strip()
                    if not key_str:
                        print("Please specify a key to press")
                        continue
                        
                    # Convert string to Key object for special keys
                    if key_str == "space":
                        key = Key.space
                    elif key_str == "enter":
                        key = Key.enter
                    elif key_str == "tab":
                        key = Key.tab
                    elif key_str in ("esc", "escape"):
                        key = Key.esc
                    elif key_str == "ctrl":
                        key = Key.ctrl_l
                    elif key_str == "alt":
                        key = Key.alt_l
                    elif key_str == "shift":
                        key = Key.shift_l
                    else:
                        # For single character keys
                        key = KeyCode.from_char(key_str[0])
                        
                    self.start(key)
                    
                elif cmd == "stop":
                    self.stop_autopress()
                    
                elif cmd.startswith("interval "):
                    try:
                        new_interval = float(cmd[9:].strip())
                        if new_interval > 0:
                            self.interval = new_interval
                            print(f"Interval changed to {new_interval} seconds")
                        else:
                            print("Interval must be greater than 0")
                    except ValueError:
                        print("Invalid interval value")
                        
                else:
                    print("Unknown command")
                    
        except KeyboardInterrupt:
            print("\nStopping RapidFire...")
        finally:
            self.stop_autopress()

if __name__ == "__main__":
    try:
        rapid_fire = RapidFire()
        rapid_fire.run()
    except Exception as e:
        logger.critical(f"Fatal error: {str(e)}")
        exit(1)