📊 CQL - Comma Query Language
Um interpretador em Python para consultar e manipular arquivos CSV usando uma sintaxe semelhante a SQL.
🔍 Visão Geral
CQL (Comma Query Language) é uma linguagem específica de domínio projetada para simplificar a manipulação de arquivos CSV. Este projeto implementa um interpretador para CQL usando Python e a biblioteca PLY (Python Lex-Yacc), fornecendo uma interface familiar semelhante a SQL para trabalhar com dados tabulares armazenados em formato CSV.
✨ Funcionalidades

Importação/Exportação 📥📤: Carrega arquivos CSV para a memória e salva tabelas de volta ao disco
Consultas de Dados 🔎: Seleciona colunas específicas, filtra dados com condições
Criação de Tabelas 🏗️: Cria novas tabelas a partir de consultas ou unindo tabelas existentes
Manipulação de Dados 🛠️: Suporte para filtrar, mesclar e transformar dados tabulares
Procedimentos 📝: Define blocos reutilizáveis de comandos (em desenvolvimento)

📁 Estrutura do Projeto
doc/
├── cql_lexer.py     # Analisador léxico para tokenização de comandos CQL
├── cql_parser.py    # Analisador sintático para análise de declarações CQL
├── tables.py        # Classes e funções para operações de tabela
├── utils.py         # Funções auxiliares
└── main.py          # Ponto de entrada do programa principal
└── executor.py      # Executador
└── Trabalho Prático - Grupo 20.pdf

📝 Sintaxe dos Comandos
Comandos Básicos
Importando Arquivos CSV
IMPORT TABLE <nome_tabela> FROM "ficheiro"
Removendo Tabelas da Memória
DISCARD TABLE <nome_tabela>
Consultando Dados
Select Básico
SELECT FROM <nome_tabela>
Select com Especificação de Colunas
SELECT <coluna1>, <coluna2>, ... FROM <nome_tabela>
Select com Condições
SELECT FROM <nome_tabela> WHERE <condição>
As condições podem usar operadores como =, <>, <, >, <=, >= e podem ser combinadas com AND e OR.
Criando Tabelas
A partir de uma Consulta
CREATE TABLE <nova_tabela> AS SELECT FROM <tabela_origem> WHERE <condição>

🚀 Instalação
Python 3.6+ instalado
Instale a biblioteca PLY necessária:
pip install ply

Clone o repositório ou baixe o código-fonte

💻 Uso

Execute o programa principal:
python main.py

Digite os comandos CQL no prompt
Veja os resultados diretamente no console

🔄 Exemplo de Sessão
> IMPORT TABLE estacoes FROM FILE "estacoes.csv"
Tabela 'estacoes' importada com sucesso.

> SELECT FROM estacoes WHERE Temp > 22
| ID | Location | Temp | Humidity |
|----|----------|------|----------|
| 2  | Porto    | 24   | 65       |
| 5  | Faro     | 27   | 55       |

> CREATE TABLE locais_quentes AS SELECT FROM estacoes WHERE Temp > 25
Tabela 'locais_quentes' criada com sucesso.

> EXPORT TABLE locais_quentes TO FILE "locais_quentes.csv"
Tabela 'locais_quentes' exportada com sucesso.
👨‍💻 Desenvolvimento
Este projeto foi desenvolvido como parte da disciplina de Processamento de Linguagens pelo Grupo 20:

Luís Pereira (27953)
Tiago Ferreira (27980)
Rodrigo Cruz (27971)

🔧 Dependências

Python 3.6+
Biblioteca PLY (Python Lex-Yacc)
