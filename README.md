# Sistema de Controle de Estoque e Fornecedores

* **Nome:** Gabriel de Oliveira
* **Curso:** Bacharelado em Ciência da Computação
* **Disciplinas Integradas:** Análise e Projeto de Sistemas (APS) e Linguagem e Programação Orientada a Objetos (LPOO)
* **Instituição:** Faculdade de Computação

---

## Descrição do Sistema Projetado
O **Sistema de Controle de Estoque e Fornecedores** consiste em uma aplicação desktop desenvolvida em linguagem Python, cujo objetivo primordial é a automação do fluxo de armazenamento e o gerenciamento cadastral de entidades corporativas parceiras. O sistema foi projetado para mitigar as inconsistências geradas por registros manuais em pequenas e médias empresas do setor comercial e industrial.

O artefato de software provê mecanismos para o controle rigoroso de entradas e saídas de insumos, garantindo a integridade dos dados por meio de especificações técnicas delimitadas:
* **Interface Gráfica Local (Tkinter):** Ambiente operacional nativo que dispensa conectividade síncrona com a internet, priorizando o tempo de resposta e a portabilidade em sistemas locais.
* **Persistência Objeto-Relacional (PostgreSQL):** Gerenciamento de estado em banco de dados relacional com aplicação de restrições de integridade, impedindo a ocorrência de saldos negativos em estoque.
* **Validação de Dados em Camada de Domínio:** Verificação sintática ativa de restrições relacionais (chaves estrangeiras) e validação matemática de formato de CNPJ.

---

## Arquitetura de Software e Divisão de Pacotes
A especificação estrutural do sistema fundamenta-se nos princípios da Programação Orientada a Objetos e adota o padrão arquitetural **MVC (Model-View-Controller)** integrado à camada de persistência **DAO (Data Access Object)**. A organização do código-fonte distribui-se de forma coesa nos seguintes pacotes:

1. **`view/`**: Responsável exclusivo pela renderização dos componentes de interface gráfica (`TelaFornecedorGUI`, `TelaProdutoGUI`, `TelaMovimentacaoGUI`) e pela exibição de subcomponentes visuais de aviso (`AlertaEstoqueObserver`).
2. **`controller/`**: Centraliza as regras de orquestração do sistema, interceptando os eventos originados na camada de visão, invocando os métodos de persistência e manipulando as entidades de domínio.
3. **`model/`**: Reúne as classes de entidade puras (`Fornecedor`, `Produto`, `Movimentacao`) e suas regras de negócio intrínsecas, estendendo formalmente o contrato do padrão comportamental **Observer** por meio das interfaces `Subject` e `Observer`.
4. **`dao/`**: Abstrai as rotinas de manipulação e execução de instruções SQL dirigidas ao PostgreSQL, isolando o controle de ciclo de vida da conexão física (`ConexaoBD`).

### Diagrama de Classes de Implementação (UML)

![Diagrama de Classes Oficial](imagens/DiagramadeClasses.png)

---

## Acesso à Documentação do Projeto
O detalhamento completo concernente ao levantamento de requisitos, diagramas de casos de uso, matrizes de rastreabilidade, especificações de fluxos alternativos e modelagens complementares (Conceitual e de Sequência) encontra-se disponível no arquivo anexo através do link:

[Acessar o Arquivo: Documentação do Projeto.md](Documentacao_do_Projeto.md)

---

## Conclusão e Relato de Aprendizado

### Desafios Enfrentados e Resoluções Técnicas


### Principais Aprendizados Obtidos

---

## Declaração de Uso de Inteligência Artificial



* **Ferramenta e Modelo:** Google Gemini.
* **Escopo de Aplicação:** * *Refinamento Sintático UML:* Revisão das amarrações textuais do código PlantUML, garantindo a conformidade da notação de blocos alternativos (`alt/else`) no Diagrama de Sequência e a correta categorização dos pacotes do padrão MVC no Diagrama de Classes de Implementação.
  * *Padronização de Documentos:* Apoio na estruturação formal da linguagem de marcação Markdown e na formatação das tabelas de requisitos do sistema.
* **Aprendizado Metodológico:** O processo demonstrou que modelos de linguagem atuam com eficácia na validação sintática e aceleração de formatação documental, desde que submetidos a prompts estruturados. A validação das saídas geradas exigiu análise crítica constante, reforçando que o design lógico, a modelagem arquitetural e a codificação final em Python constituem produções estritamente autorais do discente.