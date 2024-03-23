import time
import streamlit as st
import pandas as pd
from PIL import Image
from pickle import load
from sklearn.linear_model import LinearRegression

with open('model.dat', "rb") as file:
    model = load(file)

st.set_page_config('Предсказываем возраст краба', layout='wide', initial_sidebar_state='auto')
st.write('<style>.stSpinner > div { justify-content: center; }</style>', unsafe_allow_html=True)
st.write("### Предсказываем возраст краба!")
st.image(Image.open('crab2.jpg'))

st.write('''
Предсказание с помощью модели линейной регрессии, обученной на данных из
[этого](https://www.kaggle.com/competitions/playground-series-s3e16) соревнования.''')

st.sidebar.header('Характеристики краба')

sex = st.sidebar.radio("Пол:", ("Самец", "Самка", "Неизвестно"))
length = st.sidebar.number_input('Длина (см):', min_value=0.01, value=10.0, max_value=100.0)
height = st.sidebar.number_input('Высота (см):', min_value=0.01, value=2.0, max_value=50.0)
weight = st.sidebar.slider('Масса (г):', min_value=1, max_value=400, value=30, step=1)

if st.sidebar.button('Поехали!', type="primary"):
    length_feets = float(length) / 30.48
    height_feets = float(height) / 30.48
    weight_ounces = float(weight) / 29.86

    data = {
        'Length': length_feets,
        'Diameter': length_feets,
        'Height': height_feets,
        'Weight': weight_ounces,
        'Shucked Weight': weight_ounces / 2.3,
        'Viscera Weight': weight_ounces / 4.7,
        'Shell Weight': weight_ounces / 4.0,
        'Female': 1.0 if sex == 'Самка' else 0.0,
        'Intermediate': 1.0 if sex == 'Неизвестно' else 0.0,
        'Male': 1.0 if sex == 'Самец' else 0.0,
    }

    df = pd.DataFrame(data, index=[0])
    age = model.predict(df)

    with st.spinner('Думаем...'):
        time.sleep(3)

    st.info(f'##### Возраст краба {age[0]:.2f} месяцев!')
