import socket
from typing import Tuple, ByteString


class Client:
    _sock = None
    _addr = _port = None
    def __init__(self, addr: str, port: int) -> None:
        self.addr = addr
        self.port = port
        self.connect(self.addr, self.port)
        try:
            while True:
                msg = self.get_input()
                if msg: self.send_msg(msg)
                print(self.recv_msg())
        except KeyboardInterrupt:
            print("[!] Disconnecting...")
            self.disconnect()

    @property
    def sock(self) -> socket.socket:
        return self._sock

    @sock.setter
    def sock(self, value: Tuple[str, int]) -> None:
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.settimeout(1)
        self._sock.connect(value)

    @property
    def addr(self) -> str:
        return self._addr

    @addr.setter
    def addr(self, value: str) -> None:
        self._addr = value

    @property
    def port(self) -> int:
        return self._port

    @port.setter
    def port(self, value: int) -> None:
        self._port = value

    def connect(self, addr: str, port: int) -> None:
        self.sock = (addr, port)
        print(f"[+] Connected to {addr}:{port}")

    def disconnect(self) -> None:
        self.sock.close()
        print(f"[+] Disconnected from {self.addr}:{self.port}")

    def get_input(self) -> str:
        while True:
            msg = str(input(f"chat@{self.addr}:{self.port}> "))
            return msg

    def send_msg(self, msg: str) -> bool:
        self.sock.sendall(msg.encode())
        return True

    def recv_msg(self) -> str:
        try:
            msg = self.sock.recv(1024)
            return msg.decode()
        except TimeoutError:
            return None


if __name__ == "__main__":
    client = Client("192.168.77.119", 50508)
