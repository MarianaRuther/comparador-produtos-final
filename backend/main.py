from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json
from pathlib import Path
from pydantic import BaseModel
from typing import List
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_PATH = Path(__file__).resolve().parent / "products.json"

class Product(BaseModel):
    id: str
    name: str
    brand: str
    category: str
    price: dict
    images: List[str]
    specifications: dict
    rating: dict
    availability: dict
    features: List[str]
    created_at: str
    updated_at: str

@app.get("/products", response_model=List[Product])
def get_products():
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))