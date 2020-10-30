import pyaudio
import socket

class BuddyAudioClient:

    default_sampling_rate = 44100
    default_width = 2
    default_num_input_channels = 1
    default_chunk_size = 1024

    def __init__(self, ip_addr, port):

        self.server_ip = ip_addr
        self.port_num = port
        self.server_addr = (self.server_ip, self.port_num)
        self.client_socket = None
        self.conntinue_stream = None

        self.audio_handler = pyaudio.PyAudio()
        self.device_api_info = self.audio_handler.get_default_host_api_info()
        self.input_device_info = self.audio_handler.get_default_input_device_info()
        self.input_device_index = self.input_device_info['index']

        self.sampling_rate = self.default_sampling_rate
        self.width = self.default_width
        self.num_input_channels = self.default_num_input_channels
        self.chunk_size = self.default_chunk_size

        self.audio_stream = None

    def _connect(self):
        if(self.client_socket == None):
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect(self.server_addr)
        #except ConnectionRefusedError:
        #    print("Error: ConnRefused")
        #    return False
        except TimeoutError:
            print("Error: Timeout")
            return False

        self.client_socket.sendall(str(self.chunk_size).encode('utf-8'))
        
        return True

    def disconnect(self):
        self.client_socket.close()

    def _startStream(self):
        
        self.audio_stream = self.audio_handler.open(
            format=self.audio_handler.get_format_from_width(self.width),
            channels=self.num_input_channels,
            rate=self.sampling_rate,
            input=True,
            frames_per_buffer=self.chunk_size
        )

        while True:
            audio_data = self.audio_stream.read(self.chunk_size)
            self.client_socket.sendall(audio_data)

    def stopStream(self):
        pass

    def disconnect(self):
        self.client_socket.close()

    def setInputDevice(self):
        pass

