import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from bson import ObjectId

app = FastAPI(title="Swedish Candy Boxes API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models (import schemas for validation)
from schemas import CandyBox, Order
from database import db, create_document, get_documents


@app.get("/")
def read_root():
    return {"message": "Swedish Candy Boxes Backend Running"}


@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    return response


# ---------- Candy Boxes Endpoints ----------
@app.post("/api/boxes", response_model=dict)
def create_box(box: CandyBox):
    try:
        box_id = create_document("candybox", box)
        return {"id": box_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/boxes", response_model=List[dict])
def list_boxes(tag: Optional[str] = None):
    try:
        filter_q = {"tags": {"$in": [tag]}} if tag else {}
        docs = get_documents("candybox", filter_q)
        # Convert ObjectId to string
        for d in docs:
            if isinstance(d.get("_id"), ObjectId):
                d["id"] = str(d.pop("_id"))
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ---------- Orders Endpoints ----------
@app.post("/api/orders", response_model=dict)
def create_order(order: Order):
    try:
        order_id = create_document("order", order)
        return {"id": order_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
