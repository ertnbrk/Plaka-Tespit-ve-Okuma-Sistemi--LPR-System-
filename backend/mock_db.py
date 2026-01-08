import random
from datetime import datetime, timedelta

# Mock Database simulating a Gov/Insurance System
VEHICLE_DATABASE = {
    # Test Plate 1
    "34NH9258": {
        "plate": "34 NH 9258",
        "isLocal": True,
        "vehicle": {
            "brand": "Renault",
            "model": "Clio 1.5 dCi",
            "year": 2018,
            "fuelType": "Dizel",
            "color": "Beyaz"
        },
        "mileage": {
            "value": 142500,
            "lastUpdated": "2025-12-10"
        },
        "damageStatus": {
            "hasDamage": True,
            "damageCount": 3,
            "records": [
                {
                    "date": "2020-05-14",
                    "type": "Çarpma",
                    "location": "Arka Tampon",
                    "severity": "Hafif",
                    "cost": "1.500 TL"
                },
                {
                    "date": "2022-11-02",
                    "type": "ERP-Çarpışma",
                    "location": "Sol Ön Çamurluk",
                    "severity": "Orta",
                    "cost": "12.400 TL"
                },
                {
                    "date": "2024-01-20",
                    "type": "Park Halinde Çarpılma",
                    "location": "Sağ Ayna",
                    "severity": "Hafif",
                    "cost": "3.200 TL"
                }
            ]
        }
    },
    # Test Plate 2 (Clean Record)
    "34ABC123": {
        "plate": "34 ABC 123",
        "isLocal": True,
        "vehicle": {
            "brand": "Toyota",
            "model": "Corolla 1.8 Hybrid",
            "year": 2021,
            "fuelType": "Hibrit",
            "color": "Gri"
        },
        "mileage": {
            "value": 45000,
            "lastUpdated": "2025-11-15"
        },
        "damageStatus": {
            "hasDamage": False,
            "damageCount": 0,
            "records": []
        }
    },
     # Test Plate 3 (Diplomatic)
    "99CD999": {
        "plate": "99 CD 999",
        "isLocal": True,
        "vehicle": {
            "brand": "Mercedes-Benz",
            "model": "S-Class S400",
            "year": 2023,
            "fuelType": "Benzin",
            "color": "Siyah"
        },
        "mileage": {
            "value": 12000,
            "lastUpdated": "2025-10-01"
        },
        "damageStatus": {
            "hasDamage": False,
            "damageCount": 0,
            "records": []
        }
    }
}

def get_vehicle_info(plate_text):
    """
    Look up vehicle info by plate.
    Normalizes input (removes spaces) to find key.
    If not found, generates semi-random data for demo purposes if it looks like a valid plate.
    """
    normalized = plate_text.replace(" ", "").upper()
    
    # 1. Check exact match in mock DB
    if normalized in VEHICLE_DATABASE:
        return VEHICLE_DATABASE[normalized]
    
    # 2. If not found but looks valid, generate random realistic data (for demo effect)
    # This prevents "Not Found" disappointment during demo
    import re
    if re.match(r'^\d{2}[A-Z]+\d+$', normalized):
        return generate_random_vehicle(plate_text)
        
    return None

def generate_random_vehicle(plate):
    """Generate consistent random data based on plate string hash"""
    seed = sum(ord(c) for c in plate)
    random.seed(seed)
    
    brands = ["Fiat", "Ford", "Volkswagen", "Hyundai", "Honda"]
    models = {
        "Fiat": ["Egea", "Doblo"],
        "Ford": ["Focus", "Fiesta"],
        "Volkswagen": ["Passat", "Golf"],
        "Hyundai": ["i20", "Tucson"],
        "Honda": ["Civic", "City"]
    }
    
    brand = random.choice(brands)
    model = random.choice(models[brand])
    year = random.randint(2015, 2024)
    km = random.randint(10000, 200000)
    
    has_damage = random.choice([True, False])
    records = []
    
    if has_damage:
        count = random.randint(1, 4)
        for _ in range(count):
            records.append({
                "date": (datetime.now() - timedelta(days=random.randint(100, 1000))).strftime("%Y-%m-%d"),
                "type": random.choice(["Çarpma", "Sürtme", "Dolu Hasarı", "Park Halinde"]),
                "location": random.choice(["Tampon", "Kapı", "Tavan", "Far"]),
                "severity": random.choice(["Hafif", "Orta", "Ağır"]),
                "cost": f"{random.randint(1000, 50000)} TL"
            })
            
    return {
        "plate": plate,
        "isLocal": True,
        "vehicle": {
            "brand": brand,
            "model": model,
            "year": year,
            "fuelType": random.choice(["Benzin", "Dizel", "LPG", "Elektrik"]),
            "color": random.choice(["Beyaz", "Siyah", "Gri", "Kırmızı", "Mavi"])
        },
        "mileage": {
            "value": km,
            "lastUpdated": "2025-12-01"
        },
        "damageStatus": {
            "hasDamage": has_damage,
            "damageCount": len(records),
            "records": sorted(records, key=lambda x: x['date'], reverse=True)
        }
    }
