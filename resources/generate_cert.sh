#!/bin/bash

# Directory where the certificate and key will be stored
CERT_DIR="$HOME/.nginx"

# Certificate and key configuration
ALG_NAME="rsa"
ALG_SIZE="4096"
DAYS="3650"
CN="ip.aumaton.com"


# Check if the directory exists, create if not
if [ ! -d "$CERT_DIR" ]; then
  mkdir -p "$CERT_DIR"
fi

# Set the filenames
CERT_FILE="$CERT_DIR/cert.pem"
KEY_FILE="$CERT_DIR/key.pem"

# Generate the key and certificate
openssl req -x509 -newkey $ALG_NAME:$ALG_SIZE -keyout "$KEY_FILE" -out "$CERT_FILE" -days $DAYS -nodes -subj "/CN=$CN"

echo "Certificate and key have been generated in $CERT_DIR"
