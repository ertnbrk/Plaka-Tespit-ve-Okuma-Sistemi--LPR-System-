import os
import socket
from dotenv import load_dotenv

load_dotenv(override=True)

url = os.getenv("DATABASE_URL", "")

with open("dns_debug_result_utf8.txt", "w", encoding="utf-8") as f:
    f.write(f"Loaded URL_Raw: '{url}'\n")

    if "@" in url:
        try:
            part = url.split("@")[1]
            host = part.split(":")[0]
            if "/" in host:
                host = host.split("/")[0]

            f.write(f"Extracted Host: '{host}' (Length: {len(host)})\n")
            f.write(f"Character codes: {[ord(c) for c in host]}\n")
            
            f.write("\nResolving with socket.gethostbyname (IPv4)...\n")
            try:
                ip = socket.gethostbyname(host)
                f.write(f"SUCCESS: Resolved to {ip}\n")
            except Exception as e:
                f.write(f"FAILURE: socket.gethostbyname raised: {e}\n")
                
            f.write("\nResolving with socket.getaddrinfo...\n")
            try:
                infos = socket.getaddrinfo(host, 5432)
                for info in infos:
                    f.write(f" - {info[4]}\n")
            except Exception as e:
                f.write(f"FAILURE: socket.getaddrinfo raised: {e}\n")

        except Exception as e:
            f.write(f"Parsing error: {e}\n")
    else:
        f.write("URL does not seem to contain '@' symbol.\n")
