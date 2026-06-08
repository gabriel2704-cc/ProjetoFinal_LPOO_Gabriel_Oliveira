class Movimentacao:
    def __init__(self, tipo, quantidade, observacao, produto, data_hora=None, codigo=None):
        self.codigo = codigo
        self.tipo = tipo          # 'ENTRADA' ou 'SAIDA'
        self.quantidade = quantidade
        self.data_hora = data_hora
        self.observacao = observacao
        self.produto = produto    # Instância da classe Produto

    def __str__(self):
        return f"{self.tipo} - {self.quantidade} un. em {self.data_hora}"