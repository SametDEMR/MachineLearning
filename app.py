import streamlit as st
import pandas as pd
import numpy as np
from joblib import load
import json

# Kaydedilmiş modeli ve metrikleri yükleme
model_path = "eniyi.joblib"
metrics_path = "model_metrics.json"

# Modeli yükle
try:
    model = load(model_path)
except FileNotFoundError:
    st.error("Model dosyası bulunamadı. Lütfen doğru konumda olduğundan emin olun.")
    st.stop()

# Metrikleri yükle
try:
    with open(metrics_path, "r") as f:
        metrics = json.load(f)
except FileNotFoundError:
    st.warning("Model doğruluk bilgileri bulunamadı.")
    metrics = None

# Başlık
st.title("Gözlük Camı Fiyat Tahmini")
st.write("Bu uygulama, verilen bilgilere göre tahmini gözlük camı fiyatını hesaplar.")

# Model doğruluk bilgileri
if metrics:
    st.header("Model Doğruluğu")
    st.write(f"**Eğitim Hatası (RMSE):** {metrics['rmse_train']:.2f}")
    st.write(f"**Test Hatası (RMSE):** {metrics['rmse_test']:.2f}")

# Kullanıcı girişi
st.header("Girdi Bilgileri")
cam_turu = st.selectbox("Cam Türü", ["İnce Kenar", "Mavi Işık Filtreli", "Fotokromik"], help="Gözlük camının türünü seçin.")
uv_koruma = st.slider("UV Koruma (%)", 50, 100, step=25, help="UV koruma seviyesini seçin.")
cam_numarasi = st.number_input("Cam Numarası", min_value=-6.00, max_value=6.00, step=0.25, format="%.2f", help="Cam numarasını girin.")
kaplama_turu = st.selectbox("Kaplama Türü", ["Antirefle", "Sert Kaplama", "Standart"], help="Kaplama türünü seçin.")
marka = st.selectbox("Marka", ["Marka A", "Marka B", "Marka C", "Marka D"], help="Gözlük markasını seçin.")

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

    # Modele uygun sütunların olup olmadığını kontrol et
    expected_columns = ["Cam Türü", "UV Koruma (%)", "Cam Numarası", "Kaplama Türü", "Marka"]
    if not all(col in input_data.columns for col in expected_columns):
        st.error("Girdiler modele uygun değil. Lütfen tüm gerekli bilgileri sağlayın.")
        st.stop()

    # Modeli kullanarak tahmini yap
    try:
        prediction = model.predict(input_data)[0]
        st.success(f"Tahmini Fiyat: {prediction:.2f} TL")
    except Exception as e:
        st.error(f"Tahmin sırasında bir hata oluştu: {str(e)}")
