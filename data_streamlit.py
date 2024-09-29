import streamlit as st
import pandas as pd

class DataQuality:
    def __init__(self, path: str):
        self.path = path
        self.df = self.read_data()

    def read_data(self):
        return pd.read_csv(self.path)

    def generate_summary(self):
        # Calcular as informações desejadas
        num_variables = len(self.df.columns)
        num_observations = len(self.df)
        missing_cells = self.df.isna().sum().sum()
        total_cells = self.df.size
        missing_percentage = (missing_cells / total_cells) * 100
        
        # Dividir em colunas para exibir as métricas em cards na mesma linha
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Number of Variables", num_variables)

        with col2:
            st.metric("Number of Observations", num_observations)

        with col3:
            st.metric("Missing Cells", missing_cells)

        with col4:
            st.metric("Missing Cells (%)", f"{missing_percentage:.2f}%")




import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class DataQuality:
    def __init__(self, path: str):
        self.path = path
        self.df = self.read_data()

    def read_data(self):
        extension = self.path.split('.')[-1]
        if extension == 'csv':
            try:
                data = pd.read_csv(self.path, encoding='utf-8', on_bad_lines='skip')
                return data
            except UnicodeDecodeError:
                data = pd.read_csv(self.path, encoding='latin-1', on_bad_lines='skip')  # Tenta ler com outra codificação
                return data
                
        elif extension == 'json':
            print('json')
        elif extension == 'xlsx':
            data = pd.read_excel(self.path) # Lê o arquivo Excel
            return data
        else:
            print(f"Formato /'{extension}/' não reconhecido.")

    def show_columns(self):

        # total_values = self.df.shape[0]*self.df.shape[1]

        num_variables = len(self.df.columns)
        num_observations = len(self.df)
        missing_values = self.df.isna().sum().sum()
        total_values = self.df.size
        missing_percentage = (missing_values / total_values) * 100
        
        # Exibir os dados no formato solicitado
        # st.write("### Dados de Qualidade")
        # st.metric("Number of Variables", num_variables)
        # st.metric("Number of Observations", num_observations)
        # st.metric("Missing Cells", missing_cells)
        # st.metric("Missing Cells (%)", f"{missing_percentage:.2f}%")
        
        # st.write(f"Colunas do dataframe {self.path}\n")
        # st.write(f"Quantidade de colunas: {len(self.df.columns)}")
        # data = pd.DataFrame({"Quantidade de colunas:": self.df.shape[1],
        #                      "Linhas totais:": self.df.shape[0],
        #                      "Campos vazios:": missing_values,
        #                      "% Campos vazios:": "{:.2f}%".format(missing_values/total_values*100),
        #                      "Linhas duplicadas:": self.df.duplicated().sum()
        #                    }, index=[0]) #self.df.isna().sum().sum()/self.df.shape[0]*self.df.shape[1]*100
        # #{:.2f}%".format(missing_percentage)
        # data = data.T
        # data.columns = [''] 
        # st.table(data)

        # Dividir em colunas para exibir as métricas em cards na mesma linha
        col1, col2, col3 = st.columns(3)
        col4, col5, col6 = st.columns(3)

        with col1:
            st.metric("Quantidade de colunas", self.df.shape[1])

        with col2:
            st.metric("Linhas totais", self.df.shape[0])

        with col3:
            st.metric("Campos vazios", missing_values)

        with col4:
            st.metric("Campos vazios (%)", f"{missing_values/total_values*100:.2f}%")

        with col5:
            st.metric("Linhas duplicadas", self.df.duplicated().sum())

        with col6:
            st.metric("Linhas duplicadas", f"{self.df.duplicated().sum()/len(self.df)*100:.2f}%")


    def show_categories_columns(self):
        cat_columns = self.df.select_dtypes(exclude=np.number).columns.tolist()
        if len(cat_columns) > 0:
            st.write("Colunas categóricas:")
            st.write(cat_columns)
        else:
            st.write("Esse dataset não tem colunas categóricas")

    def show_numerical_columns(self):
        num_columns = self.df.select_dtypes(include=np.number).columns.tolist()
        if len(num_columns) > 0:
            st.write("Colunas numéricas:")
            st.write(num_columns)
        else:
            st.write("Esse dataset não tem colunas numéricas")

    def count_nulls(self):
        st.write("Quantidade de valores nulos por coluna:")
        st.write(self.df.isna().sum())

    def count_just_columns_with_nulls(self):
        cols_with_nulls = self.df.isna().sum().sort_values(ascending=False).loc[lambda x: x > 0]
        if len(cols_with_nulls) > 0:
            st.write("Apenas colunas com valores nulos:")
            st.write(cols_with_nulls)
        else:
            st.write("Não tem colunas com valores nulos.")

    def describe(self):
        st.write("Estatísticas descritivas das colunas numéricas:")
        st.write(self.df.describe())

    def histogram(self):
        num_columns = self.df.select_dtypes(include=np.number).columns.tolist()
        st.write("Histograma das colunas numéricas:")
        for col in num_columns:
            if self.df[col].isna().sum() != len(self.df):
                fig, ax = plt.subplots()
                self.df[col].hist(bins=50, ax=ax)
                ax.set_title(f"Histograma da coluna '{col}'")
                ax.set_xlabel(col)
                ax.set_ylabel('Frequência')
                st.pyplot(fig)

    def plot_categories(self):
        cat_columns = self.df.select_dtypes(exclude=np.number).columns.tolist()
        for col in cat_columns:
            if len(self.df[col].value_counts()) < 20:
                fig, ax = plt.subplots()
                self.df[col].value_counts().plot(kind='barh', ax=ax)
                ax.set_title(f"Distribuição por categorias '{col}'")
                ax.set_xlabel('Quantidade')
                ax.set_ylabel(col)
                st.pyplot(fig)

    def profile(self):
        # Abas no Streamlit
        tabs = st.tabs(["📈 Geral", "🗃 Colunas"]) 

        with tabs[0]:  # Aba "Geral"
            st.header("Relatório Geral")
            self.show_columns()
            self.count_nulls()
            self.count_just_columns_with_nulls()
            self.describe()
            self.histogram()

        with tabs[1]:  # Aba "Colunas"
            st.header("Informações das Colunas")
            self.show_columns()
            self.show_categories_columns()
            self.show_numerical_columns()
            self.plot_categories()

# Código para rodar a aplicação Streamlit

# Carregar o arquivo
#uploaded_file = st.file_uploader("Envie seu arquivo CSV ou JSON", type=["csv", "json", "xlsx"])

#if uploaded_file is not None:
dq = DataQuality("input/gula.csv")
dq.profile()
