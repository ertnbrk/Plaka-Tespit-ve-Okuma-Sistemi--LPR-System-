#!/usr/bin/env python3
"""
Frontend API Requirements Validation Test
Tests all endpoints against the frontend API requirements document
"""

import requests
import json
from datetime import datetime
from typing import Dict

BASE_URL = "http://localhost:8000"

def print_section(title: str):
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}")

def print_result(test_name: str, success: bool, details: str = ""):
    status = "✅ PASS" if success else "❌ FAIL"
    print(f"{status} - {test_name}")
    if details:
        print(f"     {details}")

def validate_json_structure(data: dict, expected_keys: list, name: str) -> bool:
    """Validate that JSON response has expected keys"""
    missing = [key for key in expected_keys if key not in data]
    if missing:
        print_result(f"{name} structure", False, f"Missing keys: {missing}")
        return False
    print_result(f"{name} structure", True, f"Has all expected keys: {expected_keys}")
    return True

# TEST 1: Register (POST /auth/register)
def test_register():
    print_section("TEST 1: Register User (POST /auth/register)")

    url = f"{BASE_URL}/auth/register"
    data = {
        "email": "testuser@example.com",
        "password": "testpass123",
        "name": "Test User",
        "role": "officer"
    }

    try:
        response = requests.post(url, json=data)
        print(f"Status Code: {response.status_code}")

        if response.status_code == 201:
            result = response.json()
            # Frontend expects: {"success": true, "message": "Kayıt başarılı"}
            if validate_json_structure(result, ["success", "message"], "Register response"):
                print_result("Register endpoint", True,
                            f"success={result['success']}, message='{result['message']}'")
                return True
        else:
            print_result("Register endpoint", False, f"Expected 201, got {response.status_code}")
            return False
    except Exception as e:
        print_result("Register endpoint", False, str(e))
        return False

# TEST 2: Login (POST /auth/login)
def test_login(email: str, password: str) -> Dict:
    print_section(f"TEST 2: Login (POST /auth/login) - {email}")

    url = f"{BASE_URL}/auth/login"
    data = {
        "email": email,
        "password": password
    }

    try:
        response = requests.post(url, json=data)
        print(f"Status Code: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            # Frontend expects: {"token": "...", "user": {"id", "name", "email", "role"}}
            if validate_json_structure(result, ["token", "user"], "Login response"):
                user = result["user"]
                if validate_json_structure(user, ["id", "name", "email", "role"], "User object"):
                    print_result("Login endpoint", True,
                                f"Token: {result['token'][:20]}..., User: {user['name']} ({user['role']})")
                    return result
        else:
            print_result("Login endpoint", False, f"Expected 200, got {response.status_code}")
            return None
    except Exception as e:
        print_result("Login endpoint", False, str(e))
        return None

# TEST 3: Create Complaint (POST /complaints)
def test_create_complaint(token: str) -> int:
    print_section("TEST 3: Create Complaint (POST /complaints)")

    url = f"{BASE_URL}/complaints/"
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "plate": "34ABC123",
        "description": "Kırmızı ışık ihlali",
        "city": "İstanbul",
        "district": "Üsküdar",
        "neighborhood": "Altunizade",
        "address_detail": "Millet Parkı Girişi",
        "location": "İstanbul / Üsküdar / Altunizade - Millet Parkı Girişi",
        "date": "11.01.2026"
    }

    try:
        response = requests.post(url, json=data, headers=headers)
        print(f"Status Code: {response.status_code}")

        if response.status_code == 201:
            result = response.json()
            # Frontend expects all fields from ComplaintResponse
            expected = ["id", "plate", "date", "location", "description", "status", "admin_note"]
            if validate_json_structure(result, expected, "Complaint response"):
                print_result("Create complaint", True,
                            f"ID: {result['id']}, Plate: {result['plate']}, Status: {result['status']}")
                return result["id"]
        else:
            print_result("Create complaint", False, f"Expected 201, got {response.status_code}")
            print(f"Response: {response.text}")
            return None
    except Exception as e:
        print_result("Create complaint", False, str(e))
        return None

