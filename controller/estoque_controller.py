from dao.produto_dao import ProdutoDAO
from dao.movimentacao_dao import MovimentacaoDAO
from model.movimentacao import Movimentacao

class EstoqueController:
    def __init__(self):
        self.produto_dao = ProdutoDAO()
        self.movimentacao_dao = MovimentacaoDAO()

    def registrar_entrada(self, produto_codigo: int, quantidade: int, observacao: str) -> tuple[bool, str]:
        """R.F. 5: Processa a entrada de estoque de um produto."""
        if quantidade <= 0:
            return False, "A quantidade de entrada deve ser maior que zero."

        produto = self.produto_dao.buscar_por_id(produto_codigo)
        if not produto:
            return False, "Produto não encontrado."

        # Executa a regra do modelo de domínio e atualiza no banco
        produto.registrar_entrada(quantidade)
        
        # Cria o registro histórico da movimentação
        movimentacao = Movimentacao(tipo="ENTRADA", quantidade=quantidade, observacao=observacao, produto=produto)

        # Salva ambas as entidades
        if self.produto_dao.atualizar(produto) and self.movimentacao_dao.salvar(movimentacao):
            return True, f"Entrada de {quantidade} unidades registrada com sucesso!"
        return False, "Falha operacional ao persistir movimentação."

    def registrar_saida(self, produto_codigo: int, quantidade: int, observacao: str, lista_observers: list = None) -> tuple[bool, str]:
        """R.F. 6, R.N. 3, R.N. 4: Processa saídas de estoque e dispara os gatilhos lógicos."""
        if quantidade <= 0:
            return False, "A quantidade de saída deve ser maior que zero."

        produto = self.produto_dao.buscar_por_id(produto_codigo)
        if not produto:
            return False, "Produto não encontrado."

        # R.N. 3: Limite de Saída por Estoque (Impede estoque negativo)
        if quantidade > produto.quantidade_atual:
            return False, f"Saída bloqueada! Saldo insuficiente. Estoque disponível: {produto.quantidade_atual}"

        # Acopla temporariamente os observers passados pela View (Janela gráfica e Logs)
        if lista_observers:
            for obs in lista_observers:
                produto.adicionar_observer(obs)

        # Modifica o estado do modelo (Aqui dentro do modelo, o gatilho do Observer será testado)
        produto.registrar_saida(quantidade)

        # Cria o registro físico
        movimentacao = Movimentacao(tipo="SAIDA", quantidade=quantidade, observacao=observacao, produto=produto)

        # Atualiza o novo saldo do produto e salva a movimentação
        if self.produto_dao.atualizar(produto) and self.movimentacao_dao.salvar(movimentacao):
            return True, "Saída registrada com sucesso!"
        return False, "Erro ao processar saída no banco de dados."

    def obter_historico(self, produto_codigo: int) -> list:
        """R.F. 10: Retorna o histórico de movimentações ordenado."""
        return self.movimentacao_dao.listar_por_produto(produto_codigo)