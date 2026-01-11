import os
import socket
from dotenv import load_dotenv

load_dotenv(override=True)

url = os.getenv("DATABASE_URL", "")
print(f"Loaded URL: '{url}'")

if "@" in url:
    try:
        # Parse host carefully
        # postgresql://user:pass@host:port/dbname
        part = url.split("@")[1]
        host = part.split(":")[0]
        if "/" in host: # in case port is missing
            host = host.split("/")[0]
            
        print(f"Extracted Host: '{host}' (Length: {len(host)})")
        print("Character codes:", [ord(c) for c in host])
        
        print("\nResolving with socket.gethostbyname (IPv4)...")
        try:
            ip = socket.gethostbyname(host)
            print(f"SUCCESS: Resolved to {ip}")
        except Exception as e:
            print(f"FAILURE: socket.gethostbyname raised: {e}")
            
        print("\nResolving with socket.getaddrinfo (IPv4/IPv6)...")
        try:
            infos = socket.getaddrinfo(host, 5432)
            for info in infos:
                print(f" - {info[4]}")
        except Exception as e:
            print(f"FAILURE: socket.getaddrinfo raised: {e}")

    except Exception as e:
        print(f"Parsing error: {e}")
else:
    print("URL does not seem to contain '@' symbol.")
