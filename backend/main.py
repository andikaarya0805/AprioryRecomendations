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
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for the latest uploaded dataset
# For a real application, this should be a database or file storage.
DATASET = None

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
            df = pd.read_excel(io.BytesIO(contents))
        else:
            raise HTTPException(status_code=400, detail="Invalid file format")
        
        DATASET = df
        
        # Basic inspection of the uploaded file
        return {
            "filename": file.filename,
            "columns": list(df.columns),
            "rows": len(df),
            "message": "File uploaded successfully."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze")
def analyze_data(request: AnalysisRequest):
    global DATASET
    if DATASET is None:
        return {
            "message": "No dataset found. Using Mock Data for testing.",
            "rules": _get_mock_rules()
        }
    
    try:
        # Preprocessing: Convert transaction list to One-Hot Encoded DataFrame
        # Assumption: Dataset has 'TransactionID' and 'Item' columns or similar structure
        # If dataset is already one-hot encoded (0/1 per item), use as is.
        # This part requires adjusting based on the actual data format.
        
        # For now, let's try to detect format or just fallback to mock if logic fails
        # Attempt to pivot if 'Item' and 'Transaction' columns exist
        df = DATASET.copy()
        cols = [c.lower() for c in df.columns]
        
        # Simplified logic: If we can't easily parse, return mock advice + error
        # In a real scenario, we would validate schema strictness.
        
        # Placeholder for actual mlxtend logic:
        # frequent_items = apriori(one_hot_df, min_support=request.min_support, use_colnames=True)
        # rules = association_rules(frequent_items, metric="confidence", min_threshold=request.min_confidence)
        # return rules.to_dict(orient="records")
        
        return {
            "message": "Apriori analysis simulation (Real logic waiting for data format confirmation)",
            "rules": _get_mock_rules()
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def _get_mock_rules():
    return [
        {
            "antecedents": ["Wedding Package"],
            "consequents": ["Prewedding Photo"],
            "support": 0.2,
            "confidence": 0.85,
            "lift": 2.1
        },
        {
            "antecedents": ["Catering Buffet"],
            "consequents": ["Desert Corner"],
            "support": 0.15,
            "confidence": 0.70,
            "lift": 1.5
        },
        {
            "antecedents": ["Sewa Gedung"],
            "consequents": ["Dekorasi Pelaminan"],
            "support": 0.3,
            "confidence": 0.9,
            "lift": 3.0
        }
    ]

@app.get("/recommendations")
def get_recommendations(service: str):
    # This endpoint would filter the generated rules for the specific service
    # For prototype, returns dummy recommendation
    return {
        "service": service,
        "recommendations": [
            {"item": "Recommendation A", "confidence": "80%"},
            {"item": "Recommendation B", "confidence": "75%"}
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
