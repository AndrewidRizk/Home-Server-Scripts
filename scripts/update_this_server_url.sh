#!/bin/bash

# Exit on error
set -e

# 🔹 Check for IP argument
if [ -z "$1" ]; then
  echo "Usage: $0 <NEW_IP_ADDRESS>"
  exit 1
fi

NEW_IP="$1"
cd ../
git remote set-url origin git@github.com:AndrewidRizk/Home-Server-Scripts
PYTHON_FILE="./server_ping_notify.py"  

# 🔹 Replace the IP address in SERVER_URL
sed -i "s|^\s*SERVER_URL = \".*\"|SERVER_URL = \"http://$NEW_IP:5000/\"|" "$PYTHON_FILE"
echo "$NEW_IP" >> deploy.txt
# 🔹 Git commit & push
git add "$PYTHON_FILE"
git add deploy.txt
git commit -m "Update SERVER_URL to $NEW_IP"
git push
