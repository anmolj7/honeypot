import socket
import os
import atexit

LOGS = []


def breakline():
    print('-' * 60)


def clear():
    os.system('clear')


def write_to_file():
    pass


def on_exit():
    global LOGS
    clear()
    print('Saving To File logs.txt')
    with open('logs.txt', 'a+') as f:
        LOGS = [log + '\n' for log in LOGS]
        f.writelines(LOGS)


atexit.register(on_exit)


class SSH:
    WELCOME = """Welcome to BackBox Linux 4.5 (GNU/Linux 4.2.0-30-generic i686)\n
     * Documentation:  http://www.backbox.org/\n\n
    The programs included with the BackBox/Ubuntu system are free software;
    the exact distribution terms for each program are described in the
    individual files in /usr/share/doc/*/copyright.\n
    BackBox/Ubuntu comes with ABSOLUTELY NO WARRANTY, to the extent
    permitted by applicable law.\n
    """

    def __init__(self, IP='192.168.43.206', listeners=3, PORT=6969):
        global LOGS
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((IP, PORT))  # binding for the ssh port!
        self.sock.listen(listeners)
        clear()
        print(f'SSH Honeypot Ready! Waiting For Attackers!')
        breakline()
        print(f'Starting Listening on {self.sock.getsockname()[0]}:{PORT}')
        breakline()
        n = 0
        while True:
            n += 1
            conn, attacker = self.sock.accept()
            ip, port = attacker
            conn.send(bytes('Login as: ', "utf8"))
            login = conn.recv(1024)
            login = login.decode('utf8')
            login = login.split('\r\n')[0]
            conn.send(bytes(f'{login}@host\'s password: ', "utf8"))
            _ = conn.recv(1024)
            PROMPT = login+'@host:~$ '
            conn.send(bytes(self.WELCOME, "utf8"))
            LOGS.append(f'[{n}] IP: {ip}:{port}')
            print(LOGS[-1])
            while True:
                conn.send(bytes(PROMPT, "utf8"))
                data = conn.recv(1024)
                data = data.decode('utf8')
                data = data.split('\r\n')[0]

                LOGS.append(f"[{ip}]: COMMAND: {data}")
                print(LOGS[-1])
                conn.send(bytes(f'{data}: command not found.\n', "utf8"))
            conn.close()


if __name__ == '__main__':
    s = SSH(PORT=69)
