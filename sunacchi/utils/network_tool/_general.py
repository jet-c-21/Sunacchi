# coding: utf-8
"""
Author: Jet C.
GitHub: https://github.com/jet-c-21
Create Date: 10/10/24
"""
from typing import Optional
import socket


def port_is_connectable(host: Optional[str] = "localhost", port: int = 16888) -> bool:
    """Tries to connect to the server at port to see if it is running.

    :Args:
     - port - The port to connect.
    """
    if not isinstance(port, int):
        raise TypeError(f"input port type is invalid: {port}, type: {type(port)}")

    socket_ = None
    _is_connectable_exceptions = (socket.error, ConnectionResetError)
    try:
        socket_ = socket.create_connection((host, port), 1)
        result = True
    except _is_connectable_exceptions:
        result = False
    finally:
        if socket_:
            socket_.close()

    return result
