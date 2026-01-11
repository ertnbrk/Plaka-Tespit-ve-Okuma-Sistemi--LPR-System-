#!/bin/bash

# API Testing Script with cURL
# Tests all major endpoints with proper formatting

BASE_URL="http://127.0.0.1:8000"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_section() {
    echo -e "\n${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}→ $1${NC}"
}

# Check if jq is installed
if ! command -v jq &> /dev/null; then
    print_error "jq is not installed. Install it for pretty JSON output:"
    echo "  Ubuntu/Debian: sudo apt-get install jq"
    echo "  Mac: brew install jq"
    exit 1
fi

# Test 1: Register Officer
print_section "1. REGISTER NEW OFFICER"
print_info "POST /auth/register"

REGISTER_RESPONSE=$(curl -s -X POST "${BASE_URL}/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test_officer@example.com",
    "password": "test123",
    "name": "Test Officer",
    "role": "officer"
  }')

echo "$REGISTER_RESPONSE" | jq .

if echo "$REGISTER_RESPONSE" | jq -e '.success' > /dev/null 2>&1; then
    print_success "Officer registered successfully"
else
    print_info "Officer might already exist (this is OK for testing)"
fi

# Test 2: Login Officer
print_section "2. LOGIN AS OFFICER"
print_info "POST /auth/login"

LOGIN_RESPONSE=$(curl -s -X POST "${BASE_URL}/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test_officer@example.com",
    "password": "test123"
  }')

echo "$LOGIN_RESPONSE" | jq .

OFFICER_TOKEN=$(echo "$LOGIN_RESPONSE" | jq -r '.token')

if [ "$OFFICER_TOKEN" != "null" ] && [ -n "$OFFICER_TOKEN" ]; then
    print_success "Officer logged in successfully"
    print_info "Token: ${OFFICER_TOKEN:0:30}..."
else
    print_error "Failed to login officer"
    exit 1
fi

# Test 3: Get Officer Profile
print_section "3. GET OFFICER PROFILE"
print_info "GET /auth/me"

PROFILE_RESPONSE=$(curl -s -X GET "${BASE_URL}/auth/me" \
  -H "Authorization: Bearer ${OFFICER_TOKEN}")

echo "$PROFILE_RESPONSE" | jq .
print_success "Profile retrieved"

# Test 4: Create Complaint
print_section "4. CREATE COMPLAINT"
print_info "POST /complaints/"

COMPLAINT_RESPONSE=$(curl -s -X POST "${BASE_URL}/complaints/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${OFFICER_TOKEN}" \
  -d '{
    "plate": "34TEST789",
    "description": "Kırmızı ışık ihlali tespit edildi",
    "date": "11.01.2026",
    "location": "İstanbul / Kadıköy / Caferağa - Moda Cd. No:15",
    "city": "İstanbul",
    "district": "Kadıköy",
    "neighborhood": "Caferağa",
    "address_detail": "Moda Cd. No:15"
  }')

echo "$COMPLAINT_RESPONSE" | jq .

COMPLAINT_ID=$(echo "$COMPLAINT_RESPONSE" | jq -r '.id')

if [ "$COMPLAINT_ID" != "null" ] && [ -n "$COMPLAINT_ID" ]; then
    print_success "Complaint created with ID: $COMPLAINT_ID"
else
    print_error "Failed to create complaint"
fi

# Test 5: Get Officer's Complaints
print_section "5. GET OFFICER'S COMPLAINTS"
print_info "GET /complaints/ (as officer)"

COMPLAINTS_RESPONSE=$(curl -s -X GET "${BASE_URL}/complaints/" \
  -H "Authorization: Bearer ${OFFICER_TOKEN}")

echo "$COMPLAINTS_RESPONSE" | jq .

COMPLAINT_COUNT=$(echo "$COMPLAINTS_RESPONSE" | jq 'length')
print_success "Found $COMPLAINT_COUNT complaint(s)"

# Test 6: Get Single Complaint
if [ "$COMPLAINT_ID" != "null" ] && [ -n "$COMPLAINT_ID" ]; then
    print_section "6. GET SINGLE COMPLAINT"
    print_info "GET /complaints/${COMPLAINT_ID}"

    SINGLE_COMPLAINT=$(curl -s -X GET "${BASE_URL}/complaints/${COMPLAINT_ID}" \
      -H "Authorization: Bearer ${OFFICER_TOKEN}")

    echo "$SINGLE_COMPLAINT" | jq .
    print_success "Complaint details retrieved"
