import pytest
from Mock import MockSerial, MockNotificationsFrame, MockStatusBar
from gui.SerialArmController import SerialArmController, Command, Position

mock_serial = None
mock_notif_frame = None
mock_status_bar = None
my_sar = None

def reset_mocked_sar():
    global mock_serial
    global mock_notif_frame
    global mock_status_bar
    global my_sar
    
    mock_serial = MockSerial()
    mock_notif_frame = MockNotificationsFrame()
    mock_status_bar = MockStatusBar()
    my_sar = SerialArmController(mock_status_bar, mock_notif_frame)
    my_sar._device = mock_serial




def test_close_connected():
    """
    Tests close() method of SerialArmController when it is connected
    """

    #setup
    reset_mocked_sar()
    my_sar.is_connected = True  #sets sar to connected state

    #run test
    my_sar.close()

    #check
    assert mock_status_bar.get_status() == "DISCONNECTED"
    assert mock_serial.open_bool == False
    assert my_sar.is_connected == False

def test_close_not_connected():
    """
    Tests close() method of SerialArmController when it not connected
    """

    #setup
    reset_mocked_sar()
    my_sar.is_connected = False

    #run test
    my_sar.close()

    #check
    assert mock_status_bar.get_status() == None

def test_send_good_bytes_connected():
    """
    Tests send() method of SerialArmController with preset byte data as input
    while it is connected
    """

    #setup
    reset_mocked_sar()
    my_sar.is_connected = True

    #test
    in_bytes = bytes((0,1,2,3))
    my_sar.send(in_bytes)
    out_bytes = mock_serial.read(in_bytes.__len__())

    #check
    assert out_bytes == in_bytes


def test_send_good_bytes_not_connected():
    """
    Tests send() method of SerialArmController with preset byte data as input
    while it is not connected
    """

    #setup
    reset_mocked_sar()
    my_sar.is_connected = False

    #test
    in_bytes = bytes((0, 1, 2, 3))
    my_sar.send(in_bytes)
    out_bytes = mock_serial.read(in_bytes.__len__())

    #check
    assert out_bytes == b''


def test_recv_good_bytes_connected():
    """
    Tests recv() method of SerialArmController with preset byte data as input
    while it is connected
    """

    #setup
    reset_mocked_sar()
    my_sar.is_connected = True

    #test

    in_bytes = bytes((3,2,1))
    mock_serial.write(in_bytes)
    out_bytes = my_sar.recv()

    #check
    assert out_bytes == in_bytes

def test_update_position_not_connected():
    """
    Tests update_position() method of SerialArmController with preset byte data as input
    while it is NOT connected
    """

    #setup
    reset_mocked_sar()
    my_sar.is_connected = False

    #test
    in_bytes = bytes((3, 100, 1))
    mock_serial.write(in_bytes)
    my_sar.update_position()


    #check
    assert my_sar.position.pitch == 0
    assert my_sar.position.yaw == 0
    assert my_sar.position.roll == 0


@pytest.mark.parametrize("input_val", [90,63,172])
def test_set_pitch_connected(input_val):
    """
    Tests set_pitch() method of SerialArmController with preset byte data as input
    while it is connected
    """
    
    #setup
    reset_mocked_sar()
    my_sar.is_connected = True

    #test
    my_sar.set_pitch(input_val)

    out_bytes = mock_serial.read(2)
    assert int(out_bytes[0]) == Command.PITCH
    assert int(out_bytes[1]) == input_val

