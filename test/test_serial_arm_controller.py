import pytest
from .Mock import MockSerial, MockNotificationsFrame, MockStatusBar
from gui.SerialArmController import SerialArmController, Command, Position

class TestSerialArmControllerHappy:

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

    def test_recv_good_bytes_not_connected(self):
        """
        Tests recv() method of SerialArmController with preset byte data as input
        while it is connected
        """

        #setup
        self.reset_mocked_sar()
        self.my_sar.is_connected = False

        #test

        in_bytes = bytes((3,2,1))
        self.mock_serial.write(in_bytes)
        out_bytes = self.my_sar.recv()

        #check
        assert out_bytes is None

    def test_update_position_connected(self):
        """
        Tests update_position() method of SerialArmController with preset byte data as input
        while it is connected
        """

        #setup
        self.reset_mocked_sar()
        self.my_sar.is_connected = True

        #test
        in_bytes = bytes((3, 100, 1))
        self.mock_serial.write(in_bytes)
        self.my_sar.update_position()


        #check
        assert self.my_sar.position.pitch == 3
        assert self.my_sar.position.yaw == 100-90
        assert self.my_sar.position.roll == 1

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


    @pytest.mark.parametrize("input_val", [0, 45, 90])
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

    @pytest.mark.parametrize("input_val", [0, 45, 90])
    def test_set_pitch_not_connected(self, input_val):
        """
        Tests set_pitch() method of SerialArmController with preset byte data as input
        while it is not connected
        """

        # setup
        self.reset_mocked_sar()
        self.my_sar.is_connected = False

        # test
        self.my_sar.set_pitch(input_val)
        out_bytes = self.mock_serial.read(2)

        # check
        assert self.my_sar.position.pitch == 0

    @pytest.mark.parametrize("input_val", [-90, 0, 90])
    def test_set_yaw_connected(self, input_val):
        """
        Tests set_yaw() method of SerialArmController with preset byte data as input
        while it is connected
        """

        # setup
        self.reset_mocked_sar()
        self.my_sar.is_connected = True

        # test
        self.my_sar.set_yaw(input_val)
        out_bytes = self.mock_serial.read(2)
        # check
        assert int(out_bytes[0]) == Command.YAW
        assert int(out_bytes[1]) == input_val+90

    @pytest.mark.parametrize("input_val", [-90, 0, 90])
    def test_set_yaw_not_connected(self, input_val):
        """
        Tests set_yaw() method of SerialArmController with preset byte data as input
        while it is not connected
        """

        # setup
        self.reset_mocked_sar()
        self.my_sar.is_connected = False

        # test
        self.my_sar.set_yaw(input_val)
        out_bytes = self.mock_serial.read(2)
        # check
        assert self.my_sar.position.yaw == 0

    @pytest.mark.parametrize("input_val", [0, 45, 90])
    def test_set_roll_connected(self, input_val):
        """
        Tests set_roll() method of SerialArmController with preset byte data as input
        while it is connected
        """

        # setup
        self.reset_mocked_sar()
        self.my_sar.is_connected = True

        # test
        self.my_sar.set_roll(input_val)
        out_bytes = self.mock_serial.read(2)
        # check
        assert int(out_bytes[0]) == Command.ROLL
        assert int(out_bytes[1]) == input_val

    @pytest.mark.parametrize("input_val", [0, 45, 90])
    def test_set_roll_not_connected(self, input_val):
        """
        Tests set_roll() method of SerialArmController with preset byte data as input
        while it is not connected
        """

        # setup
        self.reset_mocked_sar()
        self.my_sar.is_connected = False

        # test
        self.my_sar.set_roll(input_val)
        out_bytes = self.mock_serial.read(2)
        # check
        assert self.my_sar.position.roll == 0

    def test_close_arm_pitch_0(self):
        """
        Tests close_arm() method of SerialArmController with preset byte data as input
        when the pitch is already 0
        """

        # setup
        self.reset_mocked_sar()

        # test
        self.my_sar.close_arm()
        out_bytes = self.mock_serial.read(2)

        # check
        assert self.mock_notif_frame.lines[0] == "WARNING: ARM ALREADY CLOSED"

    def test_close_arm_pitch_not_0(self):
        """
        Tests close_arm() method of SerialArmController with preset byte data as input
        when the pitch is not 0
        """

        # setup
        self.reset_mocked_sar()
        self.my_sar.is_connected = True

        # test
        self.my_sar.position.pitch = int(10)
        self.my_sar.close_arm()
        out_bytes = self.mock_serial.read(2)

        # check
        assert int(out_bytes[0]) == Command.CLOSE
        assert int(out_bytes[1]) == 0

    def test_open_arm_pitch_90(self):
        """
        Tests open_arm() method of SerialArmController with preset byte data as input
        when the pitch is already 90
        """

        # setup
        self.reset_mocked_sar()
        self.my_sar.is_connected = True

        # test
        self.my_sar.position.pitch = 90
        self.my_sar.open_arm()

        # check
        assert self.mock_notif_frame.lines[0] == "WARNING: ARM ALREADY OPEN"

    def test_open_arm_pitch_not_90(self):
        """
        Tests open_arm() method of SerialArmController with preset byte data as input
        when the pitch is not 90
        """

        # setup
        self.reset_mocked_sar()
        self.my_sar.is_connected = True

        # test
        self.my_sar.open_arm()
        out_bytes = self.mock_serial.read(2)

        # check
        assert int(out_bytes[0]) == Command.OPEN
        assert int(out_bytes[1]) == 0

    def test_portrait_is_connected_roll_0(self):
        """
        Tests portrait() method of SerialArmController with preset byte data as input
        when the roll is 0 and is connected
        """

        # setup
        self.reset_mocked_sar()
        self.my_sar.is_connected = True

        # test
        self.my_sar.portrait()


        # check
        assert self.mock_notif_frame.lines[0] == "WARNING: ALREADY IN PORTRAIT"

    def test_portrait_not_connected_roll_0(self):
        """
        Tests portrait() method of SerialArmController with preset byte data as input
        when the roll is 0 and is not connected
        """

        # setup
        self.reset_mocked_sar()
        self.my_sar.is_connected = False

        # test
        self.my_sar.portrait()


        # check
        assert self.my_sar.position.roll == 0

    def test_portrait_is_connected_roll_not_0(self):
        """
        Tests portrait() method of SerialArmController with preset byte data as input
        when the roll is not 0 and is connected
        """

        # setup
        self.reset_mocked_sar()
        self.my_sar.is_connected = True

        # test
        self.my_sar.position.roll = 10
        self.my_sar.portrait()
        out_bytes = self.mock_serial.read(2)

        # check
        assert int(out_bytes[0]) == Command.PORTRAIT
        assert int(out_bytes[1]) == 0

    def test_portrait_is_not_connected_roll_not_0(self):
        """
        Tests portrait() method of SerialArmController with preset byte data as input
        when the roll is not 0 and is not connected
        """

        # setup
        self.reset_mocked_sar()
        self.my_sar.is_connected = True

        # test
        self.my_sar.position.roll = 10
        self.my_sar.landscape()

        # check
        assert self.my_sar.position.roll == 10

    def test_landscape_is_connected_roll_90(self):
        """
        Tests landscape() method of SerialArmController with preset byte data as input
        when the roll is 90 and is connected
        """

        # setup
        self.reset_mocked_sar()
        self.my_sar.is_connected = True

        # test
        self.my_sar.position.roll = 90
        self.my_sar.landscape()


        # check
        assert self.mock_notif_frame.lines[0] == "WARNING: ALREADY IN LANDSCAPE"

    def test_landscape_not_connected_roll_90(self):
        """
        Tests landscape() method of SerialArmController with preset byte data as input
        when the roll is 90 and is not connected
        """

        # setup
        self.reset_mocked_sar()
        self.my_sar.is_connected = False

        # test
        self.my_sar.landscape()

        # check
        assert self.my_sar.position.roll == 0

    def test_landscape_is_connected_roll_not_90(self):
        """
        Tests landscape() method of SerialArmController with preset byte data as input
        when the roll is not 90 and is connected
        """

        # setup
        self.reset_mocked_sar()
        self.my_sar.is_connected = True

        # test
        self.my_sar.position.roll = 10
        self.my_sar.landscape()
        out_bytes = self.mock_serial.read(2)

        # check
        assert int(out_bytes[0]) == Command.LANDSCAPE
        assert int(out_bytes[1]) == 0

    def test_landscape_is_not_connected_roll_not_90(self):
        """
        Tests landscape() method of SerialArmController with preset byte data as input
        when the roll is not 90 and is not connected
        """

        # setup
        self.reset_mocked_sar()
        self.my_sar.is_connected = True

        # test
        self.my_sar.position.roll = 10
        self.my_sar.landscape()

        # check
        assert self.my_sar.position.roll == 10

    def test_tilt_is_connected(self):
        """
        Tests tilt() method of SerialArmController with preset byte data as input
        while it is connected
        """

        # setup
        self.reset_mocked_sar()
        self.my_sar.is_connected = True

        # test
        self.my_sar.tilt()
        out_bytes = self.mock_serial.read(2)
        # check
        assert int(out_bytes[0]) == Command.TILT
        assert int(out_bytes[1]) == 0

    def test_tilt_is_not_connected(self):
        """
        Tests tilt() method of SerialArmController with preset byte data as input
        while it is not connected
        """

        # setup
        self.reset_mocked_sar()
        self.my_sar.is_connected = False

        # test
        self.my_sar.tilt()

        # check
        assert self.my_sar.position.roll == 0
        assert self.my_sar.position.yaw == 0
        assert self.my_sar.position.pitch == 0

    def test_nod_is_connected(self):
        """
        Tests nod() method of SerialArmController with preset byte data as input
        while it is connected
        """

        # setup
        self.reset_mocked_sar()
        self.my_sar.is_connected = True

        # test
        self.my_sar.nod()
        out_bytes = self.mock_serial.read(2)

        # check
        assert int(out_bytes[0]) == Command.NOD
        assert int(out_bytes[1]) == 0

    def test_nod_is_not_connected(self):
        """
        Tests nod() method of SerialArmController with preset byte data as input
        while it is not connected
        """

        # setup
        self.reset_mocked_sar()
        self.my_sar.is_connected = False

        # test
        self.my_sar.nod()

        # check
        assert self.my_sar.position.roll == 0
        assert self.my_sar.position.yaw == 0
        assert self.my_sar.position.pitch == 0

    def test_shake_is_connected(self):
        """
        Tests shake() method of SerialArmController with preset byte data as input
        while it is connected
        """

        # setup
        self.reset_mocked_sar()
        self.my_sar.is_connected = True

        # test
        self.my_sar.shake()
        out_bytes = self.mock_serial.read(2)

        # check
        assert int(out_bytes[0]) == Command.SHAKE
        assert int(out_bytes[1]) == 0

    def test_shake_is_not_connected(self):
        """
        Tests shake() method of SerialArmController with preset byte data as input
        while it is not connected
        """

        # setup
        self.reset_mocked_sar()
        self.my_sar.is_connected = False

        # test
        self.my_sar.shake()

        # check
        assert self.my_sar.position.roll == 0
        assert self.my_sar.position.yaw == 0
        assert self.my_sar.position.pitch == 0

    def test_shutdown_is_connected(self):
        """
        Tests _shutdown() method of SerialArmController with preset byte data as input
        while it is connected
        """

        # setup
        self.reset_mocked_sar()
        self.my_sar.is_connected = True

        # test
        self.my_sar._shutdown()
        out_bytes = self.mock_serial.read(2)

        # check
        assert out_bytes is None
        assert self.mock_status_bar.get_status() == "DISCONNECTED"
        assert self.mock_serial.open_bool == False
        assert self.my_sar.is_connected == False

    def test_shutdown_is_not_connected(self):
        """
        Tests shutdown() method of SerialArmController with preset byte data as input
        while it is not connected
        """

        # setup
        self.reset_mocked_sar()
        self.my_sar.is_connected = False

        # test
        self.my_sar._shutdown()

        # check
        assert self.my_sar.position.roll == 0
        assert self.my_sar.position.yaw == 0
        assert self.my_sar.position.pitch == 0


