# Dashboard Financeiro Familiar – Streamlit

Sistema web desenvolvido em Python + Streamlit para controle financeiro pessoal/familiar, permitindo registrar receitas, despesas, visualizar gráficos e gerenciar lançamentos.


## Funcionalidades
 1. Cadastro de registros financeiros (receitas e despesas)
 2. Visualização em dashboard com gráficos interativos
 3. Gerenciamento de registros (editar e excluir)
 4. Armazenamento local usando SQLite
 5. Filtros por data e tipo de lançamento


## Tecnologias

 - Python 3
 - Streamlit
 - Pandas
 - SQLite
 - Plotly
 
## Estrutura do Projeto
```
dashboard/
│
├── main.py
├── banco.db
├── paginas/
│   ├── adicionar_registro.py
│   ├── dashboard.py
│   └── gerenciar_registros.py
└── README.md
```
## Como executar
Crie um ambiente virtual (opcional, mas recomendado):
```
python -m venv venv
venv\Scripts\activate
```

Instale as dependências:
```
pip install streamlit pandas plotly
```

Execute a aplicação:
```
streamlit run main.py
```

Acesse no navegador:

http://localhost:8501

## Funcionalidades do Menu
Menu	Descrição
Dashboard	Mostra gráficos e resumo financeiro
Adicionar Registro	Permite inserir receitas e despesas
Gerenciar Registros	Editar ou excluir lançamentos
 __Banco de Dados__

 _Tabela registros:_

CREATE TABLE registros (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo TEXT,
    fonte TEXT,
    valor REAL,
    data DATE
);
## Próximas melhorias


- Categorias personalizadas
- Exportação para Excel/PDF
- Metas financeiras mensais