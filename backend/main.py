from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
import io
import json

app = FastAPI()

# Enable CORS for Next.js
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for the latest uploaded dataset
# For a real application, this should be a database or file storage.
# In-memory storage
DATASET = None
RULES = []
ITEMS = []
PRODUCTS = {}
RULES_FILE = "rules.json"
ITEMS_FILE = "items.json"
PRODUCTS_FILE = "products.json"

def load_rules():
    global RULES
    try:
        with open(RULES_FILE, 'r') as f:
            RULES = json.load(f)
            print(f"Loaded {len(RULES)} rules from {RULES_FILE}")
    except FileNotFoundError:
        RULES = []
        print("No existing rules found.")
    except Exception as e:
        print(f"Error loading rules: {e}")
        RULES = []

def save_rules(rules):
    try:
        with open(RULES_FILE, 'w') as f:
            json.dump(rules, f)
            print(f"Saved {len(rules)} rules to {RULES_FILE}")
    except Exception as e:
        print(f"Error saving rules: {e}")

def load_items():
    global ITEMS
    try:
        with open(ITEMS_FILE, 'r') as f:
            ITEMS = json.load(f)
            print(f"Loaded {len(ITEMS)} items from {ITEMS_FILE}")
    except FileNotFoundError:
        ITEMS = []
    except Exception as e:
        print(f"Error loading items: {e}")
        ITEMS = []

def save_items(items):
    try:
        with open(ITEMS_FILE, 'w') as f:
            json.dump(items, f)
            print(f"Saved {len(items)} items to {ITEMS_FILE}")
    except Exception as e:
        print(f"Error saving items: {e}")

def load_products():
    global PRODUCTS
    try:
        with open(PRODUCTS_FILE, 'r') as f:
            PRODUCTS = json.load(f)
            print(f"Loaded {len(PRODUCTS)} products from {PRODUCTS_FILE}")
    except FileNotFoundError:
        PRODUCTS = {}
    except Exception as e:
        print(f"Error loading products: {e}")
        PRODUCTS = {}

def save_products(products):
    try:
        with open(PRODUCTS_FILE, 'w') as f:
            json.dump(products, f)
            print(f"Saved {len(products)} products to {PRODUCTS_FILE}")
    except Exception as e:
        print(f"Error saving products: {e}")

# Load rules, items, and products on startup
load_rules()
load_items()
load_products()

class AnalysisRequest(BaseModel):
    min_support: float
    min_confidence: float

