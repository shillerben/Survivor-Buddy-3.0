import pytest
from .Mock import MockSerial, MockNotificationsFrame, MockStatusBar, MockLogFile
from gui.NotificationsFrame import NotificationFrame
import tkinter as tk
from datetime import datetime
class TestNotificationsFrameHappy:

    mock_serial = None
    mock_notif_frame = None
    mock_status_bar = None
    master = tk.Tk()

    def reset_mocked(self):

        self.mock_serial = MockSerial()
        self.log_file = MockLogFile()
        self.notif_frame = NotificationFrame(master=self.master, _logFile=self.log_file)

    @pytest.mark.parametrize("input_val", ['hello', 'hello world', 'goodbye'])
    def test_append_line(self, input_val):
        """
        Tests append_line() method of Notifications_frame with preset data
        """

        # setup
        self.reset_mocked()

        # test
        now = datetime.now()
        self.notif_frame.append_line(input_val)
        timestamp = now.strftime("%H:%M:%S")

        # check
        assert self.log_file.arr[0] == timestamp + " - " + input_val + "\n"