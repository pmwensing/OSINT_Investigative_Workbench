#!/usr/bin/env bash
set -euo pipefail

API="${API:-http://localhost:8088}"

TOKEN="$(curl -s -X POST "$API/api/v1/auth/register"   -H "Content-Type: application/json"   -d '{"email":"admin@example.com","password":"ChangeMe123!","full_name":"Admin"}' | python3 -c 'import sys, json; print(json.load(sys.stdin)["access_token"])')"

INV_ID="$(curl -s -X POST "$API/api/v1/investigations"   -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json"   -d '{"name":"Seed Investigation","description":"Seeded from script"}' | python3 -c 'import sys, json; print(json.load(sys.stdin)["id"])')"

TARGET_ID="$(curl -s -X POST "$API/api/v1/investigations/$INV_ID/targets"   -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json"   -d '{"target_type":"username","value":"example_user","display_name":"example_user"}' | python3 -c 'import sys, json; print(json.load(sys.stdin)["id"])')"

curl -s -X POST "$API/api/v1/investigations/$INV_ID/jobs"   -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json"   -d "{"target_id":"$TARGET_ID","connectors":["manual_import"]}"

echo
echo "Seeded investigation: $INV_ID"
