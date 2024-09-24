import pandas as pd

class DataQuality:
    def __init__(self, path: str):
        self.path = path
        self.df = self.read_data()

    def read_data(self):
        extension = self.path.split('.')[-1]
        if extension == 'csv':
            try:
                data = pd.read_csv(self.path, encoding='utf-8')
                return data
            except UnicodeDecodeError:
                data = pd.read_csv(self.path, encoding='latin-1')  # Tenta ler com outra codificação
                return data
        elif extension == 'json':
            print('json')
        elif extension == 'xlsx':
            data = pd.read_excel(self.path) # Lê o arquivo Excel
            return data
        else:
            print(f"Formato /'{extension}/' não reconhecido.")

    def show_columns(self):
        print(f"Quantidade de colunas: {len(self.df.columns)}\n")
        n = 1

        print(f"Colunas do dataframe {self.path}\n")
        for _ in list(self.df.columns):
            print(f"{n}: {_}")
            n += 1

        print('\n')

    def count_nulls(self):
        print("Quantidade de valores nulos por coluna:")
        print(self.df.isna().sum())

    def profile(self):
        print("Iniciando análise dos dados e gerando relatório...")
        self.show_columns()
        self.count_nulls()

    def __repr__(self):
        """
        Retorna o relatório completo quando o objeto é chamado diretamente no Jupyter Notebook ou terminal.
        """
        return self.profile() or ''


