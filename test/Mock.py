
import io
import threading
import socket
from gui.SerialArmController import Position

class MockSerial:
    def __init__(self):
        self.byte_buffer = io.BytesIO()
        self.offset = 0
        self.open_bool = True

    def read(self, size):
        if(self.open_bool):
            data = self.byte_buffer.read(size)
            self.offset += size
            return data
        return None

    def write(self, data):
        if(self.open_bool):
            num_written = self.byte_buffer.write(data)
            self.byte_buffer.seek(self.offset)
            return num_written
        return None

    def close(self):
        self.byte_buffer.flush()
        self.offset = 0
        self.open_bool = False

        
class MockNotificationsFrame:
    def __init__(self):
        self.lines = []

    def append_line(self, line):
        self.lines.append(line)

    def get_lines(self):
        return self.lines

class MockStatusBar:
    def __init__(self):
        self.status = None

    def set_status(self, status):
        self.status = status

    def get_status(self):
        return self.status

class MockSerialArmController:
    def __init__(self):
        self.is_connected = False
        self.open_arm_bool = False
        self.close_arm_bool = False
        self.portrait_bool = False
        self.landscape_bool = False
        self.tilt_bool = False
        self.nod_bool = False
        self.shake_bool = False
        self.shutdown_bool = False
        self.pitch = 0
        self.yaw = 0
        self.roll = 0

    def open_arm(self):
        self.open_arm_bool = True

    def close_arm(self):
        self.close_arm_bool = True

    def portrait(self):
        self.portrait_bool = True

    def landscape(self):
        self.landscape_bool = True

    def tilt(self):
        self.tilt_bool = True

    def nod(self):
        self.nod_bool = True

    def shake(self):
        self.shake_bool = True

    def _shutdown(self):
        self.shutdown_bool = True

    def set_pitch(self, val):
        self.pitch = val

    def set_yaw(self, val):
        self.yaw = val

    def set_roll(self, val):
        self.roll = val



class MockLogFile():
    def __init__(self):
        self.arr = []

    def write(self, text):
        self.arr.append(text)

class MockSpinBox():
    def __init__(self, val=0):
        self.val = val

    def get(self):
        return self.val

    def set(self, val):
        self.val = val


class MockSlider():
    def __init__(self, val=0):
        self.val = val

    def get(self):
        return self.val

    def set(self, val):
        self.val = val

class MockAudioServer:
    def __init__(self):
        pass

class MockMessageServer:

    def __init__(self, ip, port, str_format):
        
        self.recent_msg = None
        self.server = None
        self.ip = ip
        self.port = port
        self.addr = (self.ip, self.port)
        self.str_format = str_format
        self.client_conn = None
        self.restart_bool = False

        self.str_lock = threading.Lock()
        self.start_lock = threading.Lock()

        self.run_thread = None


    def start_server(self):
        self.restart_bool = True
        self.start_lock.acquire()
        self.run_thread = threading.Thread(target=self.handle_start_server)
        self.run_thread.start()

    def handle_start_server(self):
        
        while(self.restart_bool):

            try:
                self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.server.bind(self.addr)
                self.start_lock.release()

                self.server.listen()
                self.client_conn, addr = self.server.accept()

                msg = self.client_conn.recv(2048).decode(self.str_format).strip()
                self.str_lock.acquire()
                self.recent_msg = msg
                self.str_lock.release()
            
            except KeyboardInterrupt:
                break
            except ConnectionAbortedError:
                break
            except OSError:
                break

    def stop_server(self):
        self.restart_bool = False
        self.start_lock.acquire()
        if(self.client_conn is not None):
            self.client_conn.close()
        if(self.server is not None):
            self.server.close()
        self.start_lock.release()

        if(self.run_thread is not None):
            self.run_thread.join()
            self.run_thread = None
        

    def get_recent_msg(self):
        self.str_lock.acquire()
        r = self.recent_msg
        self.str_lock.release()
        return r