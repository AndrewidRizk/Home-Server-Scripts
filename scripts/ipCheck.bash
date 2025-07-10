#! /bin/bash

public_ip=$(curl -s icanhazip.com)
current_ip=$(cat publicIp.txt)

if [ "$public_ip" = "$current_ip" ]; then
    echo "No change required"
else
    echo "Public Ip address changed.."
    echo "Changing the Ip address.."
    curl -s icanhazip.com > publicIp.txt
    cat publicIp.txt
    current_ip=$(cat publicIp.txt)
    if [ "$public_ip" = "$current_ip" ]; then
    	echo "change successful"
    fi
    
fi
