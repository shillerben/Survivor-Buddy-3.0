
import io


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


