#!/bin/bash

security add-trusted-cert -d -r trustRoot -k /Library/Keychains/System.keychain config/fleet.local.crt
echo "$(ipconfig getifaddr en1)   fleet.local" | tee -a /etc/hosts > /dev/null
