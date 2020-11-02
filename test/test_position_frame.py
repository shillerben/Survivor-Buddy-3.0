import pytest
from Mock import MockSerial, MockNotificationsFrame, MockStatusBar, MockLogFile, MockSerialArmController, MockSpinBox, MockSlider
from gui.tkvlc import Player
from gui.PositionFrame import LabelScaleSpinbox

import tkinter as tk


class TestNotificationsFrameHappy:

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
