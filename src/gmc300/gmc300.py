from datetime import datetime
import threading
import time

import serial

from serial_device import CommandResult
from serial_device import SerialDevice
from geiger_counter import GeigerCounter

class Commands:
    ENABLE_HEARTBEAT = "<HEARTBEAT1>>"
    DISABLE_HEARTBEAT = "<HEARTBEAT0>>"
    GET_CPM = '<GETCPM>>'

class Gmc300:
    def __init__(self, serial: SerialDevice):
        """Inits a meter with a given serial and new counter"""
        self._serial: SerialDevice = serial
        self._counter = GeigerCounter()
        self.last_read = None
        self.stop_event = threading.Event()
        self.thread: threading.Thread = None
        self.is_heartbeat_enabled = False
    
    def send_command(self, command: str):
        result = self._serial.send_command(command=command)
        return {
            'result': self._parse_response(command=command, raw=result.data),
            'status': result.status.name,
            'err': result.err,
        }
        
    def subscribe(self):
        """Start a thread to read data from the Geiger counter."""
        self.stop_event.clear()
        self.thread = threading.Thread(target=self._subscribe, daemon=True)
        self.thread.start()

    def unsubscribe(self):
        """Disconnects from serial and stops the thread"""
        if self.thread is not None and self.thread.is_alive():
            self.stop_event.set()
        self._serial.disconnect()
    
    def set_counter(self, counter: GeigerCounter):
        """Sets a new counter"""
        self._counter = counter
    
    def get_counter(self):
        """Gets counter"""
        return self._counter
    
    def enable_heartbeat(self):
        result = self._send_command(Commands.ENABLE_HEARTBEAT)
        self.is_heartbeat_enabled = result.status.value == CommandResult.Sent.value
    
    def _send_command(self, command: str):
        return self._serial.send_command(command=command)
    
    def _parse_response(self, command: str, raw: bytes):
        if raw is None or len(raw) == 0:
            return "Empty"
        
        match command:
            case Commands.GET_CPM:
                return self._get_counts_data(raw)
            case Commands.ENABLE_HEARTBEAT:
                return "Enabled"
            case Commands.DISABLE_HEARTBEAT:
                return "Disabled"
            case _:
                return "Unknown Command"
    
    def _read_data(self):
        raw_data = self._serial.read(2)
        self.last_read = datetime.now()
        cps = self._get_counts_data(raw_data)
        self._counter.add_cps(cps)
    
    def _get_counts_data(self, raw_data: bytes) -> int:
        if len(raw_data) == 2:
            raw_cps = (raw_data[0] << 8) | raw_data[1]  # Convert to int
            return raw_cps & 0x3FFF
        else:
            self.enable_heartbeat()
        return 0
    
    def _subscribe(self):
        while not self.stop_event.is_set():
            connected = self._make_sure_connected()
            if not self.is_heartbeat_enabled:
                self.enable_heartbeat()
            
            if connected:
                try:
                    self._read_data()
                    time.sleep(1)
                except serial.SerialException as e:
                    print(f"Serial error: {e}. Retrying in 5 seconds...")
                    self._serial.disconnect()
                    time.sleep(5)
                except Exception as e:
                    print(f"Unexpected error: {e}. Retrying in 5 seconds...")
                    self._serial.disconnect()
                    time.sleep(5)
            else:
                time.sleep(5)
        print("Thread has finished")
    
    def _make_sure_connected(self):
        i = 0
        while i < 5 and not self.stop_event.is_set():
            i += 1
            self._serial.make_sure_connected()
            if not self._serial.is_connected():
                time.sleep(i)
            else:
                return True
        
        print("Unable to connect")
        return False
    
    
   