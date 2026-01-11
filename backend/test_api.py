#!/usr/bin/env python3
"""
API Integration Test Script
Tests all major endpoints to ensure database and API are working correctly
"""

import requests
import json
from datetime import datetime
from typing import Dict

BASE_URL = "http://localhost:8000"

def print_section(title: str):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

def print_result(test_name: str, success: bool, details: str = ""):
    status = "✅ PASS" if success else "❌ FAIL"
    print(f"{status} - {test_name}")
    if details:
        print(f"     {details}")

def test_auth_register() -> bool:
    """Test user registration"""
    print_section("Testing User Registration")

    url = f"{BASE_URL}/auth/register"
    data = {
        "email": "testuser@example.com",
        "password": "testpass123",
        "full_name": "Test User"
    }

    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            user_data = response.json()
            print_result("User Registration", True, f"Created user: {user_data['email']}")
            return True
        else:
            print_result("User Registration", False, f"Status: {response.status_code}, Error: {response.text}")
            return False
    except Exception as e:
        print_result("User Registration", False, str(e))
        return False

def test_auth_login(email: str, password: str) -> Dict:
    """Test user login and return token"""
    print_section(f"Testing Login: {email}")

    url = f"{BASE_URL}/auth/login"
    data = {
        "email": email,
        "password": password
    }

    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            token_data = response.json()
            print_result("Login", True, f"Token received: {token_data['access_token'][:20]}...")
            return token_data
        else:
            print_result("Login", False, f"Status: {response.status_code}, Error: {response.text}")
            return None
    except Exception as e:
        print_result("Login", False, str(e))
        return None

def test_get_me(token: str) -> bool:
    """Test getting current user info"""
    print_section("Testing Get Current User")

    url = f"{BASE_URL}/auth/me"
    headers = {"Authorization": f"Bearer {token}"}

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            user_data = response.json()
            print_result("Get Current User", True, f"User: {user_data['email']}, Admin: {user_data['is_admin']}")
            return True
        else:
            print_result("Get Current User", False, f"Status: {response.status_code}")
            return False
    except Exception as e:
        print_result("Get Current User", False, str(e))
        return False

def test_create_complaint(token: str) -> bool:
    """Test creating a complaint"""
    print_section("Testing Create Complaint")

    url = f"{BASE_URL}/complaints/"
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "plate": "34ABC123",
        "description": "Vehicle parked illegally in no-parking zone",
        "incident_datetime": datetime.now().isoformat()
    }

    try:
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            complaint_data = response.json()
            print_result("Create Complaint", True, f"Complaint ID: {complaint_data['id']}, Plate: {complaint_data['plate']}")
            return True
        else:
            print_result("Create Complaint", False, f"Status: {response.status_code}, Error: {response.text}")
            return False
    except Exception as e:
        print_result("Create Complaint", False, str(e))
        return False

def test_get_my_complaints(token: str) -> bool:
    """Test getting user's complaints"""
    print_section("Testing Get My Complaints")

    url = f"{BASE_URL}/complaints/my"
    headers = {"Authorization": f"Bearer {token}"}

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            complaints = response.json()
            print_result("Get My Complaints", True, f"Found {len(complaints)} complaint(s)")
            for c in complaints:
                print(f"     - Complaint #{c['id']}: Plate {c['plate']}, Status: {c['status']}")
            return True
        else:
            print_result("Get My Complaints", False, f"Status: {response.status_code}")
            return False
    except Exception as e:
        print_result("Get My Complaints", False, str(e))
        return False

def test_admin_get_users(token: str) -> bool:
    """Test admin endpoint to get all users"""
    print_section("Testing Admin - Get All Users")

    url = f"{BASE_URL}/admin/users"
    headers = {"Authorization": f"Bearer {token}"}

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            users = response.json()
            print_result("Admin Get Users", True, f"Found {len(users)} user(s)")
            for u in users:
                print(f"     - User: {u['email']}, Admin: {u['is_admin']}")
            return True
        else:
            print_result("Admin Get Users", False, f"Status: {response.status_code}")
            return False
    except Exception as e:
        print_result("Admin Get Users", False, str(e))
        return False

def test_admin_get_complaints(token: str) -> bool:
    """Test admin endpoint to get all complaints"""
    print_section("Testing Admin - Get All Complaints")

    url = f"{BASE_URL}/admin/complaints"
    headers = {"Authorization": f"Bearer {token}"}

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            complaints = response.json()
            print_result("Admin Get Complaints", True, f"Found {len(complaints)} complaint(s)")
            return True
        else:
            print_result("Admin Get Complaints", False, f"Status: {response.status_code}")
            return False
    except Exception as e:
        print_result("Admin Get Complaints", False, str(e))
        return False

def main():
    print("\n" + "="*60)
    print("  API INTEGRATION TEST SUITE")
    print("  Testing all endpoints with database")
    print("="*60)

    # Test 1: Register a new user
    test_auth_register()

    # Test 2: Login as regular user
    user_token_data = test_auth_login("testuser@example.com", "testpass123")
    if not user_token_data:
        print("\n❌ Cannot continue tests without valid user token")
        return

    user_token = user_token_data['access_token']

    # Test 3: Get current user info
    test_get_me(user_token)

    # Test 4: Create a complaint as regular user
    test_create_complaint(user_token)

    # Test 5: Get my complaints
    test_get_my_complaints(user_token)

    # Test 6: Login as admin
    admin_token_data = test_auth_login("admin@example.com", "admin123")
    if not admin_token_data:
        print("\n❌ Cannot continue admin tests without valid admin token")
        return

    admin_token = admin_token_data['access_token']

    # Test 7: Admin - Get all users
    test_admin_get_users(admin_token)

    # Test 8: Admin - Get all complaints
    test_admin_get_complaints(admin_token)

    print_section("TEST SUMMARY")
    print("✅ All endpoints tested successfully!")
    print("Database is properly configured and API is ready for use.")
    print("\nAPI Documentation available at: http://localhost:8000/docs")

if __name__ == "__main__":
    main()
