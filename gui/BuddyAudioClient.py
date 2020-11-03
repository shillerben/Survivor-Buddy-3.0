import pyaudio
import socket
import threading
import copy
import time

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
        self.continue_stream = None
        self.connectedBool = False

        self.audio_handler = pyaudio.PyAudio()
        self.device_api_info = self.audio_handler.get_default_host_api_info()
        self.input_device_info = self.audio_handler.get_default_input_device_info()
        self.input_device_index = self.input_device_info['index']

        self.sampling_rate = self.default_sampling_rate
        self.width = self.default_width
        self.num_input_channels = self.default_num_input_channels
        self.chunk_size = self.default_chunk_size

        self.audio_stream = None


        self.input_device_list = None


    def connect(self):
        if(self.client_socket == None):
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect(self.server_addr)
        except ConnectionRefusedError:
            print("Error: ConnRefused")
            return False
        except TimeoutError:
            print("Error: Timeout")
            return False

        self.client_socket.sendall(str(self.chunk_size).encode('utf-8'))
        
        return True

    def connectAndStart(self):
        if(not self.connectedBool):
            threading.Thread(target=self.handleConnectAndStart).start()

    def handleConnectAndStart(self):
        time.sleep(1)
        if(self.connect()):
            self.connectedBool = True
            self.start_stream()

    def disconnectAndStop(self):
        self.continue_stream = False
        print(self.client_socket)
        if(self.client_socket is not None):
            self.client_socket.close()
        self.client_socket = None
        self.connectedBool = False

    def start_stream(self):

        print(f'DEVIN: {self.input_device_index}')
        
        self.audio_stream = self.audio_handler.open(
            format=self.audio_handler.get_format_from_width(self.width),
            channels=self.num_input_channels,
            rate=self.sampling_rate,
            input=True,
            frames_per_buffer=self.chunk_size,
            input_device_index=self.input_device_index
        )

        self.continue_stream = True
        while self.continue_stream:
            self.stream_loop()


    def stream_loop(self):
        audio_data = self.audio_stream.read(self.chunk_size)
        print(audio_data)
        if(self.client_socket is None):
            self.continue_stream = False
        elif(self.client_socket._closed):
            self.continue_stream = False
        else:
            self.client_socket.sendall(audio_data)
    

    def getInputDeviceNames(self):
        #returns a list[str] of input device names
        device_name_list = []
        for mdict in self.getInputDeviceDicts():
            device_name_list.append(mdict['name'])

        return device_name_list

    def getInputDeviceDicts(self):
        dict_list = []
        #TODO: May need to set device count dynamically here
        device_count = self.device_api_info['deviceCount']
        host_api_index = self.device_api_info['index']

        for device_index in range(0, device_count):
            device_dict = self.audio_handler.get_device_info_by_host_api_device_index(
                host_api_index,
                device_index
            )
            if(device_dict['maxInputChannels'] >= 1):
                dict_list.append(copy.deepcopy(device_dict))

        return dict_list

    def setInputDevice(self, device_name):

        print(f'NAME: {device_name}')
        device_dicts = self.getInputDeviceDicts()
        chosen_dict = None

        for d in device_dicts:
            if(d['name'] == device_name):
                chosen_dict = d
                break

        if(chosen_dict == None):
            print("ERROR: Device not found")
        else:
            self.input_device_index = chosen_dict['index']
