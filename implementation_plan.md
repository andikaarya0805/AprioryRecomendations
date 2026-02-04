# Implementation Plan - Apriori Recommendation System

## Goal Description
Build a web-based prototype for an Admin-only Apriori Recommendation System.
**Frontend:** Next.js (Visuals, Interaction)
**Backend:** Python FastAPI (Data Processing, Apriori Algorithm)

## User Review Required
> [!NOTE]
> This is a prototype system. User authentication for Admin will be simulated for simplicity unless a full database auth is requested.

## Proposed Changes

### Backend (`/backend`)
#### [NEW] [main.py](file:///d:/dika/tugas/Apriori_Recommendations/backend/main.py)
- Setup FastAPI app.
- Create `/upload` endpoint to accept CSV/Excel files.
- Create `/analyze` endpoint to run Apriori algorithm.
- Create `/recommendations` endpoint to fetch results.

#### [NEW] [requirements.txt](file:///d:/dika/tugas/Apriori_Recommendations/backend/requirements.txt)
- `fastapi`
- `uvicorn`
- `pandas`
- `mlxtend`
- `python-multipart`

### Frontend (`/frontend`)
#### [NEW] [Next.js App Structure]
- `src/app/page.tsx`: Dashboard / Landing.
- `src/app/upload/page.tsx`: File upload interface.
- `src/app/analysis/page.tsx`: Input constraints (Support/Confidence) and view rules.
- `src/components/Sidebar.tsx`: Navigation for Admin.

## Verification Plan

### Automated Tests
- **Backend**: Run `pytest` (to be added) or manual API testing via Swagger UI (`http://localhost:8000/docs`).
- **Frontend**: Build check `npm run build`.

### Manual Verification
1.  **Start Backend**: `uvicorn main:app --reload`
2.  **Start Frontend**: `npm run dev`
3.  **Upload Data**: Upload a sample transaction CSV.
4.  **Run Analysis**: Set Min Support 0.1, Min Confidence 0.5. Check if rules are generated.
5.  **Check Recommendations**: Select a product and verify if recommendations appear.
