import sqlite3
from dataclasses import dataclass

# --- Entidade (Model) ---
@dataclass
class Sessao:
    id: int
    filme_titulo: str
    capacidade_sala: int
    publico_registrado: int

# --- Camada de Persistência (Repository) ---
class SessaoRepository:
    def __init__(self, db_path='cinema.db'):
        self.db_path = db_path
        self._inicializar_banco()

    def _inicializar_banco(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''CREATE TABLE IF NOT EXISTS sessao 
                (id INTEGER PRIMARY KEY, filme_titulo TEXT, 
                capacidade_sala INTEGER, publico_registrado INTEGER)''')
            # Dados iniciais de teste
            conn.execute('INSERT OR IGNORE INTO sessao VALUES (1, "Batman", 150, 0)')

    def buscar_por_id(self, sessao_id):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM sessao WHERE id = ?', (sessao_id,))
            row = cursor.fetchone()
            if row: return Sessao(*row)
        return None

    def atualizar_publico(self, sessao_id, novo_total):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('UPDATE sessao SET publico_registrado = ? WHERE id = ?', 
                         (novo_total, sessao_id))

# --- Camada de Negócio (Service) ---
class SessaoService:
    def __init__(self, repository: SessaoRepository):
        self.repo = repository

    def registrar_entrada_publico(self, sessao_id, quantidade):
        sessao = self.repo.buscar_por_id(sessao_id)
        if not sessao:
            return "Erro: Sessão não encontrada."
        
        novo_publico = sessao.publico_registrado + quantidade
        if novo_publico > sessao.capacidade_sala:
            return f"Erro: Capacidade máxima excedida! (Tentativa: {novo_publico} / Limite: {sessao.capacidade_sala})"
        
        self.repo.atualizar_publico(sessao_id, novo_publico)
        return f"Sucesso! {quantidade} pessoas registradas. Total atual: {novo_publico}."

# --- Camada de Controle (Controller) ---
class SessaoController:
    def __init__(self, service: SessaoService):
        self.service = service

    def executar_registro(self, id_sessao, qtd):
        try:
            return self.service.registrar_entrada_publico(int(id_sessao), int(qtd))
        except ValueError:
            return "Erro: Por favor, insira números válidos."

# --- Interface Simples (View) ---
if __name__ == "__main__":
    banco = SessaoRepository()
    servico = SessaoService(banco)
    controle = SessaoController(servico)

    print("-" * 40)
    print("SISTEMA DE GESTÃO DE CINEMA")
    print("-" * 40)
    
    id_s = input("Digite o ID da Sessão: ")
    puv = input("Quantidade de público a registrar: ")
    
    resultado = controle.executar_registro(id_s, puv)
    print(f"\nResultado: {resultado}\n")