import socket
from typing import Tuple


class Server:
    _sock = _addr = _port = None
    def __init__(self, addr: str, port: int) -> None:
        self.sock = (addr, port)
        self.addr = addr
        self.port = port

        self.clients = []
        self.buffer = []
        
        while True:
            try:
                self.sock.listen(1)
                conn, addr = self.sock.accept()
                conn.settimeout(1)
                print("Connected by:", addr)
                self.clients.append([conn, addr])
            except TimeoutError:
                pass

            self.recv_msg()
            

    @property
    def sock(self) -> socket.socket:
        return self._sock

    @sock.setter
    def sock(self, value: Tuple[str, int]) -> None:
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.settimeout(1)
        self._sock.bind(value)
        print(f"[+] Listening on {value[0]}:{value[1]}")

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

    def recv_msg(self) -> str:
        for conn, addr in self.clients:
            try:
                data = conn.recv(1024)
                if not data: continue
                print(f"Got {data.decode()} from {addr}")
                self.buffer.append([addr, data.decode()])
                self.redistribute()
            except TimeoutError:
                continue

    def redistribute(self) -> bool:
        to_remove = []
        for i, [conn, addr] in enumerate(self.clients):
            try:
                conn.sendall(self.buffer[-1][1].encode())
            except:  # Client disconnected
                print(f"[!] {addr} disconnected")
                to_remove.append(i)
        if to_remove:
            for i, indx in enumerate(to_remove):
                self.clients.pop(indx - i)


if __name__ == "__main__":
    server = Server("192.168.77.119", 50508)
