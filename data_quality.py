import pandas as pd

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
        n = 1
        
        print(f"\nColunas do dataframe {self.path}\n")
        print(f"Quantidade de colunas: {len(self.df.columns)}\n")
        for _ in list(self.df.columns):
            print(f"{n}: {_}")
            n += 1

        print('\n')
    
    def show_categories_columns(self):
        cat_columns = self.df.select_dtypes(exclude=np.number).columns.tolist()
        n = 1
        if len(cat_columns)>0:
            print("Colunas categóricas: ")
            for col in cat_columns:
                print(f"{n}: {col}")
                n += 1
        else:
            print("Esse dataset não tem colunas categóricas")
        print('\n')

    def show_numerical_columns(self):
        num_columns = self.df.select_dtypes(include=np.number).columns.tolist()
        n = 1
        if len(num_columns)>0:
            print("Colunas numéricas: ")
            for col in num_columns:
                print(f"{n}: {col}")
                n += 1
        else:
            print("Esse dataset não tem colunas numéricas")
        print('\n')

    def count_nulls(self):
        print("Quantidade de valores nulos por coluna:")
        print(self.df.isna().sum())
        print('\n')

    def count_just_columns_with_nulls(self):
        if self.df.isna().sum().sort_values(ascending=False).loc[lambda x: x > 0].size > 0:
            print("Apenas colunas com valores nulos:")
            print(self.df.isna().sum().sort_values(ascending=False).loc[lambda x: x > 0])
        else:
            print("Não tem colunas com valores nulos.")
        print('\n')

    def unique_values(self):
        cat_columns = self.df.select_dtypes(exclude=np.number).columns.tolist()
        n = 1
        if len(cat_columns)>0:
            print("Quantidade de valores únicos por coluna categórica:")
            for col in cat_columns:
                pct_unique_values = self.df[col].unique().size/self.df.size
                print(f"{n}: {col} possui {self.df[col].unique().size} valores únicos.")
                if (pct_unique_values) > 0.9:
                    print("Provavelmente é uma coluna de ID ou texto.")
                n += 1
        print("\n")

    def value_counts(self):
        cat_columns = self.df.select_dtypes(exclude=np.number).columns.tolist()
        n = 1
        if len(cat_columns)>0:
            print("Quantidade de valores únicos por coluna categórica:")
            for col in cat_columns:
                pct_unique_values = self.df[col].unique().size/len(self.df)
                print(f"{n}: {col} possui {self.df[col].value_counts().size} valores únicos.")
                print("Top 5 valores distintos com maior frequência: ")
                print(self.df[col].value_counts()[:5])
                # print(len(d1.df))
                n += 1
                print("\n")
        print("\n")
        
    def profile(self):
        print("Iniciando análise dos dados e gerando relatório...")
        self.show_columns()
        self.show_categories_columns()
        self.show_numerical_columns()
        self.count_nulls()
        self.count_just_columns_with_nulls()
        self.unique_values()
        self.value_counts()
        

    def __repr__(self):
        """
        Retorna o relatório completo quando o objeto é chamado diretamente no Jupyter Notebook ou terminal.
        """
        return self.profile() or ''


