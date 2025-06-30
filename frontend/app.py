import streamlit as st
import requests
import os

API_URL = os.getenv("API_URL", "http://localhost:8000/products")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="Comparador de Smartphones", layout="wide")
st.title("📱 Comparador de Smartphones")

# Carregar produtos da API
try:
    response = requests.get(API_URL)
    products = response.json()
except Exception as e:
    st.error("Erro ao carregar produtos.")
    st.stop()

# Permitir seleção de até 4 produtos
selected = st.multiselect(
    "Selecione até 4 smartphones para comparar:",
    options=[(p["id"], p["name"]) for p in products],
    format_func=lambda x: x[1],
    max_selections=4
)

selected_ids = [sid for sid, _ in selected]
selected_products = [p for p in products if p["id"] in selected_ids]

# Mostrar comparação lado a lado
if selected_products:
    cols = st.columns(len(selected_products))
    for col, prod in zip(cols, selected_products):
        with col:
            st.image(prod["images"][0], width=200)
            st.markdown(f"### {prod['name']}")
            st.write(f"**Preço:** R$ {prod['price']['current']:.2f}")
            st.write(f"**Armazenamento:** {prod['specifications'].get('storage')}")
            st.write(f"**Câmera:** {prod['specifications'].get('camera')}")
            st.write(f"**Bateria:** {prod['specifications'].get('battery')}")
            st.write(f"**Sistema:** {prod['specifications'].get('os')}")
            st.write(f"**Avaliação:** ⭐ {prod['rating']['average']} ({prod['rating']['count']} avaliações)")

# Botão de IA para recomendação
if len(selected_products) >= 2:
    if st.button("🔍 Qual o melhor custo-benefício? (IA)"):
        with st.spinner("Consultando IA..."):
            try:
                import openai
                openai.api_key = OPENAI_API_KEY

                prompt = "Compare os seguintes smartphones e diga qual oferece o melhor custo-benefício, considerando preço, avaliação, bateria e câmera:"
                for p in selected_products:
                    prompt += f"- {p['name']}: R$ {p['price']['current']:.2f}, {p['rating']['average']} estrelas, câmera {p['specifications']['camera']}, bateria {p['specifications']['battery']}"

                completion = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.5
                )
                answer = completion.choices[0].message.content
                st.success("💡 Sugestão da IA:")
                st.markdown(answer)
            except Exception as e:
                st.error("Erro ao consultar IA. Verifique sua chave e conexão.")