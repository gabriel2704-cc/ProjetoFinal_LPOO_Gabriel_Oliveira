from model.interfaces import Subject

class Produto(Subject):
    def __init__(self, nome, preco, quantidade_atual, quantidade_minima=5, categoria=None, fornecedor=None, codigo=None):
        super().__init__()
        self.codigo = codigo
        self.nome = nome
        self.preco = float(preco)
        self.quantidade_atual = int(quantidade_atual)
        self.quantidade_minima = int(quantidade_minima)
        self.categoria = categoria
        self.fornecedor = fornecedor  # Instância da classe Fornecedor

    def registrar_entrada(self, qtd: int) -> None:
        self.quantidade_atual += qtd

    def registrar_saida(self, qtd: int) -> None:
        # A validação de saldo insuficiente (R.N. 3) será feita no Controller,
        # mas aqui nós deduzimos o valor e verificamos o gatilho do Observer.
        self.quantidade_atual -= qtd
        
        if self.estoque_critico():
            self.notificar_observers() # Dispara o popup visual e o log

    def estoque_critico(self) -> bool:
        return self.quantidade_atual <= self.quantidade_minima