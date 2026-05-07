# Projeto: Sistema de Gestão - Rede de Cinemas 🎬

**Disciplina:** Engenharia de Software  
**Professor:** Max  
**Aluno:** Hanry (RA: 24001865)  

---

## 📌 Sobre o Projeto

Este repositório contém os artefatos de modelagem e a implementação prática referente ao caso de estudo **Rede de Cinemas**. O objetivo do projeto é desenvolver um sistema de informação capaz de centralizar e organizar os dados de uma rede de cinemas com diversas unidades.

O sistema visa solucionar desafios comuns do negócio, tais como:
* Controle de filmes em exibição por cinema.
* Organização das sessões, respeitando durações e intervalos.
* Registro e validação diária do público de cada sessão (evitando superlotação).
* Totalização de dados e consulta de informações de filmes.

A solução foi desenvolvida mantendo a coerência entre o levantamento de requisitos, a modelagem em UML (Casos de Uso, Classes, Atividades e Sequência) e a implementação em código.

## 📂 Estrutura do Repositório

* **`/docs`**: Contém o arquivo `modelagem.md` com os requisitos, regras de negócio e todos os diagramas UML (escritos em Mermaid para renderização nativa).
* **`/src`**: Contém o código-fonte da aplicação (`main.py`), implementado em Python utilizando a arquitetura **MVC + Service + Repository** e persistência de dados em **SQLite**.

## 🚀 Como Executar a Aplicação

A implementação contempla o caso de uso **Registrar Público Diário**. Para testar:

1. Certifique-se de ter o Python instalado na sua máquina.
2. Navegue até a pasta `src` do projeto.
3. Execute o arquivo principal:
   ```bash
   python main.py