@app.get("/")
def read_root():
    return {"message": "Apriori Recommendation API is running"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    global DATASET
    try:
        contents = await file.read()
        if file.filename.endswith('.csv'):
            df = pd.read_csv(io.BytesIO(contents))
        elif file.filename.endswith(('.xls', '.xlsx')):
            # Get all sheet names
            xl = pd.ExcelFile(io.BytesIO(contents))
            sheet_names = xl.sheet_names
            print(f"DEBUG: Sheets found: {sheet_names}")
            
            # Prioritize sheets with "database", "client", "transaksi", or "order"
            target_sheet = sheet_names[0]
            for s in sheet_names:
                if any(k in s.lower() for k in ['database', 'client', 'trans', 'order', 'data']):
                    target_sheet = s
                    break
            
            print(f"DEBUG: Using sheet: {target_sheet}")
            
            # Read first 15 rows to detect the real header
            preview = pd.read_excel(io.BytesIO(contents), sheet_name=target_sheet, header=None, nrows=15)
            
            # Re-defined keywords (more specific to avoid partial matches like 'id' in 'Radit')
            id_keywords = {'id', 'trans', 'client', 'pelanggan', 'user', 'kode', 'nama', 'customer', 'pelanggan'}
            item_keywords = {'item', 'nama', 'product', 'paket', 'event', 'layanan', 'service', 'barang', 'produk'}
            all_keywords = id_keywords.union(item_keywords)

            best_row = 0
            max_score = -1

            for i, row in preview.iterrows():
                # Score this row based on keyword matches
                row_values = [str(val).lower().strip() for val in row.values if pd.notnull(val)]
                if not row_values:
                    continue
                    
                score = 0
                for val in row_values:
                    # Check for exact word matches or common prefixes
                    words = val.replace('/', ' ').replace('_', ' ').split()
                    if any(k in words for k in all_keywords):
                        score += 5 # Strong weight for actual header keywords
                
                # Bonus for row density if it looks like a header (not too many values, usually < 20)
                if 2 < len(row_values) < 20: 
                    score += 1

                if score > max_score:
                    max_score = score
                    best_row = i
            
            print(f"DEBUG: Best header row detected at index {best_row} with score {max_score}")
            
            # Re-read with detected header row and sheet
            df = pd.read_excel(io.BytesIO(contents), sheet_name=target_sheet, skiprows=best_row)
            df = df.dropna(how='all').reset_index(drop=True)
            
            print(f"DEBUG: Resulting columns: {list(df.columns)}")
        else:
            raise HTTPException(status_code=400, detail="Invalid file format")
        
        # Clean up: remove fully empty rows/cols
        df = df.dropna(how='all').dropna(axis=1, how='all')
        DATASET = df
        
        # Basic inspection of the uploaded file
        return {
            "filename": file.filename,
            "columns": list(df.columns),
            "rows": len(df),
            "message": "File uploaded successfully."
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload-catalog")
async def upload_catalog(file: UploadFile = File(...)):
    global PRODUCTS
    try:
        contents = await file.read()
        filename = file.filename.lower()
        new_products = {}
        count = 0

        if filename.endswith(('.xls', '.xlsx')):
            import pandas as pd
            df = pd.read_excel(io.BytesIO(contents))
            # Normalize column names
            df.columns = df.columns.astype(str).str.strip().str.lower()
            
            for _, row in df.iterrows():
                try:
                    category = str(row.get('category', '')).strip()
                    name = str(row.get('name', '')).strip()
                    if not name: name = str(row.get('nama', '')).strip()
                    
                    # Key: "Category Name" or just "Name" if category missing
                    key_parts = []
                    if category: key_parts.append(category)
                    if name: key_parts.append(name)
                    key = " ".join(key_parts).strip()
                    
                    if not key: continue

                    new_products[key] = {
                        "id": str(row.get('id', '')),
                        "name": name,
                        "category": category,
                        "price": str(row.get('price', '')),
                        "description": str(row.get('description', '')),
                        "image": str(row.get('image', ''))
                    }
                    count += 1
                except:
                    continue

        elif filename.endswith('.sql'):
            # Manual SQL Parsing for INSERT INTO statements
            # Pattern: INSERT INTO `packages` (...) VALUES (...);
            # We assume the user's specific format: (id, 'Name', 'Desc', Price, 'Image')
            
            content_str = contents.decode('utf-8')
            import re
            
            # Regex to find the VALUES part. 
            # This captures groups like: (14, 'Signature Plus', 'Desc...', 15000000.00, 'img/...')
            # We handle the fact that VALUES can be followed by multiple (...) separated by commas.
            
            # Simple approach: Finding all matches of (...) that look like our data
            # Look for pattern: (Number, 'String', 'String', Number, 'String')
            # Adjust regex to be flexible but specific enough
            
            # Pattern breakdown:
            # \(          Start group
            # \s*(\d+)    Capture ID (digits)
            # \s*,\s*     Comma
            # '([^']*)'   Capture Name (Single quoted string, no escaped quotes handling needed for simple dump)
            # \s*,\s*     Comma
            # '([^']*)'   Capture Description
            # \s*,\s*     Comma
            # ([\d\.]+)   Capture Price (digits and dot)
            # \s*,\s*     Comma
            # '([^']*)'   Capture Image
            # \s*\)       End group
            
            pattern = re.compile(r"\(\s*(\d+)\s*,\s*'([^']*)'\s*,\s*'([^']*)'\s*,\s*([\d\.]+)\s*,\s*'([^']*)'\s*\)")
            
            matches = pattern.findall(content_str)
            
            for match in matches:
                pid, name, desc, price, image = match
                name = name.strip()
                
                # For SQL data, we don't have explicit category.
                # Key will be the Product Name itself.
                # Recommendation lookup will need fuzzy matching.
                key = name 
                
                new_products[key] = {
                    "id": pid,
                    "name": name,
                    "category": "", # No category in SQL
                    "price": price,
                    "description": desc.replace('\\r\\n', '\n'), # Clean formatting
                    "image": image
                }
                count += 1
                
        else:
            raise HTTPException(status_code=400, detail="Catalog must be .xlsx or .sql file")

        PRODUCTS = new_products
        save_products(PRODUCTS)
        
        return {
            "message": f"Catalog uploaded successfully. Processed {count} items.",
            "sample_keys": list(PRODUCTS.keys())[:5]
        }
        
    except Exception as e:
        # import traceback
        # traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@app.post("/analyze")
def analyze_data(request: AnalysisRequest):
    global DATASET, RULES, PRODUCTS
    if DATASET is None:
        raise HTTPException(status_code=400, detail="No dataset uploaded")
    
    try:
        df = DATASET.copy()
        # Ensure column names are clean
        df.columns = [str(c).strip() for c in df.columns]
        
        # Attempt to find Transaction and Item columns (refined for Indonesian/English)
        id_keywords = ['id', 'trans', 'client', 'pelanggan', 'user', 'no', 'kode', 'nama']
        item_keywords = ['item', 'nama', 'product', 'paket', 'event', 'layanan', 'service']
        
        # Try to find best fit for ID (Transaction)
        id_col = next((c for c in df.columns if any(k in str(c).lower() for k in id_keywords)), df.columns[0])
        
        # Identify all potential item columns (Event, Paket, Service, etc.)
        item_keywords = ['item', 'nama', 'product', 'paket', 'event', 'layanan', 'service', 'barang', 'produk']
        item_cols = [c for c in df.columns if any(k in str(c).lower() for k in item_keywords) and c != id_col]
        
        if not item_cols:
            item_cols = [next((c for c in df.columns if c != id_col), df.columns[0])]

        print(f"DEBUG: Using ID column: {id_col}")
        print(f"DEBUG: Using Item columns: {item_cols}")

        # Preprocessing: 
        # 1. Drop rows where ID is missing
        df = df.dropna(subset=[id_col])
        
        # Check if Long or Wide format
        # Long format: ID appears multiple times (multiple rows per client) -> Merge columns in row to form item
        # Wide format: ID is unique (one row per client) -> Columns are separate items
        is_long_format = df[id_col].duplicated().any()
        
        print(f"DEBUG: Dataset format detected as {'LONG (Multi-row transactions)' if is_long_format else 'WIDE (Single-row transactions)'}")

        # Create a list of normalized product names for fast lookup, sorted by length DESC
        # This ensures we match "Signature Plus" before "Signature"
        known_products_sorted = sorted(
            [k for k in PRODUCTS.keys()], 
            key=lambda x: len(x), 
            reverse=True
        )

        transactions = []
        
        # Helper to extract catalog items from a text string
        def extract_catalog_items(text_soup):
            found = []
            soup_lower = text_soup.lower()
            
            # Iterate through known products (longest first)
            for product in known_products_sorted:
                p_lower = product.lower()
                # Check if product is in the text
                if p_lower in soup_lower:
                    found.append(product)
                    # Remove the found product from soup to prevent double matching
                    # (Simple replace might be risky if duplicated, but works for basic sets)
                    soup_lower = soup_lower.replace(p_lower, '', 1)
            
            return found

        # STOPLIST: Generic words to ignore if they appear alone or as leftovers
        STOPLIST = {'photo', 'video', 'paket', 'package', 'item', 'harga', 'price', 
                    'jasa', 'layanan', 'service', 'product', 'produk', 'kali', 'pcs', 'album'}

        if is_long_format:
            # Group by ID first
            grouped = df.groupby(id_col)
            for _, group in grouped:
                # Gather ALL text from this client's rows into one big soup
                full_text_parts = []
                for _, row in group.iterrows():
                    for col in item_cols:
                        val = str(row[col]).strip()
                        if pd.notnull(row[col]) and val.lower() != 'nan' and val:
                            full_text_parts.append(val)
                
                full_text_soup = " ".join(full_text_parts)
                
                # 1. Try to find Catalog Items first
                identified_items = extract_catalog_items(full_text_soup)
                
                # 2. If no catalog items found, fallback to raw aggregation
                if not identified_items:
                     # Filter out stoplist items from raw text parts
                     raw_items = list(set(full_text_parts))
                     identified_items = [x for x in raw_items if x.lower() not in STOPLIST]

                transactions.append(list(set(identified_items)))
        else:
            # Wide format: One row per transaction
            for _, row in df.iterrows():
                # Gather text from all columns
                row_text_parts = []
                for col in item_cols:
                    val = str(row[col]).strip()
                    if pd.notnull(row[col]) and val.lower() != 'nan' and val:
                        row_text_parts.append(val)
                
                full_row_soup = " ".join(row_text_parts)
                
                # 1. Try to find Catalog Items first
                identified_items = extract_catalog_items(full_row_soup)
                
                # 2. Fallback: Standard splitting if no catalog items found
                if not identified_items:
                    row_items = []
                    for val in row_text_parts:
                        # Split by comma
                        cell_items = [x.strip() for x in val.replace('\n', ',').replace(';', ',').split(',') if x.strip()]
                        # Filter out stoplist items
                        valid_items = [x for x in cell_items if x.lower() not in STOPLIST]
                        row_items.extend(valid_items)
                    identified_items = row_items
                
                transactions.append(list(set(identified_items)))
        
        # Collect all unique items for the frontend dropdown
        unique_items = sorted(list(set([item for sublist in transactions for item in sublist])))
        global ITEMS
        ITEMS = unique_items
        save_items(ITEMS)

        # Filter out transactions with only 1 item (Apriori needs at least 2)
        transactions = [t for t in transactions if len(t) > 1]
        
        if not transactions:
            RULES = []
            return {
                "message": "Pola tidak ditemukan. Pastikan satu Client memiliki minimal 2 item/transaksi yang berbeda agar bisa dianalisis.",
                "rules": []
            }
        
        # One-Hot Encoding
        from mlxtend.preprocessing import TransactionEncoder
        te = TransactionEncoder()
        te_ary = te.fit(transactions).transform(transactions)
        one_hot_df = pd.DataFrame(te_ary, columns=te.columns_)

        # Apriori
        frequent_itemsets = apriori(one_hot_df, min_support=request.min_support, use_colnames=True)
        
        if frequent_itemsets.empty:
            RULES = []
            return {"message": "No frequent itemsets found with this support level", "rules": []}

        # Association Rules
        res_rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=request.min_confidence)
        
        # Convert to JSON friendly format
        processed_rules = []
        for _, row in res_rules.iterrows():
            processed_rules.append({
                "antecedents": list(row['antecedents']),
                "consequents": list(row['consequents']),
                "support": float(row['support']),
                "confidence": float(row['confidence']),
                "lift": float(row['lift'])
            })
        
        RULES = processed_rules
        save_rules(RULES)
        return {
            "message": f"Analysis complete. Found {len(RULES)} rules and {len(ITEMS)} unique items.",
            "rules": RULES,
            "items": ITEMS
        }

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/recommendations")
def get_recommendations(service: str):
    global RULES, PRODUCTS
    if not RULES:
        return {
            "service": service,
            "recommendations": [],
            "message": "No rules available. Run analysis first."
        }
    
    # Filter rules where the query is in the antecedents
    recommendations = []
    query_lower = service.lower().strip()
    
    # Helper to look up product details
    # We try to find the best matching product key for a given item string.
    # e.g. Item: "Wedding Platinum", Product Key: "Platinum" -> Match!
    def get_product_details(item_name):
        item_lower = item_name.lower()
        
        # 1. Exact Key Match
        for k, v in PRODUCTS.items():
            if k.lower() == item_lower:
                return v
        
        # 2. Check if Product Name is contained in Item Name
        # e.g. Product "Platinum" is inside Item "Wedding Platinum"
        # We pick the longest matching product name to be safe (e.g. match "Signature Plus" over "Signature")
        best_match = None
        longest_len = 0
        
        for k, v in PRODUCTS.items():
            k_lower = k.lower()
            if k_lower in item_lower:
                if len(k_lower) > longest_len:
                    longest_len = len(k_lower)
                    best_match = v
        
        if best_match:
            return best_match
            
        return None

    # Get details for the *queried* service itself
    query_details = get_product_details(service)

    for rule in RULES:
        # Check if any part of the query matches any antecedent
        if any(query_lower in str(ant).lower() for ant in rule['antecedents']):
            for cons in rule['consequents']:
                # Avoid duplicates and check if already in list
                # Also filter out items that are purely numeric (usually IDs or prices)
                if not any(r['item'] == str(cons) for r in recommendations):
                    item_str = str(cons).strip()
                    if not item_str.isdigit() and len(item_str) > 2:
                        # Fetch Product Details
                        details = get_product_details(item_str)
                        
                        rec_obj = {
                            "item": item_str,
                            "confidence": f"{int(rule['confidence'] * 100)}%",
                            "details": details # Can be None
                        }
                        recommendations.append(rec_obj)
    
    # Sort by confidence
    recommendations = sorted(recommendations, key=lambda x: int(x['confidence'].replace('%', '')), reverse=True)

    return {
        "service": service,
        "service_details": query_details,
        "recommendations": recommendations[:5] # Return top 5
    }

@app.get("/items")
def get_items():
    global ITEMS
    return {"items": ITEMS}

@app.get("/status")
def get_status():
    global DATASET, RULES
    return {
        "dataset_loaded": DATASET is not None,
        "rows": len(DATASET) if DATASET is not None else 0,
        "rules_count": len(RULES)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
