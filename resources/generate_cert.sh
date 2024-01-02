#!/bin/bash

# Key and certificate configuration
ALG_NAME=${ALG_NAME:-rsa}
ALG_SIZE=${ALG_SIZE:-4096}
DAYS=${DAYS:-3650}
CN=${CN:-ipask.me}

# Directory where the key and certificate will be stored
CERT_DIR="$HOME/.nginx"

# Make sure CERT_DIR exists
if [ ! -d "$CERT_DIR" ]; then
  mkdir -p "$CERT_DIR"
fi

# Set the filenames
KEY_FILE="$CERT_DIR/key.pem"
CERT_FILE="$CERT_DIR/cert.pem"

# Generate the key and certificate
openssl req -x509 -newkey $ALG_NAME:$ALG_SIZE -keyout "$KEY_FILE" -out "$CERT_FILE" -days $DAYS -nodes -subj "/CN=$CN"

echo "Key and certificate have been generated in $CERT_DIR"
