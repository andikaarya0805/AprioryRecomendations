import requests
import json

BASE_URL = "http://localhost:8000"

print("=" * 60)
print("UPLOADING AND ANALYZING TRANSACTION DATA")
print("=" * 60)

# Step 1: Upload catalog (if needed)
print("\n1. Uploading catalog (packages.sql)...")
try:
    with open("packages.sql", "rb") as f:
        response = requests.post(f"{BASE_URL}/upload-catalog", files={"file": f})
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
except Exception as e:
    print(f"   Error: {e}")

# Step 2: Upload transaction data
print("\n2. Uploading transaction data (Schedule Ranah Creative.xlsx - Database Client (1).xlsx)...")
try:
    with open("Schedule Ranah Creative.xlsx - Database Client (1).xlsx", "rb") as f:
        response = requests.post(f"{BASE_URL}/upload", files={"file": f})
    print(f"   Status: {response.status_code}")
    result = response.json()
    print(f"   Filename: {result.get('filename')}")
    print(f"   Columns: {result.get('columns')}")
    print(f"   Rows: {result.get('rows')}")
except Exception as e:
    print(f"   Error: {e}")

# Step 3: Run analysis
print("\n3. Running Apriori analysis...")
try:
    payload = {
        "min_support": 0.08,  # Lower threshold for more rules
        "min_confidence": 0.3
    }
    response = requests.post(f"{BASE_URL}/analyze", json=payload)
    print(f"   Status: {response.status_code}")
    result = response.json()
    print(f"   Message: {result.get('message')}")
    print(f"   Rules found: {len(result.get('rules', []))}")
    print(f"   Items found: {len(result.get('items', []))}")
    
    # Show first 5 rules
    if result.get('rules'):
        print("\n   Sample rules:")
        for i, rule in enumerate(result['rules'][:5], 1):
            print(f"   {i}. {rule['antecedents']} → {rule['consequents']} (confidence: {rule['confidence']:.2%})")
            
except Exception as e:
    print(f"   Error: {e}")

# Step 4: Test recommendations
print("\n4. Testing recommendations...")
test_queries = ["wedding", "prewedding", "pengajian", "engagement", "akad"]

for query in test_queries:
    try:
        response = requests.get(f"{BASE_URL}/recommendations?service={query}")
        result = response.json()
        recs = result.get('recommendations', [])
        print(f"\n   Query: '{query}' → {len(recs)} recommendations")
        for rec in recs[:3]:
            print(f"      - {rec['item']} ({rec['confidence']})")
    except Exception as e:
        print(f"   Error for '{query}': {e}")

print("\n" + "=" * 60)
print("ANALYSIS COMPLETE!")
print("=" * 60)
