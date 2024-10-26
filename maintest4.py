import streamlit as st
from pycoingecko import CoinGeckoAPI
import plotly.graph_objects as go
import pandas as pd
import pandas_ta as ta

cg = CoinGeckoAPI()
st.set_page_config(page_title="CryptoBen")
st.title('Visualizador de Precios de Criptomonedas')
# Lista de criptomonedas disponibles
crypto_list = ['bitcoin', 'ethereum', 'cardano', 'tether']
# Selección de la criptomoneda por el usuario
selected_crypto = st.selectbox('Selecciona una criptomoneda', crypto_list)
# Seleccion de moneda Fiat por el usuario
fiat_list = ['usd','ars','eur']
selected_fiat = st.selectbox('Selecciona una moneda-pais- ', fiat_list)
# Obtener datos de la API de CoinGecko
crypto_data = cg.get_coin_by_id(id=selected_crypto)
# funcion para actualizar precio
def  resetPrecio():
    coin = crypto_data['market_data']['current_price'][selected_fiat]
    return coin 
price = resetPrecio()
st.button("actualizar",type="primary",on_click=resetPrecio)
# Seleccionar el periodo de tiempo 
days_list = [1,10,30,90,180,365]
selected_day = st.selectbox('Selecciona el periodo de tiempo-dias-', days_list)
# Mostrar el precio actual
st.markdown(f"<h2>El precio actual de {selected_crypto.capitalize()} es: {selected_fiat}$ {price}</h2>", unsafe_allow_html=True)
# Obtener datos históricos de precios
crypto_data_history = cg.get_coin_market_chart_by_id(id=selected_crypto, vs_currency=selected_fiat, days= selected_day)
# Preparar los datos para el gráfico de velas
prices = [item[1] for item in crypto_data_history['prices']]
dates = [item[0] for item in crypto_data_history['prices']]
dates = pd.to_datetime(dates, unit='ms')
# Obtener los datos historicos para conformar la grafica de velas
df = pd.DataFrame({'Date': dates, 'Close': prices})
df['Open'] = df['Close'].shift(1)
df['High'] = df['Close'].rolling(window=2).max()
df['Low'] = df['Close'].rolling(window=2).min()
#calcular indicadores tecnicos
df['RSI'] = ta.rsi(df['Close'], length=14)
# Crear el gráfico de velas
fig = go.Figure(data=[go.Candlestick(x=df['Date'],
                                    open=df['Open'],
                                    high=df['High'],
                                    low=df['Low'],
                                    close=df['Close'])])
# Agregar un slider para seleccionar el rango de precios
min_price = st.slider('Precio mínimo', min_value=df['Low'].min(), max_value=df['High'].max(), value=df['Low'].min())
max_price = st.slider('Precio máximo', min_value=df['Low'].min(), max_value=df['High'].max(), value=df['High'].max())
# Agregar indicadores a la gráfica
fig.add_trace(go.Scatter(x=df['Date'], y=df['RSI'], name='RSI',yaxis='y2',line=dict(color='orange', width=2)))
# Configurar los ejes
fig.update_layout(
    yaxis=dict(title='Precio', autorange=True),  # Ajustar rango automáticamente
    yaxis2=dict(title='Indicadores', overlaying='y', side='right', autorange=True)
)
# Ajustar el rango de precios en el gráfico
fig.update_yaxes(range=[min_price, max_price])
# Personalizar el gráfico
fig.update_layout(title=f"Gráfico de Velas {selected_crypto.capitalize()} (Último/s {selected_day} día/s)",
                  xaxis_title='Periodo',
                  yaxis_title=f'Precio({selected_fiat})')
# Mostrar el gráfico en Streamlit
st.plotly_chart(fig)    
# Informacion para el usuario
st.text('Todo el contenido disponible en nuestro sitio web, en los sitios web hipervinculados,\n y en las aplicaciones, foros, blogs, cuentas de redes sociales y otras plataformas asociados ("Sitio") tienen como único objetivo proporcionarle información general procedente de fuentes externas.\n No ofrecemos garantías de ningún tipo en lo que respecta a nuestro contenido,\n y esto incluye, aunque no se limita únicamente a eso, la exactitud y vigencia de la información.\n Ninguna parte del contenido que ofrecemos debe interpretarse como un asesoramiento financiero,\n jurídico o de cualquier otro tipo en el que pueda basarse de forma específica para la consecución de algún propósito.\n Cualquier utilización o dependencia que haga de nuestro contenido correrá exclusivamente por su cuenta y riesgo.\n Lo que usted debería hacer es llevar a cabo sus propias investigaciones, revisiones y análisis,\n y verificar nuestro contenido antes de basarse en él.\n El comercio es una actividad de alto riesgo que puede resultar en pérdidas importantes,\n por lo que debe consultar con su asesor financiero antes de tomar ninguna decisión.\n Ningún contenido de nuestro Sitio debe considerarse una invitación u oferta para realizar una acción.\n Para mas informacion CoinGeckoApi. CryptoBen2024-v1.1.0')
with st.sidebar:
    st.warning("**Disclaimer:** La información proporcionada en este sitio web es solo para fines informativos y no constituye asesoramiento financiero. Realiza tu propia investigación antes de tomar cualquier decisión de inversión. CriptoBen2024.")
    