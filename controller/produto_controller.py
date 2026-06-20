from dao.produto_dao import ProdutoDAO
from model.produto import Produto

class ProdutoController:
    def __init__(self):
        self.produto_dao = ProdutoDAO()

    def cadastrar_produto(self, nome: str, preco: float, qtd_atual: int, qtd_minima: int, categoria: str, descricao: str, fornecedor_obj) -> tuple[bool, str]:
        """Cadastra um produto garantindo os vínculos obrigatórios."""
        if not fornecedor_obj:
            return False, "Erro: Um produto deve obrigatoriamente possuir um Fornecedor vinculado!"

        novo_produto = Produto(nome=nome, preco=preco, quantidade_atual=qtd_atual, 
                               quantidade_minima=qtd_minima, categoria=categoria, descricao=descricao, fornecedor=fornecedor_obj)

        sucesso = self.produto_dao.salvar(novo_produto)
        if sucesso:
            return True, "Produto cadastrado com sucesso!"
        return False, "Erro ao salvar produto no banco."

    def atualizar_produto(self, codigo: int, nome: str, preco: float, qtd_atual: int, qtd_minima: int, categoria: str, descricao: str, fornecedor_obj) -> tuple[bool, str]:
        if not fornecedor_obj:
            return False, "Erro: Um produto deve obrigatoriamente possuir um Fornecedor vinculado!"

        produto_editado = Produto(codigo=codigo, nome=nome, preco=preco, quantidade_atual=qtd_atual, 
                                  quantidade_minima=qtd_minima, categoria=categoria, descricao=descricao, fornecedor=fornecedor_obj)

        sucesso = self.produto_dao.atualizar(produto_editado)
        if sucesso:
            return True, "Produto atualizado com sucesso!"
        return False, "Erro ao atualizar produto."

    def excluir_produto(self, codigo: int) -> tuple[bool, str]:
        sucesso = self.produto_dao.excluir(codigo)
        if sucesso:
            return True, "Produto removido com sucesso!"
        return False, "Erro ao remover produto."

    def listar_produtos(self) -> list:
        return self.produto_dao.listar()

    def filtrar_produtos(self, nome_parcial: str = "", codigo_fornecedor: int = None) -> list:
        """R.F. 11: Filtra produtos por busca parcial de nome ou por fornecedor."""
        todos = self.produto_dao.listar()
        filtrados = []

        for p in todos:
            # Transforma em letras minúsculas para ignorar diferenças de caixa alta/baixa
            valido_nome = nome_parcial.lower() in p.nome.lower() if nome_parcial else True
            valido_forn = p.fornecedor.codigo == codigo_fornecedor if codigo_fornecedor else True

            if valido_nome and valido_forn:
                filtrados.append(p)
                
        return filtrados
