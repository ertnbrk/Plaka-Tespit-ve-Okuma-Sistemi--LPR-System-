#!/bin/bash

# Simple Token Generator (No jq required)
# Uses Python for JSON parsing

BASE_URL="http://127.0.0.1:8000"

echo "============================================"
echo "  API Token Generator"
echo "============================================"
echo ""

# Get Officer Token
echo "→ Getting Officer Token..."
OFFICER_RESPONSE=$(curl -s -X POST "${BASE_URL}/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test_officer@example.com",
    "password": "test123"
  }')

OFFICER_TOKEN=$(echo "$OFFICER_RESPONSE" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('token', ''))" 2>/dev/null)

if [ -n "$OFFICER_TOKEN" ]; then
    echo "✓ Officer Token obtained"
else
    echo "✗ Failed to get officer token (user might not exist)"
    echo "  Run: python test_frontend_api.py first to create test users"
fi

# Get Admin Token
echo "→ Getting Admin Token..."
ADMIN_RESPONSE=$(curl -s -X POST "${BASE_URL}/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@example.com",
    "password": "admin123"
  }')

ADMIN_TOKEN=$(echo "$ADMIN_RESPONSE" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('token', ''))" 2>/dev/null)

if [ -n "$ADMIN_TOKEN" ]; then
    echo "✓ Admin Token obtained"
else
    echo "✗ Failed to get admin token"
fi

echo ""
echo "============================================"
echo "  Tokens:"
echo "============================================"
echo ""
echo "Officer Token:"
echo "$OFFICER_TOKEN"
echo ""
echo "Admin Token:"
echo "$ADMIN_TOKEN"
echo ""
echo "============================================"
echo "  Export Commands (copy and paste):"
echo "============================================"
echo ""
echo "export BASE_URL='${BASE_URL}'"
echo "export OFFICER_TOKEN='${OFFICER_TOKEN}'"
echo "export ADMIN_TOKEN='${ADMIN_TOKEN}'"
echo ""
echo "============================================"
echo "  Quick Test Commands:"
echo "============================================"
echo ""
echo "# Get complaints as officer:"
echo "curl -X GET \"\${BASE_URL}/complaints/\" -H \"Authorization: Bearer \${OFFICER_TOKEN}\""
echo ""
echo "# Get all complaints as admin:"
echo "curl -X GET \"\${BASE_URL}/complaints/\" -H \"Authorization: Bearer \${ADMIN_TOKEN}\""
echo ""
echo "# Create complaint:"
echo "curl -X POST \"\${BASE_URL}/complaints/\" \\"
echo "  -H \"Content-Type: application/json\" \\"
echo "  -H \"Authorization: Bearer \${OFFICER_TOKEN}\" \\"
echo "  -d '{\"plate\":\"34ABC123\",\"description\":\"Test\",\"date\":\"11.01.2026\",\"location\":\"İstanbul\"}'"
echo ""
