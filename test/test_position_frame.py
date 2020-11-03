import pytest
from .Mock import MockSerial, MockNotificationsFrame, MockStatusBar, MockLogFile, MockSerialArmController, MockSpinBox, MockSlider
import gui.tkvlc
from gui.PositionFrame import LabelScaleSpinbox

import tkinter as tk


class TestLabelScaleSpinboxHappy:

    mock_serial = None
    mock_notif_frame = None
    mock_status_bar = None
    master = tk.Tk()
    lss = None
    def reset_mocked(self):

        self.mock_serial = MockSerial()
        self.mock_notif_frame = MockNotificationsFrame()
        self.mock_status_bar = MockStatusBar()
        self.lss = LabelScaleSpinbox(master=self.master)
        self.lss.serial_arm_controller = MockSerialArmController()
        self.lss.slider = MockSlider()
        self.lss.spinbox = MockSpinBox()

    def test_increment(self):
        """
        Tests increment() method of LabelScaleSpinBox
        """

        #setup
        self.reset_mocked()

        #run test
        self.lss.increment()

        #check
        assert self.lss.spinbox.val == 1
        assert self.lss.current_value == 1

    def test_decrement(self):
        """
        Tests decrement() method of LabelScaleSpinBox
        """

        #setup
        self.reset_mocked()

        #run test
        self.lss.decrement()

        #check
        assert self.lss.spinbox.val == -1
        assert self.lss.current_value == -1

    @pytest.mark.parametrize("input_val", [0, 45, 90])
    def test_slider_update(self, input_val):
        """
        Tests slider_update() method of LabelScaleSpinBox
        """

        #setup
        self.reset_mocked()

        #run test
        self.lss.slider.set(input_val)
        self.lss.sliderUpdate(input_val)

        #check
        assert self.lss.spinbox.val == input_val
        assert self.lss.current_value == input_val


    def test_set_slider(self):
        """
        Tests set_slider() method of LabelScaleSpinBox
        """

        #setup
        self.reset_mocked()

        #run test
        self.lss.spinbox.set(50)
        self.lss.set_slider()

        #check
        assert self.lss.slider.val == 50
        assert self.lss.current_value == 50

    @pytest.mark.parametrize("input_val", [0, 45, 90])
    def test_send_command_axis_0_connected(self, input_val):
        """
        Tests send_command() method of LabelScaleSpinBox with serial arm connected and axis set to 0
        """

        #setup
        self.reset_mocked()
        self.lss.serial_arm_controller.is_connected = True
        self.lss.axis = 0
        self.lss.current_value = input_val

        #run test
        self.lss.send_command()

        #check
        assert self.lss.serial_arm_controller.pitch == input_val

    @pytest.mark.parametrize("input_val", [0, 45, 90])
    def test_send_command_axis_1_connected(self, input_val):
        """
        Tests send_command() method of LabelScaleSpinBox with serial arm connected and axis set to 1
        """

        #setup
        self.reset_mocked()
        self.lss.serial_arm_controller.is_connected = True
        self.lss.axis = 1
        self.lss.current_value = input_val

        #run test
        self.lss.send_command()

        #check
        assert self.lss.serial_arm_controller.yaw == input_val

    @pytest.mark.parametrize("input_val", [0, 45, 90])
    def test_send_command_axis_2_connected(self, input_val):
        """
        Tests send_command() method of LabelScaleSpinBox with serial arm connected and axis set to 2
        """

        #setup
        self.reset_mocked()
        self.lss.serial_arm_controller.is_connected = True
        self.lss.axis = 2
        self.lss.current_value = input_val

        #run test
        self.lss.send_command()

        #check
        assert self.lss.serial_arm_controller.roll == input_val

    @pytest.mark.parametrize("input_val", [0, 45, 90])
    def test_send_command_axis_0_not_connected(self, input_val):
        """
        Tests send_command() method of LabelScaleSpinBox with serial arm not connected and axis set to 0
        """

        # setup
        self.reset_mocked()
        self.lss.serial_arm_controller.is_connected = False
        self.lss.axis = 0
        self.lss.current_value = input_val

        # run test
        self.lss.send_command()

        # check
        assert self.lss.serial_arm_controller.pitch == 0

    @pytest.mark.parametrize("input_val", [0, 45, 90])
    def test_send_command_axis_1_not_connected(self, input_val):
        """
        Tests send_command() method of LabelScaleSpinBox with serial arm not connected and axis set to 1
        """

        # setup
        self.reset_mocked()
        self.lss.serial_arm_controller.is_connected = False
        self.lss.axis = 1
        self.lss.current_value = input_val

        # run test
        self.lss.send_command()

        # check
        assert self.lss.serial_arm_controller.yaw == 0

    @pytest.mark.parametrize("input_val", [0, 45, 90])
    def test_send_command_axis_2_not_connected(self, input_val):
        """
        Tests send_command() method of LabelScaleSpinBox with serial arm not connected and axis set to 2
        """

        # setup
        self.reset_mocked()
        self.lss.serial_arm_controller.is_connected = False
        self.lss.axis = 2
        self.lss.current_value = input_val

        # run test
        self.lss.send_command()

        # check
        assert self.lss.serial_arm_controller.roll == 0

    @pytest.mark.parametrize("input_val", [0, 5, 7])
    def test_validate_spinbox_positive(self, input_val):
        """
        Tests validate_spinbox() method of LabelScaleSpinBox with values that will work
        """

        # setup
        self.reset_mocked()

        # run test
        self.lss.validate_spinbox(input_val)

        # check
        assert self.lss.slider.val == input_val

    @pytest.mark.parametrize("input_val", [-5, 20, 90])
    def test_validate_spinbox_negative(self, input_val):
        """
        Tests validate_spinbox() method of LabelScaleSpinBox with values that won't work
        """

        # setup
        self.reset_mocked()

        # run test
        self.lss.validate_spinbox(input_val)

        # check
        assert self.lss.spinbox.val == '0'


