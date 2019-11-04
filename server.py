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

        # Check balance
        if data == b'1':
            # send back balance to client
            print(balance)
            c.send(bytes(str(balance), 'utf8'))
        # Withdraw
        if data == b'2':
            withdrawal = c.recv(1024)
            print("Withdraw: ", str(withdrawal, 'utf8'))
            # Check if withdrawal amount is more than current balance.
            if int(withdrawal) < balance:
                balance = balance - int(withdrawal)
                print("New balance: ", balance)
                c.send(bytes(str(balance), 'utf8'))
            else:
                print("Withdrawal amount larger then current balance.")
                c.send(bytes("No", 'utf8'))
        # Deposit
        if data == b'3':
            deposit = c.recv(1024)
            print("Deposit: ", str(deposit, 'utf8'))
            balance = balance + int(deposit)
            print("New balance: ", balance)
            c.send(bytes(str(balance), 'utf8'))
        # connection closed
    c.close()


def Main():
    host = ""

    # reserve a port on your computer
    port = 12345
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    print("socket binded to port", port)

    # put the socket into listening mode
    s.listen(5)
    print("socket is listening")

    # loop until client exits
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
