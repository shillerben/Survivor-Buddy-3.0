import pytest
from pytest_mock import mocker

from gui.BuddyMessageClient import BuddyMessageClient

class DefaultValues:
    port = 5050
    ip = 'localhost'
    master = None
    format = 'utf-8'

class TestBuddyMessageClientHappy():

    def test_connect_server_running(self, mocker):
        '''
        Tests that connect returns true when the server is running
        '''

        #setup
        bmc = BuddyMessageClient(DefaultValues.ip, DefaultValues.port, DefaultValues.master)
        mock_socket = mocker.patch('socket.socket', autospec=True)

        #run
        bmc.connect()

        #check
        mock_socket.return_value.connect.assert_called_with(bmc.full_addr)

    def test_connect_server_not_running(self, mocker):
        '''
        Tests that connect returns False when the server is not running
        '''

        #setup
        bmc = BuddyMessageClient(DefaultValues.ip, DefaultValues.port, DefaultValues.master)
        mock_socket = mocker.patch('socket.socket', autospec=True)
        mock_socket.return_value.connect.side_effect = TimeoutError

        #run
        connect_return = bmc.connect()

        #check
        mock_socket.return_value.connect.assert_called_with(bmc.full_addr)
        assert connect_return == False

    def test_disconnect_connected(self, mocker):
        '''
        Tests that diconnect calls socket.close when it is connected\
        '''

        #setup
        bmc = BuddyMessageClient(DefaultValues.ip, DefaultValues.port, DefaultValues.master)
        mock_socket = mocker.patch('socket.socket', autospec=True)

        bmc.client_socket = mock_socket.return_value
        #run
        bmc.disconnect()

        #check
        mock_socket.return_value.close.assert_called()
        assert bmc.client_socket is None


    @pytest.mark.parametrize("input_val", ['hello', 'goodbye', '12345'])
    def test_handle_send_server_running(self, mocker, input_val):
        '''
        Tests handleSend() method with some preset data and checks that
        it matches when read on the server
        '''

        #setup
        bmc = BuddyMessageClient(DefaultValues.ip, DefaultValues.port, DefaultValues.master)
        mock_socket = mocker.patch('socket.socket', autospec=True)

        #run
        bmc.handleSend(input_val)

        #check
        encode_input = input_val.encode(bmc.str_format)
        mock_socket.return_value.sendall.assert_called_with(encode_input)

    def test_handle_send_server_not_running(self, mocker):
        '''
        Tests handleSend() method with some preset data. This should
        not send anything to the server as it is not running.
        '''

        #setup
        bmc = BuddyMessageClient(DefaultValues.ip, DefaultValues.port, DefaultValues.master)
        mock_socket = mocker.patch('socket.socket', autospec=True)
        mock_socket.return_value.connect.side_effect = TimeoutError

        #run
        bmc.handleSend("hello")

        #check
        mock_socket.return_value.sendall.assert_not_called()


class TestBuddyMessageClientNegative():

    def test_wrong_ip_address_only(self, mocker):
        '''
        Tests the error handling of the connect() method for when a bad ip 
        is provided to the client
        '''

        ip_addr = '192.168.0.1'
        #setup
        bmc = BuddyMessageClient(ip_addr, DefaultValues.port, DefaultValues.master)
        mock_socket = mocker.patch('socket.socket', autospec=True)
        mock_socket.return_value.connect.side_effect = TimeoutError

        #run
        connect_return = bmc.connect()

        #check
        assert connect_return == False
        mock_socket.return_value.connect.assert_called_with((ip_addr, DefaultValues.port))
        


    def test_wrong_port_only(self, mocker):
        '''
        Tests the error handling of the connect() method for when a bad port 
        is provided to the client
        '''

        port_num = 9999
        #setup
        bmc = BuddyMessageClient(DefaultValues.ip, port_num, DefaultValues.master)
        mock_socket = mocker.patch('socket.socket', autospec=True)
        mock_socket.return_value.connect.side_effect = TimeoutError

        #run
        connect_return = bmc.connect()

        #check
        assert connect_return == False
        mock_socket.return_value.connect.assert_called_with((DefaultValues.ip, port_num))

    def test_wrong_ip_address_and_port(self, mocker):
        '''
        Tests the error handling of the connect() method for when a bad ip 
        and port is provided to the client
        '''
        ip_addr = '192.168.0.1'
        port_num = 9999
        #setup
        bmc = BuddyMessageClient(ip_addr, port_num, DefaultValues.master)
        mock_socket = mocker.patch('socket.socket', autospec=True)
        mock_socket.return_value.connect.side_effect = TimeoutError

        #run
        connect_return = bmc.connect()

        #check
        assert connect_return == False
        mock_socket.return_value.connect.assert_called_with((ip_addr, port_num))

    def test_disconnect_not_connected(self, mocker):
        '''
        Tests that disconnect() method does not do anything if the socket is not connected
        '''

        #setup
        bmc = BuddyMessageClient(DefaultValues.ip, DefaultValues.port, DefaultValues.master)
        mock_socket = mocker.patch('socket.socket', autospec=True)

        #run
        bmc.disconnect()

        #check
        mock_socket.return_value.close.assert_not_called()

