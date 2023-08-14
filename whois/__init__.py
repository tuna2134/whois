import socket
import re
import asyncio

from typing import Tuple


def get_whois_info(
    domain_name: str, whois_server: str = "whois.iana.org", port: int = 43
) -> str:
    whois_query = f"{domain_name}\r\n"

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((whois_server, port))
        s.send(whois_query.encode())
        response = b""
        while True:
            data = s.recv(1024)
            if not data:
                break
            response += data
    data = response.decode()
    is_refer, data = get_refer_target(data)
    if is_refer:
        return get_whois_info(domain_name, data)
    return data

def get_refer_target(data: str) -> Tuple[bool, str]:
    if "refer" in data:
        whois_server = re.findall("refer: *([^\n]*)", data)[0]
        return True, whois_server
    return False, data

async def get_whois_info_async(
    domain_name: str, whois_server: str = "whois.iana.org", port: int = 43
) -> str:
    whois_query = f"{domain_name}\r\n"

    reader, writer = await asyncio.open_connection(whois_server, port)
    writer.write(whois_query.encode())
    await writer.drain()
    response = b""
    while True:
        data = await reader.read(1024)
        if not data:
            break
        response += data
    data = response.decode()
    writer.close()
    await writer.wait_closed()
    is_refer, data = get_refer_target(data)
    if is_refer:
        return await get_whois_info_async(data)
    return data