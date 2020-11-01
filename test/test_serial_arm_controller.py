import pytest
from Mock import MockSerial, MockNotificationsFrame, MockStatusBar
from gui.SerialArmController import SerialArmController, Command, Position

class TestSerialArmControllerPositive:

    mock_serial = None
    mock_notif_frame = None
    mock_status_bar = None
    my_sar = None   #SerialArmController object for testing

    def reset_mocked_sar(self):

        self.mock_serial = MockSerial()
        self.mock_notif_frame = MockNotificationsFrame()
        self.mock_status_bar = MockStatusBar()
        self.my_sar = SerialArmController(self.mock_status_bar, self.mock_notif_frame)
        self.my_sar._device = self.mock_serial

    def test_close_connected(self):
        """
        Tests close() method of SerialArmController when it is connected
        """

        #setup
        self.reset_mocked_sar()
        self.my_sar.is_connected = True  #sets sar to connected state

        #run test
        self.my_sar.close()

        #check
        assert self.mock_status_bar.get_status() == "DISCONNECTED"
        assert self.mock_serial.open_bool == False
        assert self.my_sar.is_connected == False

    def test_close_not_connected(self):
        """
        Tests close() method of SerialArmController when it not connected
        """

        #setup
        self.reset_mocked_sar()
        self.my_sar.is_connected = False

        #run test
        self.my_sar.close()

        #check
        assert self.mock_status_bar.get_status() == None

    def test_send_good_bytes_connected(self):
        """
        Tests send() method of SerialArmController with preset byte data as input
        while it is connected
        """

        #setup
        self.reset_mocked_sar()
        self.my_sar.is_connected = True

        #test
        in_bytes = bytes((0,1,2,3))
        self.my_sar.send(in_bytes)
        out_bytes = self.mock_serial.read(in_bytes.__len__())

        #check
        assert out_bytes == in_bytes


    def test_send_good_bytes_not_connected(self):
        """
        Tests send() method of SerialArmController with preset byte data as input
        while it is not connected
        """

        #setup
        self.reset_mocked_sar()
        self.my_sar.is_connected = False

        #test
        in_bytes = bytes((0, 1, 2, 3))
        self.my_sar.send(in_bytes)
        out_bytes = self.mock_serial.read(in_bytes.__len__())

        #check
        assert out_bytes == b''


    def test_recv_good_bytes_connected(self):
        """
        Tests recv() method of SerialArmController with preset byte data as input
        while it is connected
        """

        #setup
        self.reset_mocked_sar()
        self.my_sar.is_connected = True

        #test

        in_bytes = bytes((3,2,1))
        self.mock_serial.write(in_bytes)
        out_bytes = self.my_sar.recv()

        #check
        assert out_bytes == in_bytes

    def test_update_position_not_connected(self):
        """
        Tests update_position() method of SerialArmController with preset byte data as input
        while it is NOT connected
        """

        #setup
        self.reset_mocked_sar()
        self.my_sar.is_connected = False

        #test
        in_bytes = bytes((3, 100, 1))
        self.mock_serial.write(in_bytes)
        self.my_sar.update_position()


        #check
        assert self.my_sar.position.pitch == 0
        assert self.my_sar.position.yaw == 0
        assert self.my_sar.position.roll == 0


    @pytest.mark.parametrize("input_val", [90,63,172])
    def test_set_pitch_connected(self, input_val):
        """
        Tests set_pitch() method of SerialArmController with preset byte data as input
        while it is connected
        """
        
        #setup
        self.reset_mocked_sar()
        self.my_sar.is_connected = True

        #test
        self.my_sar.set_pitch(input_val)
        out_bytes = self.mock_serial.read(2)

        #check
        assert int(out_bytes[0]) == Command.PITCH
        assert int(out_bytes[1]) == input_val

