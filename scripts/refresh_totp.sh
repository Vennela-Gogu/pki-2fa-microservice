#!/bin/sh

# Call the TOTP generation endpoint
curl -X GET http://localhost:8080/generate-2fa >/dev/null 2>&1