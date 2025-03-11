import streamlit as st
import pandas as pd
from io import StringIO
import plotly.figure_factory as ff
import plotly.express as px
import streamlit_pydantic as sp
from pydantic import BaseModel


class PieChartConfig(BaseModel):
    values_field: str
    name_field: str


tab1, tab2 = st.tabs(["上传数据", "图表配置"])

with tab1:
    st.header("上传图表")
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        # To read file as bytes:
        bytes_data = uploaded_file.getvalue()
        st.write(bytes_data)

        # To convert to a string based IO:
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        st.write(stringio)

        # To read file as string:
        string_data = stringio.read()
        st.write(string_data)

        # Can be used wherever a "file-like" object is accepted:
        dataframe = pd.read_csv(uploaded_file)
        st.write(dataframe)

    df = px.data.tips()
    st.write(df)

with tab2:
    st.header("图表配置")

    option = st.selectbox(
        "Choose a chart type ...",
        ("Pie Charts", "Scatter", "..."),
    )

    if option == "Pie Charts":
        data = sp.pydantic_form(key="my_sample_form", model=PieChartConfig)
        if data:
            st.json(data.model_dump())
    elif option == "Scatter":
        st.write("Scatter")
    else:
        st.write("...")

fig = px.pie(df, values='tip', names='day',
             color_discrete_sequence=px.colors.sequential.RdBu)
st.plotly_chart(fig)
