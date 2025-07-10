#!/bin/bash

set -e

# === Config ===
DUCKDNS_TOKEN_FILE="scripts/duckdns_token.txt"
VERCEL_TOKEN_FILE="scripts/vercel_token.txt"
PUBLIC_IP_FILE="scripts/publicIp.txt"
PYTHON_EMAIL_HELPER="scripts/send_email.py"  # We'll define this below

SENDER_EMAIL="${SENDER_EMAIL:-your_email@gmail.com}"
SENDER_PASSWORD="${SENDER_PASSWORD:-your_app_password}"
RECIPIENT_EMAIL="${RECIPIENT_EMAIL:-recipient@example.com}"

# === Fetch public IP ===
public_ip=$(curl -s icanhazip.com)
current_ip=$(cat "$PUBLIC_IP_FILE")

if [ "$public_ip" = "$current_ip" ]; then
    echo "✅ No IP change detected. Exiting."
    python3 "$PYTHON_EMAIL_HELPER" "No Change" "$public_ip" "$SENDER_EMAIL" "$SENDER_PASSWORD" "$RECIPIENT_EMAIL"
    exit 0
fi

# Update publicIp.txt
echo "$public_ip" > "$PUBLIC_IP_FILE"

# === Begin Pipeline ===
results="Public IP changed to $public_ip\n\n"

# DuckDNS Update
echo "🔄 Updating DuckDNS..."
if python3 scripts/duckdns.py "$public_ip" "$DUCKDNS_TOKEN_FILE"; then
    results+="✅ DuckDNS update succeeded.\n"
else
    results+="❌ DuckDNS update failed.\n"
fi

# Vercel Update
echo "🔄 Updating Vercel..."
if python3 scripts/vercel.py "$public_ip" "$VERCEL_TOKEN_FILE"; then
    results+="✅ Vercel update succeeded.\n"
else
    results+="❌ Vercel update failed.\n"
fi
# Redeploy (optional custom logic)
echo "🔄 Triggering reDeploy script..."
if ./scripts/reDeploy.bash "$public_ip"; then
    results+="✅ Redeploy script completed.\n"
else
    results+="❌ Redeploy script failed.\n"
fi

# Update server monitor file
echo "🔄 Updating Python SERVER_URL..."
if ./scripts/update-server-url.sh "$public_ip"; then
    results+="✅ Updated server monitor URL.\n"
else
    results+="❌ Failed to update server monitor URL.\n"
fi


# === Send Email Summary ===
python3 "$PYTHON_EMAIL_HELPER" "Server Update Status" "$results" "$SENDER_EMAIL" "$SENDER_PASSWORD" "$RECIPIENT_EMAIL"
