from utils import parse_csv, write_csv

class TableManager:
    def __init__(self):
        self.tables = {}


    def import_table(self, table_name, file_path):
        parsed = parse_csv(file_path)
        columns = parsed['columns']
        data = parsed['data']
    
        self.tables[table_name] = {
            'columns': columns,
            'data': data
        }

        print(f"[DEBUG] Colunas: {columns}")
        print(f"[DEBUG] Dados: {data}")

    def export_table(self, table_name, file_path):
        if table_name in self.tables:
            write_csv(file_path, self.tables[table_name])
        else:
            raise ValueError(f"Tabela '{table_name}' não encontrada")

    def discard_table(self, table_name):
        if table_name in self.tables:
            del self.tables[table_name]
        else:
            raise ValueError(f"Tabela '{table_name}' não encontrada")

    def rename_table(self, old_name, new_name):
        if old_name in self.tables:
            self.tables[new_name] = self.tables.pop(old_name)
        else:
            raise ValueError(f"Tabela '{old_name}' não encontrada")

    def print_table(self, table_name):
        print(f"[DEBUG] Tentando imprimir tabela: {table_name}")
        if table_name in self.tables:
            table = self.tables[table_name]
        
            # Imprime os nomes das colunas
            print(" | ".join(table['columns']))
        
            # Itera sobre as linhas de dados
            for row in table['data']:
                # Imprime a linha, convertendo os elementos para string
                print(" | ".join(str(x) for x in row))
        else:
            raise ValueError(f"Tabela '{table_name}' não encontrada")

    def select(self, table_name, fields, condition=None):
        if table_name not in self.tables:
            raise ValueError(f"Tabela '{table_name}' não encontrada")

        table = self.tables[table_name]
        columns = table['columns']
        data = table['data']
        
        # Determina quais colunas selecionar
        if fields == '*':
            selected_cols = columns
            col_indices = list(range(len(columns)))
        else:
            selected_cols = fields
            col_indices = [columns.index(col) for col in fields]
        
        # Filtra linhas baseado na condição
        filtered_data = []
        for row in data:
            if condition is None or self._evaluate_condition(condition, columns, row):
                filtered_data.append([row[i] for i in col_indices])
        
        return {'columns': selected_cols, 'data': filtered_data}

    def _evaluate_condition(self, condition, columns, row):
        if isinstance(condition, tuple) and len(condition) == 3:
            op, col, value = condition
            col_index = columns.index(col)
            cell_value = row[col_index]

            # Tenta converter os valores para float 
            try:
                cell_value = float(cell_value)
                value = float(value)
            except ValueError:
                pass  # Se não for possível, mantém como string para comparação textual

            # Comparação dos valores após a conversão
            if op == '=': 
                return cell_value == value
            elif op == '<>': 
                return cell_value != value
            elif op == '<': 
                return cell_value < value
            elif op == '>': 
                return cell_value > value
            elif op == '<=': 
                return cell_value <= value
            elif op == '>=': 
                return cell_value >= value

        elif isinstance(condition, tuple) and len(condition) == 3:
            # Condição composta (AND / OR)
            op, left, right = condition
            left_result = self._evaluate_condition(left, columns, row)
            right_result = self._evaluate_condition(right, columns, row)
        
            if op == 'AND': 
                return left_result and right_result
            elif op == 'OR': 
                return left_result or right_result

        return False

    def create_table(self, table_name, data):
        print(f"Criando tabela '{table_name}' com os dados:", data)  # Debugging
        self.tables[table_name] = data

    def join_tables(self, table1_name, table2_name, join_field):
        print(f"Realizando junção entre '{table1_name}' e '{table2_name}' usando '{join_field}'")  # Debugging
        if table1_name not in self.tables or table2_name not in self.tables:
            raise ValueError("Uma das tabelas não foi encontrada")

        table1 = self.tables[table1_name]
        table2 = self.tables[table2_name]
    
        try:
            join_index1 = table1['columns'].index(join_field)
            join_index2 = table2['columns'].index(join_field)
        except ValueError:
            raise ValueError(f"Campo de junção '{join_field}' não encontrado em uma das tabelas")

        new_columns = table1['columns'] + [
            col for col in table2['columns'] if col != join_field
        ]
        joined_data = []
        for row1 in table1['data']:
            for row2 in table2['data']:
                if row1[join_index1] == row2[join_index2]:
                    new_row = row1 + [
                        val for i, val in enumerate(row2) if i != join_index2
                    ]
                    joined_data.append(new_row)

        print(f"Junção resultante ({len(joined_data)} linhas)")  # Debugging
        return {'columns': new_columns, 'data': joined_data}