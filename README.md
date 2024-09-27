# Projeto TecProg

Este projeto foi desenvolvido como parte da conclusão da disciplina de Técnicas de Programação 1 do curso de Engenharia de Dados da [Ada Tech](https://ada.tech/sou-aluno/programas/santander-coders-2024) em parceria com o Santander Coders. 
O objetivo é criar um módulo de Data Quality utilizando Programação Orientada a Objetos (POO), que será importado em um Jupyter Notebook para gerar relatórios de análise de datasets.

## Descrição do Projeto

O módulo desenvolvido permitirá realizar análises de qualidade em qualquer conjunto de dados (dataset). As principais funcionalidades incluem:

- **Contagem de Nulos**: Identificação e contagem de valores nulos em cada coluna do dataset.
- **Contagem de Valores Únicos**: Cálculo da quantidade de valores únicos presentes em cada coluna.
- **Análise de Colunas Categóricas**: Geração de `value_counts` para colunas categóricas, proporcionando uma visão clara da distribuição de categorias.
- **Estatísticas Descritivas**: Uso do método `describe()` nas colunas numéricas para fornecer estatísticas como média, mediana, mínimo e máximo.
- **Visualizações**:
  - Gráficos de distribuição para colunas categóricas, permitindo a visualização da frequência de cada categoria.
  - Gráficos de distribuição para colunas numéricas, oferecendo insights sobre a dispersão e a forma dos dados.

## Estrutura do Projeto

Abaixo está a estrutura de arquivos do projeto:

#### Módulo principal para análise de qualidade de dados 
├── .gitignore 
├── data_quality.py 

#### Jupyter Notebook que utiliza o módulo para análises
├── dotebook.ipynb 

#### Pasta contendo os datasets para análise
├── dinput 

# Como Usar

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/naiieandrade/DataQuality.git
2. **Instale as dependências**: Certifique-se de ter o Python e o Jupyter Notebook instalados. Você pode instalar as dependências necessárias usando:

   ```bash
   pip install -r requirements.txt
3. **Execute o Jupyter Notebook**: Navegue até o diretório do projeto e inicie o Jupyter Notebook:
   ```bash
   jupyter notebook notebook.ipynb
# Contribuição
Contribuições são bem-vindas! Se você deseja contribuir, sinta-se à vontade para abrir uma issue ou enviar um pull request.

# Licença
Este projeto está licenciado sob a [MIT License](https://opensource.org/license/mit).