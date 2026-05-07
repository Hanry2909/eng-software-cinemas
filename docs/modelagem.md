Com certeza, Hanry! Aqui está o conteúdo completo dos tópicos de 1 a 5.

Você pode copiar todo o bloco abaixo e colar diretamente dentro do seu arquivo modelagem.md.
1. Levantamento de Requisitos e Regras de Negócio

Requisitos Funcionais (RF)

    RF01: O sistema deve permitir o cadastro e gerenciamento de cinemas (endereço e capacidade total).

    RF02: O sistema deve permitir o cadastro de filmes (título, duração, diretor, elenco, gênero).

    RF03: O sistema deve permitir a alocação de filmes em sessões por cinema.

    RF04: O sistema deve permitir o registro diário do público presente em cada sessão.

    RF05: O sistema deve calcular e exibir a totalização de público por sessão, por filme e por cinema.

    RF06: O sistema deve permitir a consulta dos filmes em cartaz e suas informações.

Regras de Negócio (RN)

    RN01: O intervalo de tempo entre duas sessões na mesma sala do cinema deve respeitar o tempo de limpeza e organização obrigatórios (ex: 30 minutos).

    RN02: O público registrado em uma sessão não pode ultrapassar a capacidade máxima estipulada para aquela sala/cinema.

    RN03: Um filme só pode ser colocado em cartaz se possuir todas as informações obrigatórias preenchidas.

    2. Diagrama de Casos de Uso (Visão Geral)
    usecaseDiagram
    actor "Administrador" as Admin
    actor "Espectador" as Espectador

    package "Sistema Rede de Cinemas" {
        usecase "Gerenciar Cinemas" as UC1
        usecase "Gerenciar Filmes" as UC2
        usecase "Gerenciar Sessões" as UC3
        usecase "Registrar Público Diário" as UC4
        usecase "Gerar Relatórios de Público" as UC5
        usecase "Consultar Filmes em Cartaz" as UC6
    }

    Admin --> UC1
    Admin --> UC2
    Admin --> UC3
    Admin --> UC4
    Admin --> UC5

    Espectador --> UC6

    3. Diagrama de Classes do Domínio
    classDiagram
    class Cinema {
        -String nome
        -String endereco
        -int capacidadeTotal
    }

    class Sala {
        -int numero
        -int capacidadeMaxima
    }

    class Filme {
        -String titulo
        -int duracaoMinutos
        -String genero
        -String diretor
        -String elenco
    }

    class Sessao {
        -DateTime dataHoraInicio
        -DateTime dataHoraFim
        -int publicoRegistrado
    }

    Cinema "1" -- "*" Sala : possui
    Sala "1" -- "*" Sessao : abriga
    Filme "1" -- "*" Sessao : exibido em

    4. Diagramas de Atividade
    stateDiagram-v2
    [*] --> BuscarSessao : Administrador inicia registro
    BuscarSessao --> InformarPublico : Sessão encontrada
    InformarPublico --> ValidarCapacidade : Insere quantidade de espectadores
    
    state ValidarCapacidade {
        direction LR
        VerificarLimites : Público <= Capacidade da Sala?
    }
    
    ValidarCapacidade --> RegistrarNoBanco : [Válido]
    ValidarCapacidade --> InformarErro : [Inválido]
    InformarErro --> InformarPublico : Solicitar nova entrada
    
    RegistrarNoBanco --> AtualizarTotalizadores
    AtualizarTotalizadores --> [*] : Registro concluído

    5. Diagramas de Sequência
    sequenceDiagram
    actor Admin
    participant View as SessaoView
    participant Controller as SessaoController
    participant Service as SessaoService
    participant Repo as SessaoRepository
    participant DB as Banco de Dados (SQLite)

    Admin->>View: Informa ID da sessão e total de público
    View->>Controller: registrarPublico(sessaoId, publico)
    Controller->>Service: adicionarPublico(sessaoId, publico)
    Service->>Repo: buscarSessao(sessaoId)
    Repo->>DB: SELECT * FROM sessao WHERE id = sessaoId
    DB-->>Repo: Dados da Sessão
    Repo-->>Service: Objeto Sessao
    
    Note over Service: Service valida se público < capacidade da sala
    
    Service->>Repo: atualizarPublico(sessaoId, publico)
    Repo->>DB: UPDATE sessao SET publico = publico
    DB-->>Repo: Confirmação
    Repo-->>Service: true
    Service-->>Controller: Sucesso
    Controller-->>View: Mensagem de sucesso
    View-->>Admin: "Público registrado com sucesso!"