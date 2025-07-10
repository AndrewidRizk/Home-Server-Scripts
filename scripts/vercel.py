import sys
import requests
import json
import time

def read_token(token_file):
    try:
        with open(token_file, "r") as f:
            token = f.read().strip()
            print(f"[Token Loaded] {token[:5]}...")  # Partial print for safety
            return token
    except Exception as e:
        print(f"Error reading token: {e}")
        sys.exit(1)

def update_env_var(project_id, var_name, value, target, headers):
    env_url = f"https://api.vercel.com/v10/projects/{project_id}/env"
    
    existing = requests.get(env_url, headers=headers).json()
    for env in existing.get("envs", []):
        if env["key"] == var_name:
            del_url = f"{env_url}/{env['id']}"
            del_resp = requests.delete(del_url, headers=headers)
            if del_resp.status_code != 200:
                print(f"Failed to delete old env: {del_resp.text}")
                return False
    
    payload = {
        "key": var_name,
        "value": value,
        "target": [target],
        "type": "encrypted"
    }
    resp = requests.post(env_url, headers=headers, data=json.dumps(payload))
    if resp.status_code not in [200, 201]:
        print(f"Failed to add env var: {resp.status_code} — {resp.text}")
    return resp.status_code == 200 or resp.status_code == 201

def get_latest_deployment(project_id, headers):
    url = f"https://api.vercel.com/v6/deployments?projectId={project_id}&limit=1"
    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        print(f"Failed to fetch deployments: {resp.text}")
        return None
    deployments = resp.json().get("deployments", [])
    if not deployments:
        print("No deployments found.")
        return None
    return deployments[0]["uid"]

def trigger_fresh_deploy(project_id, headers):
    deployment_id = get_latest_deployment(project_id, headers)
    if not deployment_id:
        return False

    url = f"https://api.vercel.com/v13/deployments/{deployment_id}/redeploy"

    # Add this header to force redeploy and bypass loop protection
    headers_with_force = headers.copy()
    headers_with_force["X-Vercel-Force"] = "1"

    resp = requests.post(url, headers=headers_with_force)

    if resp.status_code not in [200, 201]:
        print(f"Failed to redeploy: {resp.status_code} — {resp.text}")
        return False

    print(f"✅ Triggered redeploy from deployment ID: {deployment_id}")
    return True

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python vercel.py <IP_ADDRESS> <token_file>")
        sys.exit(1)

    ip = sys.argv[1]
    token_file = sys.argv[2]

    project_name = "englishify-public"
    project_id = "prj_vb2gnAyWxD7BmKwbZIOXlxmJ3LH2"
    token = read_token(token_file)

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }


    updated = update_env_var(project_id, "DB_HOST", ip, "production", headers)
    if not updated:
        print("❌ Failed to update env variable.")
        sys.exit(1)

    print("Sucess")
