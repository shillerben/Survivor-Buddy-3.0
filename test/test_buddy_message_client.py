import pytest
import time
import contextlib

from gui.BuddyMessageClient import BuddyMessageClient
from Mock import MockMessageServer

class DefaultValues:
    port = 5050
    ip = 'localhost'
    format = 'utf-8'

class BaseBuddyMessageTestClass:
    bmc = None  # bmc=buddy message client
    mock_bms = None  # bms=buddy message server

    def reset_client(
        self,
        ip=DefaultValues.ip,
        port=DefaultValues.port,
        str_format=DefaultValues.format
    ):
        self.bmc = BuddyMessageClient(ip, port, None, str_format=str_format)

    @contextlib.contextmanager
    def run_mock_server(
        self,
        ip=DefaultValues.ip,
        port=DefaultValues.port,
        _format=DefaultValues.format
    ):
        self.mock_bms = MockMessageServer(ip, port, _format)
        self.mock_bms.start_server()
        yield
        self.mock_bms.stop_server()
        self.mock_bms = None

class TestBuddyMessageClientHappy(BaseBuddyMessageTestClass):

    def test_connect_server_running(self):
        '''
        Tests that connect returns true when the server is running
        '''

        #setup
        self.reset_client()
        #run
        with self.run_mock_server():
            assert self.bmc.connect() == True

    def test_connect_server_not_running(self):
        '''
        Tests that connect returns False when the server is not running
        '''

        #setup
        self.reset_client()
        #run
        assert self.bmc.connect() == False

    @pytest.mark.parametrize("input_val", ['hello', 'goodbye', '12345'])
    def test_handle_send_server_running(self, input_val):
        '''
        Tests handleSend() method with some preset data and checks that
        it matches when read on the server
        '''

        self.reset_client()

        with self.run_mock_server():
            self.bmc.handleSend(input_val)
            time.sleep(0.1) #allows time for the socket IO to happen
            assert self.mock_bms.get_recent_msg() == input_val

    def test_handle_send_server_not_running(self):
        '''
        Tests handleSend() method with some preset data. This should
        not send anything to the server as it is not running.
        '''

        self.reset_client()
        mock_server = MockMessageServer(
            DefaultValues.ip,
            DefaultValues.port,
            DefaultValues.format
        )

        self.bmc.handleSend("hello")
        assert mock_server.get_recent_msg() is None


class TestBuddyMessageClientNegative(BaseBuddyMessageTestClass):

    def test_wrong_ip_address(self):
        '''
        Tests the error handling of the connect() method for when a bad ip 
        is provided to the client
        '''

        self.reset_client(ip='192.168.0.1')
        with self.run_mock_server():
            assert self.bmc.connect() == False

    def test_wrong_port(self):
        '''
        Tests the error handling of the connect() method for when a bad port 
        is provided to the client
        '''

        self.reset_client(port=9999)
        with self.run_mock_server():
            assert self.bmc.connect() == False

    def test_wrong_ip_address_and_port(self):
        '''
        Tests the error handling of the connect() method for when a bad ip 
        and port is provided to the client
        '''

        self.reset_client(ip='192.168.0.1', port=9999)
        with self.run_mock_server():
            assert self.bmc.connect() == False


