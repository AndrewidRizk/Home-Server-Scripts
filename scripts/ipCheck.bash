#!/bin/bash

set -e

# === Config ===
BASE_DIR="/home/androrizk/Desktop/projects/Home-Server-Scripts/scripts"
DUCKDNS_TOKEN_FILE="$BASE_DIR/duckdns_token.txt"
VERCEL_TOKEN_FILE="$BASE_DIR/vercel_token.txt"
PUBLIC_IP_FILE="$BASE_DIR/publicIp.txt"
PYTHON_EMAIL_HELPER="$BASE_DIR/send_email.py"
REDEPLOY_SCRIPT="$BASE_DIR/reDeploy.bash"
UPDATE_SERVER_URL="$BASE_DIR/update_this_server_url.sh"

SENDER_EMAIL="contact.andrewrizk@gmail.com"
SENDER_PASSWORD="uslf xkma osnc qklh"
RECIPIENT_EMAIL="androwmaged47@gmail.com"

# === Fetch public IP ===
public_ip=$(curl -s icanhazip.com)
current_ip=$(cat "$PUBLIC_IP_FILE")

if [ "$public_ip" = "$current_ip" ]; then
    echo "✅ No IP change detected. Exiting."
    exit 0
fi

# Update publicIp.txt
echo "$public_ip" > "$PUBLIC_IP_FILE"

# === Begin Pipeline ===
results="✅ Public IP changed to $public_ip\n"

echo "------------"
echo "🔄 Updating DuckDNS..."
if python3 "$BASE_DIR/duckdns.py" "$public_ip" "$DUCKDNS_TOKEN_FILE"; then
    results+="✅ DuckDNS update succeeded.\n"
else
    results+="❌ DuckDNS update failed.\n"
fi

echo "------------"
echo "🔄 Updating Vercel..."
if python3 "$BASE_DIR/vercel.py" "$public_ip" "$VERCEL_TOKEN_FILE"; then
    results+="✅ Vercel update succeeded.\n"
else
    results+="❌ Vercel update failed.\n"
fi

echo "------------"
echo "🔄 Triggering reDeploy script..."
if "$REDEPLOY_SCRIPT" "$public_ip"; then
    results+="✅ Redeploy script completed.\n"
else
    results+="❌ Redeploy script failed.\n"
fi

echo "------------"
echo "🔄 Updating Python SERVER_URL..."
if "$UPDATE_SERVER_URL" "$public_ip"; then
    results+="✅ Updated server monitor URL.\n"
else
    results+="❌ Failed to update server monitor URL.\n"
fi

echo "------------"
echo "📧 Sending email summary..."
python3 "$PYTHON_EMAIL_HELPER" "$public_ip" "$results" "$SENDER_EMAIL" "$SENDER_PASSWORD" "$RECIPIENT_EMAIL"
