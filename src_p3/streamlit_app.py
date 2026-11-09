import streamlit as st
import requests

st.title("Predicción de Precios de Vivienda en California")

# URL de tu API en Render (FastAPI)
URL_API = "https://daw-practica-3.onrender.com/predict"

# 1. Definir valores por defecto razonables para las 8 variables requeridas
DEFAULTS = {
    "MedInc": 3.5,
    "HouseAge": 25.0,
    "AveRooms": 5.0,
    "AveBedrms": 1.0,
    "Population": 1400.0,
    "AveOccup": 3.0,
    "Latitude": 37.88,
    "Longitude": -122.23
}

# Ejercicio d / b: Formulario para introducir variables clave
st.subheader("Datos de la Vivienda")
med_inc = st.number_input("Ingreso Medio de la zona (MedInc en 10k$)", value=DEFAULTS["MedInc"])
ave_rooms = st.number_input("Número medio de habitaciones (AveRooms)", value=DEFAULTS["AveRooms"])

# Construimos el diccionario de datos
datos_envio = {
    "MedInc": med_inc,
    "HouseAge": DEFAULTS["HouseAge"],
    "AveRooms": ave_rooms,
    "AveBedrms": DEFAULTS["AveBedrms"],
    "Population": DEFAULTS["Population"],
    "AveOccup": DEFAULTS["AveOccup"],
    "Latitude": DEFAULTS["Latitude"],
    "Longitude": DEFAULTS["Longitude"]
}

if st.button("Calcular Predicción"):
    # EJERCICIO B: Validar que contiene las 8 variables antes de enviar
    variables_requeridas = ['MedInc', 'HouseAge', 'AveRooms', 'AveBedrms', 'Population', 'AveOccup', 'Latitude', 'Longitude']
    faltantes = [var for var in variables_requeridas if var not in datos_envio or datos_envio[var] is None]
    
    if faltantes:
        st.error(f" Error: Faltan los siguientes campos obligatorios: {', '.join(faltantes)}")
    else:
        try:
            # Petición POST a la API
            response = requests.post(URL_API, json=datos_envio)
            
            if response.status_code == 200:
                resultado = response.json()
                
                # Obtener el valor bruto que devuelve la API (ej: 2.857)
                # (Ajusta la clave 'prediction' si tu FastAPI usa otro nombre de propiedad)
                #  CÓDIGO CORREGIDO: Extraemos el valor de la clave 'MedHouseVal'
                if isinstance(resultado, dict):
                    valor_bruto = resultado.get("MedHouseVal", list(resultado.values())[0])
                else:
                    valor_bruto = resultado
                st.info(f"Valor bruto devuelto por la API: {valor_bruto}")
                
                # EJERCICIO C: Transformación a dólares reales (* 100,000) y formateo
                precio_final = float(valor_bruto) * 100000
                st.success(f"Precio estimado formateado: **${precio_final:,.2f}**")
            else:
                st.error(f"Error en el servidor de la API (Código HTTP {response.status_code})")
                
        except Exception as e:
            st.error(f"Error de conexión con la API: {e}")
