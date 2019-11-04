# import socket programming library
import socket

# import thread module
from _thread import *
import threading

print_lock = threading.Lock()

balance = 10000


# thread function
def threaded(c):
    global balance
    while True:

        # data received from client
        data = c.recv(1024)
        if not data:
            print('Bye')

            # lock released on exit
            print_lock.release()
            break

        if data == b'1':
            # send back balance to client
            print(balance)
            c.send(bytes(str(balance), 'utf8'))
        if data == b'2':
            withdrawal = c.recv(1024)
            print("Withdraw: ", str(withdrawal, 'utf8'))
            if int(withdrawal) < balance:
                balance = balance - int(withdrawal)
                print("New balance: ", balance)
                c.send(bytes(str(balance), 'utf8'))
            else:
                print("Withdrawal amount larger then current balance.")
                c.send(bytes("No", 'utf8'))
        if data == b'3':
            deposit = c.recv(1024)
            print("Withdraw: ", str(deposit, 'utf8'))
            balance = balance + int(deposit)
            print("New balance: ", balance)
            c.send(bytes(str(balance), 'utf8'))
        # connection closed
    c.close()


def Main():
    host = ""

    # reverse a port on your computer
    # in our case it is 12345 but it
    # can be anything
    port = 12345
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    print("socket binded to port", port)

    # put the socket into listening mode
    s.listen(5)
    print("socket is listening")

    # a forever loop until client wants to exit
    while True:
        # establish connection with client
        c, addr = s.accept()

        # lock acquired by client
        print_lock.acquire()
        print('Connected to :', addr[0], ':', addr[1])

        # Start a new thread and return its identifier
        start_new_thread(threaded, (c,))
    s.close()


if __name__ == '__main__':
    Main()
