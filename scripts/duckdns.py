import sys
import requests

def read_token(file_path):
    try:
        with open(file_path, 'r') as f:
            token = f.read().strip()
            return token
    except FileNotFoundError:
        print(f"Error: Cannot find token file at {file_path}")
        sys.exit(1)

def update_duckdns(ip_address, domain, token):
    url = f"https://www.duckdns.org/update?domains={domain}&token={token}&ip={ip_address}"
    try:
        response = requests.get(url, timeout=10)
        return response.text.strip() == "OK"
    except Exception as e:
        print(f"Request failed: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python duckdns.py <IP_ADDRESS> <token_file>")
        sys.exit(1)

    ip = sys.argv[1]
    token_file = sys.argv[2]

    # Hardcoded domain names
    DOMAIN1 = "visionmaster"
    DOMAIN2 = "androrizk"

    token = read_token(token_file)

    success1 = update_duckdns(ip, DOMAIN1, token)
    success2 = update_duckdns(ip, DOMAIN2, token)

    print(f"{DOMAIN1}: {'Success' if success1 else 'Failed'}")
    print(f"{DOMAIN2}: {'Success' if success2 else 'Failed'}")

    all_ok = success1 and success2
    print("Overall:", "OK" if all_ok else "Some Failed")
