import sqlite3
from dataclasses import dataclass

# ==========================================
# CONFIGURAÇÃO INICIAL DO BANCO (DIDÁTICO)
# ==========================================
def setup_database():
    conn = sqlite3.connect('cinema.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sessao (
            id INTEGER PRIMARY KEY,
            filme_titulo TEXT,
            capacidade_sala INTEGER,
            publico_registrado INTEGER
        )
    ''')
    # Inserindo dados mockados para teste
    cursor.execute('DELETE FROM sessao')
    cursor.execute('INSERT INTO sessao (id, filme_titulo, capacidade_sala, publico_registrado) VALUES (1, "Oppenheimer", 100, 0)')
    conn.commit()
    conn.close()

# ==========================================
# DOMAIN MODEL (Entidade)
# ==========================================
@dataclass
class Sessao:
    id: int
    filme_titulo: str
    capacidade_sala: int
    publico_registrado: int

# ==========================================
# REPOSITORY LAYER
# ==========================================
class SessaoRepository:
    def __init__(self, db_path='cinema.db'):
        self.db_path = db_path

    def buscar_por_id(self, sessao_id: int) -> Sessao:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT id, filme_titulo, capacidade_sala, publico_registrado FROM sessao WHERE id = ?', (sessao_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return Sessao(id=row[0], filme_titulo=row[1], capacidade_sala=row[2], publico_registrado=row[3])
        return None

    def atualizar_publico(self, sessao_id: int, novo_publico: int):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('UPDATE sessao SET publico_registrado = ? WHERE id = ?', (novo_publico, sessao_id))
        conn.commit()
        conn.close()

# ==========================================
# SERVICE LAYER (Regras de Negócio)
# ==========================================
class SessaoService:
    def __init__(self, repository: SessaoRepository):
        self.repository = repository

    def registrar_publico(self, sessao_id: int, publico: int) -> str:
        sessao = self.repository.buscar_por_id(sessao_id)
        
        if not sessao:
            return "Erro: Sessão não encontrada."
        
        # Regra de Negócio: Público não pode exceder capacidade
        novo_total = sessao.publico_registrado + publico
        if novo_total > sessao.capacidade_sala:
            return f"Erro: O público total ({novo_total}) excede a capacidade da sala ({sessao.capacidade_sala})."
        
        self.repository.atualizar_publico(sessao_id, novo_total)
        return f"Sucesso! Público atualizado. Total atual da sessão: {novo_total} espectadores."

# ==========================================
# CONTROLLER LAYER
# ==========================================
class SessaoController:
    def __init__(self, service: SessaoService):
        self.service = service

    def processar_registro_publico(self, sessao_id_str: str, publico_str: str) -> str:
        try:
            sessao_id = int(sessao_id_str)
            publico = int(publico_str)
            if publico < 0:
                return "Erro: O público não pode ser negativo."
            return self.service.registrar_publico(sessao_id, publico)
        except ValueError:
            return "Erro: Por favor, insira valores numéricos válidos."

# ==========================================
# VIEW LAYER (Interface do Usuário / CLI)
# ==========================================
class SessaoView:
    def __init__(self, controller: SessaoController):
        self.controller = controller

    def exibir_menu(self):
        print("\n--- Sistema de Gestão de Cinemas ---")
        print("1. Registrar Público da Sessão")
        print("2. Sair")
        
    def iniciar(self):
        while True:
            self.exibir_menu()
            opcao = input("Escolha uma opção: ")
            
            if opcao == '1':
                sessao_id = input("Digite o ID da sessão (Use 1 para teste): ")
                publico = input("Digite a quantidade de público a registrar: ")
                
                resultado = self.controller.processar_registro_publico(sessao_id, publico)
                print(f"\n>> {resultado}")
            
            elif opcao == '2':
                print("Encerrando o sistema...")
                break
            else:
                print("Opção inválida.")

# ==========================================
# INJEÇÃO DE DEPENDÊNCIA E EXECUÇÃO
# ==========================================
if __name__ == "__main__":
    setup_database() # Prepara o banco SQlite
    
    # Montando a arquitetura
    repo = SessaoRepository()
    service = SessaoService(repo)
    controller = SessaoController(service)
    view = SessaoView(controller)
    
    # Iniciando o sistema
    view.iniciar()