import pytest
from .Mock import MockSerial, MockNotificationsFrame, MockStatusBar, MockSerialArmController
from gui.ControlButtons import ControlButtons
import tkinter as tk
class TestControlButtonsHappy:
    mock_serial = None
    mock_notif_frame = None
    mock_status_bar = None
    mock_sar = None
    my_cb =  None
    master = tk.Tk()
    def reset_mocked_cb(self):

        self.mock_serial = MockSerial()
        self.mock_notif_frame = MockNotificationsFrame()
        self.mock_status_bar = MockStatusBar()
        self.mock_sar = MockSerialArmController()
        self.my_cb = ControlButtons(master= self.master, arm_controller=self.mock_sar, notifications=self.mock_notif_frame)

    def test_open_arm_connected(self):
        """
        Tests open_arm() method of ControlButtons when it is connected
        """

        #setup
        self.reset_mocked_cb()
        self.my_cb.serial_arm_controller.is_connected = True  #sets sar to connected state

        #run test
        self.my_cb.open_arm()

        #check
        assert self.mock_notif_frame.lines[0] == "Opening arm..."
        assert self.mock_sar.open_arm_bool == True

    def test_open_arm_not_connected(self):
        """
        Tests open_arm() method of ControlButtons when it is not connected
        """

        #setup
        self.reset_mocked_cb()
        self.my_cb.serial_arm_controller.is_connected = False  #sets sar to connected state

        #run test
        self.my_cb.open_arm()

        #check
        assert self.mock_notif_frame.lines[0] == "[DISCONNECTED] Opening arm..."
        assert self.mock_sar.open_arm_bool == False

    def test_close_arm_connected(self):
        """
        Tests close_arm() method of ControlButtons when it is connected
        """

        # setup
        self.reset_mocked_cb()
        self.my_cb.serial_arm_controller.is_connected = True  # sets sar to connected state

        # run test
        self.my_cb.close_arm()

        # check
        assert self.mock_notif_frame.lines[0] == "Closing arm..."
        assert self.mock_sar.close_arm_bool == True

    def test_close_arm_not_connected(self):
        """
        Tests close_arm() method of ControlButtons when it is not connected
        """

        # setup
        self.reset_mocked_cb()
        self.my_cb.serial_arm_controller.is_connected = False  # sets sar to connected state

        # run test
        self.my_cb.close_arm()

        # check
        assert self.mock_notif_frame.lines[0] == "[DISCONNECTED] Closing arm..."
        assert self.mock_sar.close_arm_bool == False

    def test_portrait_connected(self):
        """
        Tests portrait() method of ControlButtons when it is connected
        """

        # setup
        self.reset_mocked_cb()
        self.my_cb.serial_arm_controller.is_connected = True  # sets sar to connected state

        # run test
        self.my_cb.portrait()

        # check
        assert self.mock_notif_frame.lines[0] == "Changing to portrait..."
        assert self.mock_sar.portrait_bool == True
        assert self.my_cb.orientation == "PORTRAIT"

    def test_portrait_not_connected(self):
        """
        Tests close_arm() method of ControlButtons when it is not connected
        """

        # setup
        self.reset_mocked_cb()
        self.my_cb.serial_arm_controller.is_connected = False  # sets sar to connected state

        # run test
        self.my_cb.portrait()

        # check
        assert self.mock_notif_frame.lines[0] == "[DISCONNECTED] Changing to portrait..."
        assert self.mock_sar.portrait_bool == False

    def test_landscape_connected(self):
        """
        Tests landscape() method of ControlButtons when it is connected
        """

        # setup
        self.reset_mocked_cb()
        self.my_cb.serial_arm_controller.is_connected = True  # sets sar to connected state

        # run test
        self.my_cb.landscape()

        # check
        assert self.mock_notif_frame.lines[0] == "Changing to landscape..."
        assert self.mock_sar.landscape_bool == True
        assert self.my_cb.orientation == "LANDSCAPE"

    def test_landscape_not_connected(self):
        """
        Tests landscape() method of ControlButtons when it is not connected
        """

        # setup
        self.reset_mocked_cb()
        self.my_cb.serial_arm_controller.is_connected = False  # sets sar to connected state

        # run test
        self.my_cb.landscape()

        # check
        assert self.mock_notif_frame.lines[0] == "[DISCONNECTED] Changing to landscape..."
        assert self.mock_sar.landscape_bool == False

    def test_tilt_connected(self):
        """
        Tests tilt() method of ControlButtons when it is connected
        """

        # setup
        self.reset_mocked_cb()
        self.my_cb.serial_arm_controller.is_connected = True  # sets sar to connected state

        # run test
        self.my_cb.tilt()

        # check
        assert self.mock_notif_frame.lines[0] == "Tilting head..."
        assert self.mock_sar.tilt_bool == True

    def test_tilt_not_connected(self):
        """
        Tests tilt() method of ControlButtons when it is not connected
        """

        # setup
        self.reset_mocked_cb()
        self.my_cb.serial_arm_controller.is_connected = False  # sets sar to connected state

        # run test
        self.my_cb.tilt()

        # check
        assert self.mock_notif_frame.lines[0] == "[DISCONNECTED] Tilting head..."
        assert self.mock_sar.tilt_bool == False

    def test_nod_connected(self):
        """
        Tests nod() method of ControlButtons when it is connected
        """

        # setup
        self.reset_mocked_cb()
        self.my_cb.serial_arm_controller.is_connected = True  # sets sar to connected state

        # run test
        self.my_cb.nod()

        # check
        assert self.mock_notif_frame.lines[0] == "Nodding head..."
        assert self.mock_sar.nod_bool == True

    def test_nod_not_connected(self):
        """
        Tests nod() method of ControlButtons when it is not connected
        """

        # setup
        self.reset_mocked_cb()
        self.my_cb.serial_arm_controller.is_connected = False  # sets sar to connected state

        # run test
        self.my_cb.nod()

        # check
        assert self.mock_notif_frame.lines[0] == "[DISCONNECTED] Nodding head..."
        assert self.mock_sar.nod_bool == False

    def test_shake_connected(self):
        """
        Tests shake() method of ControlButtons when it is connected
        """

        # setup
        self.reset_mocked_cb()
        self.my_cb.serial_arm_controller.is_connected = True  # sets sar to connected state

        # run test
        self.my_cb.shake()

        # check
        assert self.mock_notif_frame.lines[0] == "Shaking head..."
        assert self.mock_sar.shake_bool == True

    def test_shake_not_connected(self):
        """
        Tests shake() method of ControlButtons when it is not connected
        """

        # setup
        self.reset_mocked_cb()
        self.my_cb.serial_arm_controller.is_connected = False  # sets sar to connected state

        # run test
        self.my_cb.shake()

        # check
        assert self.mock_notif_frame.lines[0] == "[DISCONNECTED] Shaking head..."
        assert self.mock_sar.shake_bool == False

    def test_shutdown_connected(self):
        """
        Tests shutdown() method of ControlButtons when it is connected
        """

        # setup
        self.reset_mocked_cb()
        self.my_cb.serial_arm_controller.is_connected = True  # sets sar to connected state

        # run test
        self.my_cb.shutdown()

        # check
        assert self.mock_notif_frame.lines[0] == "Shutting down..."
        assert self.mock_sar.shutdown_bool == True

    def test_shutdown_not_connected(self):
        """
        Tests shutdown() method of ControlButtons when it is not connected
        """

        # setup
        self.reset_mocked_cb()
        self.my_cb.serial_arm_controller.is_connected = False  # sets sar to connected state

        # run test
        self.my_cb.shutdown()

        # check
        assert self.mock_notif_frame.lines[0] == "[DISCONNECTED] Shutting down..."
        assert self.mock_sar.shutdown_bool == False





