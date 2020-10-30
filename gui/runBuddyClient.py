from BuddyAudioClient import BuddyAudioClient

host = '192.168.1.31'
port = 5050
mbac = BuddyAudioClient(host, port)
mbac.connect()
print("Connected")
mbac.startStream()
