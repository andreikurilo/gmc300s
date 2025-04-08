# serial_device.py
import threading
import serial
from enum import Enum

# Defining an Enum class
class CommandResult(Enum):
    NotConnected = 1
    Sent = 2
    Error = 3

class CommandResponse:
    def __init__(self, status: CommandResult, data: bytes = None, err: str = None):
        self.status = status
        self.err = err
        self.data = data

class SerialDevice:
    def __init__(self, serial_port: str, baud_rate=57600):
        self.serial_port: str = serial_port
        self.baud_rate = baud_rate
        self.ser = None
        self.lock = threading.Lock()

    def make_sure_connected(self):
        """Connects to a serial device"""
        
        if self.is_connected():
            return
        
        try:
            print(f"Attempting to connect to {self.serial_port}...")
            self.ser = serial.Serial(self.serial_port, self.baud_rate, timeout=1)
            print(f"Connected to {self.serial_port} at {self.baud_rate} baud")
        except serial.SerialException as e:
            print(f"Error connecting to serial port: {e}")

    def disconnect(self):
        """Disconnect from the serial device."""
        if self.ser and self.ser.is_open:
            self.ser.close()
            print("Serial port closed.")

    def read(self, size: int):
        with self.lock:
            return self.ser.read(size=size)
    
    def is_connected(self):
        return self.ser and self.ser.is_open
    
    def send_command(self, command: str) -> CommandResponse:
        """Send a command to the serial device."""
        if self.ser and self.ser.is_open:
            try:
                response: bytes = None
                with self.lock:
                    self.ser.reset_input_buffer()
                    self.ser.write(command.encode())  # Send the command (make sure it's a string)
                    # Read the response from the device
                    response = self.ser.readline()
                print(f"Sent command: {command}. Response {response}")
                result = CommandResponse(status=CommandResult.Sent, data=response)
                return result
            except serial.SerialException as e:
                print(f"Failed to send command: {e}")
                return CommandResponse(status=CommandResult.Error, err=str(e))
                
        else:
            print("Not connected to the Geiger counter.")
            return CommandResponse(status=CommandResult.NotConnected)