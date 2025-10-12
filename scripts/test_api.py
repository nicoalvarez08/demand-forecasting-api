#!/usr/bin/env python3
"""
Script para probar los endpoints de la API
"""

import requests
import json


BASE_URL = "http://localhost:8000"


def test_health():
    """Test health endpoint"""
    print("\n1. Testing Health Check...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


def test_stats():
    """Test stats endpoint"""
    print("\n2. Testing Statistics...")
    response = requests.get(f"{BASE_URL}/api/v1/stats")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


def test_model_info():
    """Test model info endpoint"""
    print("\n3. Testing Model Info...")
    response = requests.get(f"{BASE_URL}/api/v1/model/info")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


def test_prediction():
    """Test prediction endpoint"""
    print("\n4. Testing Single Prediction...")
    
    payload = {
        "product_id": 101,
        "month": 12,
        "day_of_week": 5,
        "price": 29.99,
        "promotion": 1,
        "stock": 150
    }
    
    response = requests.post(f"{BASE_URL}/api/v1/predict", json=payload)
    print(f"Status: {response.status_code}")
    print(f"Request: {json.dumps(payload, indent=2)}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


def test_batch_prediction():
    """Test batch prediction endpoint"""
    print("\n5. Testing Batch Prediction...")
    
    payload = [
        {
            "product_id": 101,
            "month": 12,
            "day_of_week": 5,
            "price": 29.99,
            "promotion": 1,
            "stock": 150
        },
        {
            "product_id": 105,
            "month": 6,
            "day_of_week": 2,
            "price": 49.99,
            "promotion": 0,
            "stock": 80
        }
    ]
    
    response = requests.post(f"{BASE_URL}/api/v1/predict/batch", json=payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


def main():
    print("=" * 60)
    print("Testing Demand Forecasting API")
    print("=" * 60)
    print("\nAsegúrate de que la API esté corriendo en http://localhost:8000")
    
    try:
        test_health()
        test_stats()
        test_model_info()
        test_prediction()
        test_batch_prediction()
        
        print("\n" + "=" * 60)
        print("✓ Todos los tests completados!")
        print("=" * 60)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: No se pudo conectar a la API")
        print("Asegúrate de iniciar la API con: python -m uvicorn app.main:app --reload")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")


if __name__ == "__main__":
    main()

