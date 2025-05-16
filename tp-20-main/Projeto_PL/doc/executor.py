from tables import TableManager
import os

BASE_DIR = os.path.join(os.getcwd(), 'data')

class CommandExecutor:
    def __init__(self):
        self.table_manager = TableManager()
        self.procedures = {}

    def execute(self, command):
        cmd_type = command[0]
        
        if cmd_type == 'IMPORT':
            _, table_name, file_path = command
            full_file_path = os.path.join(BASE_DIR, file_path)
            self.table_manager.import_table(table_name, full_file_path)
            
        elif cmd_type == 'EXPORT':
            _, table_name, file_path = command
            full_file_path = os.path.join(BASE_DIR, file_path)
            self.table_manager.export_table(table_name, file_path)
            
        elif cmd_type == 'DISCARD':
            _, table_name = command
            self.table_manager.discard_table(table_name)
            
        elif cmd_type == 'RENAME':
            _, old_name, new_name = command
            print(f"[DEBUG] Comando RENAME executado: {old_name} -> {new_name}")  
            self.table_manager.rename_table(old_name, new_name)
            
        elif cmd_type == 'PRINT':
            _, _, table_name = command  
            self.table_manager.print_table(table_name)
            
        elif cmd_type == 'SELECT':
            _, fields, table_name, condition, limit = command
            result = self.table_manager.select(table_name, fields, condition)
            if limit:
                result['data'] = result['data'][:limit]
            return result
            
        elif cmd_type == 'CREATE_FROM_SELECT':
            _, new_table_name, select_command = command
            result = self.execute(select_command)
            self.table_manager.create_table(new_table_name, result)
            
        elif cmd_type == 'CREATE_FROM_JOIN':
            _, new_table_name, table1, table2, join_field = command
            result = self.table_manager.join_tables(table1, table2, join_field)
            self.table_manager.create_table(new_table_name, result)
            
        elif cmd_type == 'PROCEDURE_DECLARE':
            _, proc_name, commands = command
            self.procedures[proc_name] = commands
            
        elif cmd_type == 'PROCEDURE_CALL':
            _, proc_name = command
            if proc_name in self.procedures:
                for cmd in self.procedures[proc_name]:
                    self.execute(cmd)
            else:
                print(f"Procedimento '{proc_name}' não encontrado.")