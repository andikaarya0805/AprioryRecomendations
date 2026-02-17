import json

# Test script to verify keyword search logic
print("=" * 60)
print("TESTING KEYWORD SEARCH LOGIC")
print("=" * 60)

# Load products
with open('products.json', 'r') as f:
    PRODUCTS = json.load(f)

# Test case 1: Search "wedding"
print("\n1. Testing search: 'wedding'")
query = "wedding"
matches = []
for key, data in PRODUCTS.items():
    name = key.lower()
    desc = str(data.get('description', '')).lower()
    if query in name or query in desc:
        matches.append(key)
        print(f"   ✓ Matched: {key}")

print(f"\n   Total matches: {len(matches)}")

# Test case 2: Search "pengajian"
print("\n2. Testing search: 'pengajian'")
query = "pengajian"
matches = []
for key, data in PRODUCTS.items():
    name = key.lower()
    desc = str(data.get('description', '')).lower()
    if query in name or query in desc:
        matches.append(key)
        print(f"   ✓ Matched: {key}")

print(f"\n   Total matches: {len(matches)}")

# Test case 3: Search "prewedding"
print("\n3. Testing search: 'prewedding'")
query = "prewedding"
matches = []
for key, data in PRODUCTS.items():
    name = key.lower()
    desc = str(data.get('description', '')).lower()
    if query in name or query in desc:
        matches.append(key)
        print(f"   ✓ Matched: {key}")

print(f"\n   Total matches: {len(matches)}")

print("\n" + "=" * 60)
print("All packages in catalog:")
print("=" * 60)
for i, key in enumerate(PRODUCTS.keys(), 1):
    print(f"{i}. {key}")
