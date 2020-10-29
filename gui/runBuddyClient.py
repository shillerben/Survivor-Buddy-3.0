from BuddyMessageClient import BuddyMessageClient

host = '192.168.1.31'
port = 5050
myBuddyClient = BuddyMessageClient(host,port)

while True:
    my_str = input('Enter input: ')
    myBuddyClient.sendMsg(my_str)