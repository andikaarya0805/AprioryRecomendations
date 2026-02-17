import requests
import json

def test_search(keyword):
    print(f"\n--- Testing Search: '{keyword}' ---")
    url = f"http://localhost:8000/recommendations?service={keyword}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            recs = data.get('recommendations', [])
            print(f"Found {len(recs)} recommendations.")
            for i, rec in enumerate(recs[:5]):
                print(f"{i+1}. {rec['item']}")
        else:
            print(f"Error: {response.status_code}")
    except Exception as e:
        print(f"Failed: {e}")

if __name__ == "__main__":
    test_search("wedding")
    test_search("prewedding")
