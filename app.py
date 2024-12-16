import streamlit as st
import pandas as pd
import numpy as np
from joblib import load

# Kaydedilmiş modeli yükleme
model_path = "eniyi.joblib"  # Modelin doğru konumda olduğundan emin olun
model = load(model_path)

# Başlık
st.title("Gözlük Camı Fiyat Tahmini")
st.write("Bu uygulama, verilen bilgilere göre tahmini gözlük camı fiyatını hesaplar.")

# Kullanıcı girişi
st.header("Girdi Bilgileri")
cam_turu = st.selectbox("Cam Türü", ["İnce Kenar", "Mavi Işık Filtreli", "Fotokromik"])
uv_koruma = st.slider("UV Koruma (%)", 50, 100, step=25)
cam_numarasi = st.number_input("Cam Numarası", min_value=-6.00, max_value=6.00, step=0.25, format="%.2f")
kaplama_turu = st.selectbox("Kaplama Türü", ["Antirefle", "Sert Kaplama", "Standart"])
marka = st.selectbox("Marka", ["Marka A", "Marka B", "Marka C", "Marka D"])

# Tahmin düğmesi
if st.button("Tahmini Fiyatı Göster"):
    # Kullanıcı girdilerini bir DataFrame'e dönüştür
    input_data = pd.DataFrame({
        "Cam Türü": [cam_turu],
        "UV Koruma (%)": [uv_koruma],
        "Cam Numarası": [cam_numarasi],
        "Kaplama Türü": [kaplama_turu],
        "Marka": [marka]
    })

    # Modeli kullanarak tahmini yap
    prediction = model.predict(input_data)[0]
    st.success(f"Tahmini Fiyat: {prediction:.2f} TL")
