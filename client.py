# Import socket module
import socket


def Main():
    # local host IP '127.0.0.1'
    host = '127.0.0.1'

    # Define the port on which you want to connect
    port = 12345

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect to server on local computer
    s.connect((host, port))

    while True:
        # ask the client whether he wants to continue
        ans = input('\nWhat would you like to do?'
                    '\n1: Check balance'
                    '\n2: Withdrawal'
                    '\n3: Deposit'
                    '\nq: End the current session\n: ')
        if ans == '1':
            s.send(ans.encode('ascii'))
            data = s.recv(1024)
            print('\nCurrent balance :', str(data, 'utf8'))
            continue
        if ans == '2':
            s.send(ans.encode('ascii'))
            withdraw = input('\n How much to withdrawal? : ')
            s.send(withdraw.encode('ascii'))
            data = s.recv(1024)
            if data == b'No':
                print("\nNot enough funds.")
            else:
                print('\nBalance after withdrawal :', str(data, 'utf8'))
            continue
        if ans == '3':
            s.send(ans.encode('ascii'))
            withdraw = input('\n How much to deposit? : ')
            s.send(withdraw.encode('ascii'))
            data = s.recv(1024)
            print('\nBalance after withdrawal :', str(data, 'utf8'))
            continue
        if ans == 'q':
            print("\nEnding session")
            break
        else:
            print("\nNot a valid input, try again.")
            continue
    # close the connection
    s.close()


if __name__ == '__main__':
    Main()
