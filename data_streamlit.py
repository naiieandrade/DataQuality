import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.figure_factory as ff
import plotly.express as px


class DataQuality:
    def __init__(self, path: str):
        self.path = path
        self.df = self.read_data()

    def read_data(self):
        
        extension = self.path.name.split('.')[-1]
        if extension == 'csv':
            try:
                data = pd.read_csv(self.path, encoding='utf-8', on_bad_lines='skip')
                return data
            except UnicodeDecodeError:
                data = pd.read_csv(self.path, encoding='latin-1', on_bad_lines='skip')  # Tenta ler com outra codificação
                return data
                
        #elif extension == 'json':
        #    print('json')
        elif extension == 'xlsx':
            data = pd.read_excel(self.path) # Lê o arquivo Excel
            return data
        else:
            print(f"Formato /'{extension}/' não reconhecido.")

    def show_columns(self):

        # Adicionar subtítulo
        st.subheader("Dados gerais do dataset")

        num_variables = len(self.df.columns)
        num_observations = len(self.df)
        missing_values = self.df.isna().sum().sum()
        total_values = self.df.size
        missing_percentage = (missing_values / total_values) * 100

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
        st.write("")
        st.write("")

    
    def show_types_of_columns(self):
        # Adicionar subtítulo
        st.subheader("Tipos de categorias das colunas")
        st.write("")
        
        tipos = {
        'Categórica': [],
        'Numérica': [],
        'Texto': [],
        'Booleana': [],
        'Outros': []
    }
    
        for col in self.df.columns:
            if isinstance(self.df[col].dtype, pd.CategoricalDtype) or (self.df[col].dtype == 'object' and self.df[col].nunique() < 20):
                # Colunas categóricas: identificadas como 'category' ou 'object' com poucos valores únicos
                tipos['Categórica'].append(col)
            elif pd.api.types.is_bool_dtype(self.df[col]):
                # Colunas booleanas: True/False
                tipos['Booleana'].append(col)
            elif pd.api.types.is_numeric_dtype(self.df[col]):
                # Colunas numéricas: inteiros ou floats
                tipos['Numérica'].append(col)
            elif pd.api.types.is_string_dtype(self.df[col]):
                # Colunas de texto: strings (exceto as categorizadas)
                tipos['Texto'].append(col)
            else:
                tipos['Outros'].append(col)

        
        # Dividir em colunas para exibir as métricas em cards na mesma linha
        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.metric("Categórica", len(tipos['Categórica']))

        with col2:
            st.metric("Booleana", len(tipos['Booleana']))

        with col3:
            st.metric("Numérica", len(tipos['Numérica']))

        with col4:
            st.metric("Texto", len(tipos['Texto']))
        
        with col5:
            st.metric("Outros", len(tipos['Outros']))

        st.markdown("---")
        

    def count_nulls(self):

        st.subheader("Quantidade de valores nulos por coluna:")
        st.write("")

        nulos = self.df.isna().sum().sort_values(ascending=False)

        # Checkbox para filtrar colunas que não têm nulos
        filtrar_nulos = st.checkbox("Mostrar apenas colunas sem valores nulos")

        if filtrar_nulos:
            # Filtrar apenas as colunas que não têm nulos
            colunas_sem_nulos = nulos[nulos == 0]
            st.subheader("Colunas sem valores nulos:")
            st.dataframe(colunas_sem_nulos, use_container_width=True)
        else:
            # st.subheader("Quantidade de valores nulos por coluna:")
            st.write("A tabela é interativa, podendo ordenar por coluna.")
            st.dataframe(nulos, use_container_width=True)
        
        st.write("")
        st.write("")


    def count_just_columns_with_nulls(self):
        cols_with_nulls = self.df.isna().sum().sort_values(ascending=False).loc[lambda x: x > 0]
        if len(cols_with_nulls) > 0:
            st.write("Apenas colunas com valores nulos:")
            st.write(cols_with_nulls)
        else:
            st.write("Não tem colunas com valores nulos.")

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

    

    def describe(self):
        st.subheader("Estatísticas descritivas das colunas numéricas")
        st.write("Não mostra colunas vazias.")
        num_columns = self.df.select_dtypes(include=np.number).columns.tolist()

        num_columns_nonzeros = []
        for col in num_columns:
            if int(self.df[col].isna().sum()) != len(self.df):
                num_columns_nonzeros.append(col)
        st.dataframe(self.df[num_columns_nonzeros].describe().map(lambda x: round(x,2)))
        #st.write(self.df.describe())

    def show_lines(self):
        st.subheader("Dados da tabela")
        #st.write("Não mostra colunas vazias.")

        option = st.selectbox(
            "Selecione a opção de ver as linhas iniciais ou finais do dataframe.",
            ("Linhas iniciais", "Linhas finais"),
        )
        
        st.write("Selecionado:", option)
        if option == 'Linhas iniciais':
            st.dataframe(self.df.head(10).apply(lambda x: round(x,2)))
        if option == 'Linhas finais':
            st.dataframe(self.df.tail(10).apply(lambda x: round(x,2)))
    

    def histogram(self):
        st.write("")
        st.subheader("Histograma das colunas numéricas")
        num_columns = self.df.select_dtypes(include=np.number).columns.tolist()        
        
        for col in num_columns:
            if self.df[col].isna().sum() != len(self.df):

                fig = px.histogram(self.df, x=col, nbins=50, title=f"Distribuição da coluna {col}")
                fig.update_layout(yaxis_title="Frequência") 

                st.plotly_chart(fig, use_container_width=True)

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
        tabs = st.tabs(["📈 Geral", "🗃 Colunas"]) 

        with tabs[0]:  # Aba "Geral"
            st.title("Relatório de Qualidade de Dados")
            #st.header("Relatório Geral")
            self.show_columns()
            self.show_types_of_columns()
            self.count_nulls()
            #self.count_just_columns_with_nulls()
            self.describe()
            self.show_lines()
            self.histogram()

        with tabs[1]:  # Aba "Colunas"
            st.header("Informações das Colunas")
            self.show_columns()
            self.show_categories_columns()
            self.show_numerical_columns()
            self.plot_categories()


uploaded_file = st.file_uploader("Envie seu arquivo CSV", type=["csv"])


if uploaded_file is not None:
    dq = DataQuality(uploaded_file)
    dq.profile()
