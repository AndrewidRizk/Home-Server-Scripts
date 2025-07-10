import requests
import sys

def update_duckdns(ip_address: str, domain: str, token: str) -> bool:
    url = f"https://www.duckdns.org/update?domains={domain}&token={token}&ip={ip_address}"
    
    try:
        response = requests.get(url, timeout=10)
        result = response.text.strip()

        if result == "OK":
            return True
        else:
            print(f"DuckDNS returned error: {result}")
            return False
    except Exception as e:
        print(f"Request failed: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python update_duckdns.py <IP_ADDRESS>")
        sys.exit(1)

    ip = sys.argv[1]

    DUCKDNS_DOMAIN1 = "visionmaster"
    DUCKDNS_DOMAIN2 = "androrizk"
    DUCKDNS_TOKEN = ""

    success1 = update_duckdns(ip, DUCKDNS_DOMAIN1, DUCKDNS_TOKEN)
    success2 = update_duckdns(ip, DUCKDNS_DOMAIN2, DUCKDNS_TOKEN)

    print(f"{DUCKDNS_DOMAIN1}: {'Success' if success1 else 'Failure'}")
    print(f"{DUCKDNS_DOMAIN2}: {'Success' if success2 else 'Failure'}")

    # Optional: Overall success
    all_success = success1 and success2
    print(f"Overall Update Status: {'OK' if all_success else 'Failed'}")
