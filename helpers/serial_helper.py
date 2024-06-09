import serial

class SerialHelper:
    def __init__(self, port=None, baudrate=9600, timeout=1):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial_connection = None

    def set_port(self, port):
        self.port = port
        print(f"Port set to {self.port}")

    def set_baudrate(self, baudrate):
        self.baudrate = baudrate
        print(f"Baudrate set to {self.baudrate}")

    def open_connection(self):
        if self.port is None:
            raise ValueError("Port not set. Please set the port before opening the connection.")
        self.serial_connection = serial.Serial(
            port=self.port,
            baudrate=self.baudrate,
            timeout=self.timeout
        )
        print(f"Connection opened on {self.port} with baudrate {self.baudrate}")

    def close_connection(self):
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.close()
            print("Connection closed")

    def flush_serial(self):
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.flush()
            print("Serial port flushed")

    def write_data(self, data):
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.write(data.encode())
            print(f"Data written to serial port: {data}")

    def read_data(self):
        if self.serial_connection and self.serial_connection.is_open and self.serial_connection.in_waiting > 0:
            data = self.serial_connection.read(self.serial_connection.in_waiting)
            return data.decode()
        return None