class TestSerialArmControllerNegative:

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

    def test_update_position_is_connected(self):
        """
        Tests update_position() method of SerialArmController with preset byte data as input
        while it is connected. Uses bad byte data to check for error handling.
        """

        # setup
        self.reset_mocked_sar()
        self.my_sar.is_connected = True

        # test
        with pytest.raises(ValueError, match='.*'):
            in_bytes = bytes((256, 100, 300))
            self.mock_serial.write(in_bytes)
            self.my_sar.update_position()

    def test_send_good_bytes_connected(self):
        """
        Tests send() method of SerialArmController with preset byte data as input
        while it is connected. Uses bad byte data to check for error handling.
        """

        #setup
        self.reset_mocked_sar()
        self.my_sar.is_connected = True

        #test
        with pytest.raises(ValueError, match='.*'):
            in_bytes = bytes((360,1,2,3))
            self.my_sar.send(in_bytes)
            out_bytes = self.mock_serial.read(in_bytes.__len__())

    def test_recv_good_bytes_connected(self):
        """
        Tests recv() method of SerialArmController with preset byte data as input
        while it is connected. Uses bad byte data to check for error handling.
        """

        #setup
        self.reset_mocked_sar()
        self.my_sar.is_connected = True

        #test
        with pytest.raises(ValueError, match='.*'):
            in_bytes = bytes((360,2,1))
            self.mock_serial.write(in_bytes)
            out_bytes = self.my_sar.recv()

