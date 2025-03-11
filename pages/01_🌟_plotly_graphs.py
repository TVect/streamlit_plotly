import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit_pydantic as sp
from pydantic import BaseModel, Field

st.set_page_config(page_title="Plotly Graphs",
                   page_icon=":bar_chart:", layout="wide")

st.title("Plotly Graphs")
st.markdown(
    ":small[:gray[[Plotly](!https://plotly.com/python/) "
    "is an open-source graphing library that enables you "
    "to create interactive, publication-quality graphs.]]"
)


class PieChartsConfig(BaseModel):
    values: str = Field(alias="values field", description="values field")
    names: str = Field(alias="names field", description="names field")


class ScatterPlotsConfig(BaseModel):
    x: str = Field(alias="x field", description="x field")
    y: str = Field(alias="y field", description="y field")
    color: str = Field(alias="color field", description="color field")
    size: str = Field(alias="size field", description="size field")


df_data = None
# df = px.data.tips()
plot_config = {"option": "Pie Charts", "params": {}}

col1, col2 = st.columns([0.7, 0.3], gap="medium", border=True)

with col2:
    uploaded_file = st.file_uploader(
        "Choose a file", 
        label_visibility="collapsed")    # visible | hidden | collapsed
    option = st.selectbox(
        "Choose a chart type ...",
        ("Pie Charts", "Scatter Plots", "..."),
    )

    plot_config["option"] = option
    if option == "Pie Charts":
        data = sp.pydantic_form(key="my_sample_form", model=PieChartsConfig)
        if data:
            plot_config["params"] = data
    elif option == "Scatter Plots":
        data = sp.pydantic_form(key="my_sample_form", model=ScatterPlotsConfig)
        if data:
            plot_config["params"] = data
    else:
        st.write("...")


with col1:
    if uploaded_file is not None:
        # Can be used wherever a "file-like" object is accepted:
        df_data = pd.read_csv(uploaded_file)

    if df_data is not None:
        st.dataframe(df_data, height=640)

if df_data is not None and plot_config["params"]:
    params = {
        key: value for key, value in plot_config["params"].dict().items() if value != ""
    }
    with st.container(border=False):
        if plot_config["option"] == "Pie Charts":
            fig = px.pie(
                df_data,
                #  color_discrete_sequence=px.colors.sequential.RdBu,
                **plot_config["params"].dict()
            )
        elif plot_config["option"] == "Scatter Plots":
            fig = px.scatter(df_data, **params)
        st.plotly_chart(fig)
