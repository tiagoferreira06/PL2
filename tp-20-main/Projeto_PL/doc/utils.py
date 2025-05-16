import csv

def parse_csv(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        
        
        rows = []
        for row in reader:
            if not row or row[0].startswith('#'):
                continue
            rows.append(row)
        
        if not rows:
            return {'columns': [], 'data': []}
        
        columns = rows[0]
        data = []
        
        # Processa linhas de dados
        for row in rows[1:]:
            # Remove aspas se existirem
            processed_row = []
            for cell in row:
                if cell.startswith('"') and cell.endswith('"'):
                    processed_row.append(cell[1:-1])
                else:
                    processed_row.append(cell)
            data.append(processed_row)
        
        return {'columns': columns, 'data': data}

def write_csv(file_path, table_data):
    with open(file_path, 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        
        # Escreve cabeçalho
        writer.writerow(table_data['columns'])
        
        # Escreve dados
        for row in table_data['data']:
            writer.writerow(row)