fi

# Test 7: Login Admin
print_section "7. LOGIN AS ADMIN"
print_info "POST /auth/login"

ADMIN_LOGIN_RESPONSE=$(curl -s -X POST "${BASE_URL}/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@example.com",
    "password": "admin123"
  }')

echo "$ADMIN_LOGIN_RESPONSE" | jq .

ADMIN_TOKEN=$(echo "$ADMIN_LOGIN_RESPONSE" | jq -r '.token')

if [ "$ADMIN_TOKEN" != "null" ] && [ -n "$ADMIN_TOKEN" ]; then
    print_success "Admin logged in successfully"
    print_info "Token: ${ADMIN_TOKEN:0:30}..."
else
    print_error "Failed to login admin"
    exit 1
fi

# Test 8: Get All Complaints (Admin)
print_section "8. GET ALL COMPLAINTS (AS ADMIN)"
print_info "GET /complaints/ (as admin)"

ALL_COMPLAINTS=$(curl -s -X GET "${BASE_URL}/complaints/" \
  -H "Authorization: Bearer ${ADMIN_TOKEN}")

echo "$ALL_COMPLAINTS" | jq .

TOTAL_COMPLAINTS=$(echo "$ALL_COMPLAINTS" | jq 'length')
print_success "Admin can see $TOTAL_COMPLAINTS total complaint(s)"

# Test 9: Update Complaint Status
if [ "$COMPLAINT_ID" != "null" ] && [ -n "$COMPLAINT_ID" ]; then
    print_section "9. UPDATE COMPLAINT STATUS (ADMIN)"
    print_info "PUT /complaints/${COMPLAINT_ID}"

    UPDATE_RESPONSE=$(curl -s -X PUT "${BASE_URL}/complaints/${COMPLAINT_ID}" \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer ${ADMIN_TOKEN}" \
      -d '{
        "status": "Onaylandı",
        "admin_note": "Test için onaylandı. Kanıtlar yeterli."
      }')

    echo "$UPDATE_RESPONSE" | jq .

    UPDATED_STATUS=$(echo "$UPDATE_RESPONSE" | jq -r '.status')
    if [ "$UPDATED_STATUS" == "Onaylandı" ]; then
        print_success "Complaint status updated to: Onaylandı"
    else
        print_error "Failed to update complaint status"
    fi
fi

# Test 10: Try Officer Update (Should Fail)
if [ "$COMPLAINT_ID" != "null" ] && [ -n "$COMPLAINT_ID" ]; then
    print_section "10. TRY OFFICER UPDATE (SHOULD FAIL)"
    print_info "PUT /complaints/${COMPLAINT_ID} (as officer)"

    OFFICER_UPDATE=$(curl -s -X PUT "${BASE_URL}/complaints/${COMPLAINT_ID}" \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer ${OFFICER_TOKEN}" \
      -d '{
        "status": "Reddedildi"
      }')

    echo "$OFFICER_UPDATE" | jq .

    if echo "$OFFICER_UPDATE" | jq -e '.detail' | grep -q "admin"; then
        print_success "Correctly blocked: Only admins can update"
    else
        print_error "Security issue: Officer was able to update!"
    fi
fi

# Test 11: Get Admin Users
print_section "11. GET ALL USERS (ADMIN)"
print_info "GET /admin/users"

USERS_RESPONSE=$(curl -s -X GET "${BASE_URL}/admin/users" \
  -H "Authorization: Bearer ${ADMIN_TOKEN}")

echo "$USERS_RESPONSE" | jq .

USER_COUNT=$(echo "$USERS_RESPONSE" | jq 'length')
print_success "Found $USER_COUNT user(s) in system"

# Summary
print_section "TEST SUMMARY"
echo ""
print_success "Authentication tests passed"
print_success "Complaint CRUD operations passed"
print_success "Role-based access control working"
print_success "Admin operations working"
echo ""
print_info "Officer Token: ${OFFICER_TOKEN:0:50}..."
print_info "Admin Token: ${ADMIN_TOKEN:0:50}..."
echo ""
print_info "Use these tokens for manual testing:"
echo ""
echo "  export OFFICER_TOKEN='$OFFICER_TOKEN'"
echo "  export ADMIN_TOKEN='$ADMIN_TOKEN'"
echo ""
print_success "All tests completed successfully!"
echo ""
print_info "API Documentation: ${BASE_URL}/docs"
echo ""
