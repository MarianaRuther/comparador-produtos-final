from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from pathlib import Path
import json
import openai

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

# IA: Análise de custo-benefício
class CompareRequest(BaseModel):
    products: List[str]

@app.post("/compare")
async def compare_products(request: CompareRequest):
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            all_products = json.load(f)

        selected = [p for p in all_products if p["name"] in request.products]

        if len(selected) < 2:
            raise HTTPException(status_code=400, detail="Selecione ao menos dois produtos para comparar.")

        prompt = f"""Você é um especialista em tecnologia de consumo. Compare os seguintes smartphones com base no custo-benefício, considerando preço, armazenamento, câmera, bateria, sistema e avaliação. No final, diga qual é o melhor custo-benefício e por quê.\n\n"""

        for p in selected:
            prompt += f"- {p['name']}: preço R$ {p['price']['current']}, armazenamento {p['specifications']['storage']}, câmera {p['specifications']['camera']}, bateria {p['specifications']['battery']}, sistema {p['specifications']['os']}, avaliação {p['rating']['average']} de {p['rating']['count']} avaliações.\n"

        prompt += "\nSeja direto e claro na recomendação."

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            temperature=0.7,
            messages=[
                {"role": "system", "content": "Você é um especialista em tecnologia e custo-benefício de smartphones."},
                {"role": "user", "content": prompt}
            ]
        )

        result = response.choices[0].message.content.strip()
        return {"resultado": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
