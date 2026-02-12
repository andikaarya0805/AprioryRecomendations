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

@app.post("/analyze")
def analyze_data(request: AnalysisRequest):
    global DATASET, RULES
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
        
        # 2. Extract items from ALL item columns and split them
        def get_all_items(group):
            all_items = []
            for col in item_cols:
                # Get non-null values from this column for this transaction
                vals = group[col].dropna().astype(str).str.lower().str.strip().tolist()
                for v in vals:
                    # Split multi-item strings like "Photo Video" or "Engagement, Wedding"
                    parts = [p.strip() for p in v.replace(',', ' ').split() if p.strip()]
                    all_items.extend(parts)
            return list(set(all_items)) # Unique items in this transaction (Client)

        transactions = df.groupby(id_col).apply(get_all_items).values.tolist()
        
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
        return {
            "message": f"Analysis complete. Found {len(RULES)} rules.",
            "rules": RULES
        }

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/recommendations")
def get_recommendations(service: str):
    global RULES
    if not RULES:
        return {
            "service": service,
            "recommendations": [],
            "message": "No rules available. Run analysis first."
        }
    
    # Filter rules where the query is in the antecedents
    recommendations = []
    query_lower = service.lower().strip()
    
    for rule in RULES:
        # Check if any part of the query matches any antecedent
        if any(query_lower in str(ant).lower() for ant in rule['antecedents']):
            for cons in rule['consequents']:
                # Avoid duplicates and check if already in list
                # Also filter out items that are purely numeric (usually IDs or prices)
                if not any(r['item'] == str(cons) for r in recommendations):
                    item_str = str(cons).strip()
                    if not item_str.isdigit() and len(item_str) > 2:
                        recommendations.append({
                            "item": item_str,
                            "confidence": f"{int(rule['confidence'] * 100)}%"
                        })
    
    # Sort by confidence
    recommendations = sorted(recommendations, key=lambda x: int(x['confidence'].replace('%', '')), reverse=True)

    return {
        "service": service,
        "recommendations": recommendations[:5] # Return top 5
    }

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