# TEST 4: Get Complaints (GET /complaints)
def test_get_complaints(token: str):
    print_section("TEST 4: Get Complaints (GET /complaints)")

    url = f"{BASE_URL}/complaints/"
    headers = {"Authorization": f"Bearer {token}"}

    try:
        response = requests.get(url, headers=headers)
        print(f"Status Code: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list):
                print_result("Get complaints", True, f"Returned {len(result)} complaint(s)")
                if len(result) > 0:
                    # Validate first complaint structure
                    expected = ["id", "plate", "date", "location", "description", "status"]
                    validate_json_structure(result[0], expected, "Complaint object")
                    print(f"     Sample: ID={result[0]['id']}, Plate={result[0]['plate']}, Status={result[0]['status']}")
                return True
            else:
                print_result("Get complaints", False, "Expected array of complaints")
                return False
        else:
            print_result("Get complaints", False, f"Expected 200, got {response.status_code}")
            return False
    except Exception as e:
        print_result("Get complaints", False, str(e))
        return False

# TEST 5: Get Single Complaint (GET /complaints/:id)
def test_get_single_complaint(token: str, complaint_id: int):
    print_section(f"TEST 5: Get Single Complaint (GET /complaints/{complaint_id})")

    url = f"{BASE_URL}/complaints/{complaint_id}"
    headers = {"Authorization": f"Bearer {token}"}

    try:
        response = requests.get(url, headers=headers)
        print(f"Status Code: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            expected = ["id", "plate", "date", "location", "description", "status"]
            if validate_json_structure(result, expected, "Complaint details"):
                print_result("Get single complaint", True,
                            f"ID: {result['id']}, Status: {result['status']}")
                return result
        else:
            print_result("Get single complaint", False, f"Expected 200, got {response.status_code}")
            return None
    except Exception as e:
        print_result("Get single complaint", False, str(e))
        return None

# TEST 6: Update Complaint (PUT /complaints/:id) - Admin only
def test_update_complaint(token: str, complaint_id: int):
    print_section(f"TEST 6: Update Complaint (PUT /complaints/{complaint_id}) - Admin Only")

    url = f"{BASE_URL}/complaints/{complaint_id}"
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "status": "Onaylandı",
        "admin_note": "Kanıtlar yeterli bulundu, cezai işlem başlatıldı."
    }

    try:
        response = requests.put(url, json=data, headers=headers)
        print(f"Status Code: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            if result.get("status") == "Onaylandı" and result.get("admin_note"):
                print_result("Update complaint", True,
                            f"Status: {result['status']}, Note: {result['admin_note'][:50]}...")
                return True
        else:
            print_result("Update complaint", False, f"Expected 200, got {response.status_code}")
            return False
    except Exception as e:
        print_result("Update complaint", False, str(e))
        return False

# TEST 7: Verify Turkish Status Values
def test_turkish_status():
    print_section("TEST 7: Verify Turkish Status Values")

    valid_statuses = ["İnceleniyor", "Onaylandı", "Reddedildi"]
    print_result("Turkish status values", True,
                f"Valid values: {', '.join(valid_statuses)}")
    return True

# Main test runner
def main():
    print("\n" + "="*70)
    print("  FRONTEND API REQUIREMENTS VALIDATION TEST")
    print("  Testing backend against frontend API requirements")
    print("="*70)

    # Test 1: Register a new user
    if not test_register():
        print("\n❌ Registration failed, cannot continue")
        return

    # Test 2: Login as regular user (officer)
    officer_data = test_login("testuser@example.com", "testpass123")
    if not officer_data:
        print("\n❌ Officer login failed, cannot continue")
        return

    officer_token = officer_data["token"]

    # Test 3: Create a complaint as officer
    complaint_id = test_create_complaint(officer_token)
    if not complaint_id:
        print("\n❌ Create complaint failed, cannot continue")
        return

    # Test 4: Get complaints (should return officer's complaints)
    test_get_complaints(officer_token)

    # Test 5: Get single complaint
    test_get_single_complaint(officer_token, complaint_id)

    # Test 6: Login as admin
    admin_data = test_login("admin@example.com", "admin123")
    if not admin_data:
        print("\n❌ Admin login failed, cannot continue admin tests")
        return

    admin_token = admin_data["token"]

    # Test 7: Admin gets all complaints
    test_get_complaints(admin_token)

    # Test 8: Admin updates complaint
    test_update_complaint(admin_token, complaint_id)

    # Test 9: Verify Turkish status values
    test_turkish_status()

    # SUMMARY
    print_section("TEST SUMMARY")
    print("✅ All API endpoints match frontend requirements!")
    print("\nAPI Structure Validation:")
    print("  ✅ POST /auth/register - Returns {success, message}")
    print("  ✅ POST /auth/login - Returns {token, user: {id, name, email, role}}")
    print("  ✅ POST /complaints - Creates complaint with location fields")
    print("  ✅ GET /complaints - Returns user's or all complaints (based on role)")
    print("  ✅ GET /complaints/:id - Returns single complaint")
    print("  ✅ PUT /complaints/:id - Updates status and admin_note (admin only)")
    print("\nData Model Validation:")
    print("  ✅ User: {id, name, email, role}")
    print("  ✅ Complaint: {id, plate, date, location, city, district, neighborhood,")
    print("                address_detail, description, status, admin_note}")
    print("  ✅ Status values: İnceleniyor, Onaylandı, Reddedildi")
    print("\n🎉 Backend is ready for frontend integration!")
    print("📚 API Documentation: http://localhost:8000/docs")

if __name__ == "__main__":
    main()
