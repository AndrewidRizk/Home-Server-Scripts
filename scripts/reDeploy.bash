#!/bin/bash

# ✅ Ensure script stops on error
set -e

# ✅ Check if an IP address was provided
if [ -z "$1" ]; then
  echo "Usage: $0 <new-ip-address>"
  exit 1
fi

newIP=$1

# ✅ Change to your project directory
cd ~/Desktop/projects/Englishify-public
git remote set-url origin git@github.com:AndrewidRizk/Englishify-public.git

# ✅ Log the new IP to deploy.txt
echo "$newIP" >> deploy.txt

# ✅ Git commit and push
git add deploy.txt
git commit -m "Automated -> deploy new IP: $newIP"
git push

