# 📌 Instruções de Execução

## 1. Clone ou extraia o projeto

```bash
unzip comparador_produtos.zip
cd comparador_produtos
pip install -r requirements.txt
```

## 2. Executar o Backend (FastAPI)

```bash
cd backend
uvicorn main:app --reload
```

A API estará disponível em: http://localhost:8000/products

## 3. Executar o Frontend (Streamlit)

Em outro terminal:

```bash
cd frontend
streamlit run app.py
```

Acesse: http://localhost:8501

✅ Pronto! Compare smartphones e peça uma sugestão inteligente da IA.