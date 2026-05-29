# Documentação do Projeto

## Sistema de Controle de Estoque e Fornecedores
* **Disciplina:** Análise e Projeto de Sistemas (APS) + Linguagem e Programação de Orientação a Objetos (LPOO)
* **Curso:** Bacharelado em Ciência da Computação
* **Aluno:** Gabriel de Oliveira

---

## 1. Descrição e Delimitação do Escopo

### 1.1 Cenário do Sistema
Pequenas e médias empresas do setor comercial e industrial frequentemente enfrentam dificuldades no controle manual de estoques: produtos em falta sem aviso prévio, fornecedores desorganizados em planilhas dispersas e ausência de histórico de movimentações. Esses problemas geram perdas financeiras, interrupções na operação e tomada de decisão baseada em dados desatualizados.

O Sistema de Controle de Estoque e Fornecedores é uma aplicação desktop desenvolvida em Python com interface gráfica (Tkinter) e persistência em banco de dados relacional (PostgreSQL). O sistema centraliza o cadastro de fornecedores e produtos, registra toda movimentação de entrada e saída de mercadorias e alerta automaticamente o operador quando o estoque de um produto atinge nível crítico.

### 1.2 Público-Alvo
O sistema destina-se a operadores de estoque, almoxarifes e gestores de pequenas empresas que necessitam de uma ferramenta simples, local e confiável para controle diário de mercadorias, sem dependência de conexão com a internet ou infraestrutura de servidores externos.

### 1.3 Problema que o Sistema Resolve


| Problema | Solução oferecida pelo sistema |
| :--- | :--- |
| Falta de visibilidade do estoque em tempo real | Tela de listagem com quantidades atualizadas a cada operação |
| Fornecedores registrados em planilhas sem padronização | Cadastro estruturado com validação de CNPJ e dados de contato |
| Ausência de histórico de movimentações | Registro completo de entradas e saídas com data, hora e observação |
| Risco de ruptura de estoque sem aviso | Alerta automático (Observer) quando quantidade cai abaixo do mínimo definido |
| Dificuldade em rastrear produtos por fornecedor | Filtro de produtos por fornecedor vinculado |

### 1.4 Escopo Funcional (O que o sistema FAZ)
* Cadastrar, consultar, editar e excluir fornecedores com validação de CNPJ.
* Cadastrar, consultar, editar e excluir produtos vinculados a fornecedores.
* Registrar movimentações de entrada e saída no estoque.
* Exibir histórico de movimentações por produto.
* Emitir alerta visual e registrar em log quando o estoque atinge nível mínimo.
* Filtrar produtos por nome e por fornecedor.
* Exibir tela "Sobre" com informações do sistema e do autor.

### 1.5 Fora do Escopo (O que o sistema NÃO FAZ)
* Emissão de notas fiscais ou documentos fiscais.
* Integração com sistemas ERP externos.
* Controle de múltiplos depósitos ou filiais.
* Gestão financeira ou controle de pagamentos a fornecedores.
* Acesso multiusuário simultâneo com controle de permissões.

---

## 2. Fase de Análise

### 2a. Requisitos Funcionais


| ID | Descrição |
| :--- | :--- |
| **RF01** | O sistema deve permitir cadastrar um fornecedor informando nome, CNPJ, telefone de contato, e-mail e status (ativo/inativo). |
| **RF02** | O sistema deve validar o formato do CNPJ no momento do cadastro ou edição do fornecedor, recusando entradas fora do padrão `XX.XXX.XXX/XXXX-XX`. |
| **RF03** | O sistema deve permitir editar os dados de um fornecedor já cadastrado. |
| **RF04** | O sistema deve impedir a exclusão de um fornecedor que possua produtos vinculados, exibindo mensagem explicativa ao operador. |
| **RF05** | O sistema deve permitir cadastrar um produto informando nome, descrição, preço, quantidade inicial, quantidade mínima, categoria e fornecedor responsável. |
| **RF06** | O sistema deve permitir registrar uma entrada de estoque para um produto, informando a quantidade recebida e uma observação opcional. |
| **RF07** | O sistema deve permitir registrar uma saída de estoque para um produto, informando a quantidade retirada e uma observação opcional. |
| **RF08** | O sistema deve impedir o registro de uma saída cuja quantidade solicitada seja superior à quantidade disponível em estoque, exibindo mensagem de erro. |
| **RF09** | O sistema deve emitir um alerta visual (popup) ao operador sempre que, após uma saída, a quantidade em estoque de um produto for igual ou inferior à sua quantidade mínima configurada. |
| **RF10** | O sistema deve registrar em arquivo de log todas as ocorrências de estoque abaixo do mínimo, contendo produto, quantidade atual, quantidade mínima e data/hora do evento. |
| **RF11** | O sistema deve exibir o histórico completo de movimentações de um produto selecionado, ordenado da mais recente para a mais antiga. |
| **RF12** | O sistema deve permitir filtrar a lista de produtos por nome (busca parcial, sem diferenciação de maiúsculas e minúsculas) e por fornecedor vinculado. |
| **RF13** | O sistema deve permitir filtrar a lista de fornecedores por nome ou CNPJ. |
| **RF14** | O sistema deve exibir uma tela "Sobre" contendo o nome do sistema, descrição resumida, nome do autor, disciplina e semestre. |

### 2b. Requisitos Não Funcionais


| ID | Categoria | Descrição |
| :--- | :--- | :--- |
| **RNF01** | Usabilidade | A interface deve ser navegável exclusivamente pelo menu principal, sem exigir conhecimento técnico do operador. Todas as ações destrutivas (exclusão) devem solicitar confirmação antes de serem executadas. |
| **RNF02** | Desempenho | As operações de listagem, inserção e atualização no banco de dados devem ser concluídas em no máximo 2 segundos em condições normais de uso (base com até 10.000 registros). |
| **RNF03** | Confiabilidade | O sistema deve garantir a integridade referencial dos dados por meio de chaves estrangeiras no banco de dados. Toda operação de escrita deve ser executada dentro de uma transação, com rollback automático em caso de falha. |
| **RNF04** | Manutenibilidade | O código deve estar organizado em camadas bem definidas (model, dao, controller, view, patterns), seguindo o padrão DAO e o princípio de responsabilidade única, de forma que a substituição do banco de dados ou da biblioteca gráfica impacte apenas a camada correspondente. |
| **RNF05** | Portabilidade | O sistema deve executar em qualquer sistema operacional que possua Python 3.10 ou superior, Tkinter e acesso a uma instância PostgreSQL, sem necessidade de instalação de dependências nativas além das listadas no `requirements.txt`. |
| **RNF06** | Segurança | Todas as queries ao banco de dados devem utilizar parâmetros parametrizados (prepared statements via psycopg2) para prevenir injeção de SQL. Nenhuma credencial de banco deve ser exposta no código-fonte; devem ser lidas de variável de ambiente ou arquivo `.env`. |
