from dao.conexao import ConexaoBD
from dao.fornecedor_dao import FornecedorDAO
from model.fornecedor import Fornecedor

class FornecedorController:
    def __init__(self):
        self.fornecedor_dao = FornecedorDAO()

    def cadastrar_fornecedor(self, nome: str, cnpj: str, email: str, telefone: str, status: bool) -> tuple[bool, str]:
        """Cria e valida um novo fornecedor. Retorna (Sucesso, Mensagem)."""
        # Cria a instância com os dados recebidos da View
        novo_fornecedor = Fornecedor(nome=nome, cnpj=cnpj, email=email, telefone=telefone, status=status)

        # 1. R.F. 2: Validação de Formato do CNPJ
        if not novo_fornecedor.validar_cnpj():
            return False, "Formato de CNPJ inválido! Use o padrão: XX.XXX.XXX/XXXX-XX"

        # 2. R.N. 1: Validação de Unicidade de CNPJ
        todos = self.fornecedor_dao.listar()
        for f in todos:
            if f.cnpj == cnpj:
                return False, "Erro: Já existe um fornecedor cadastrado com este CNPJ!"

        # 3. Persistência
        sucesso = self.fornecedor_dao.salvar(novo_fornecedor)
        if sucesso:
            return True, "Fornecedor cadastrado com sucesso!"
        return False, "Erro interno ao salvar no banco de dados."

    def atualizar_fornecedor(self, codigo: int, nome: str, cnpj: str, email: str, telefone: str, status: bool) -> tuple[bool, str]:
        """Atualiza um fornecedor existente verificando as regras lógicas."""
        fornecedor_editado = Fornecedor(codigo=codigo, nome=nome, cnpj=cnpj, email=email, telefone=telefone, status=status)

        if not fornecedor_editado.validar_cnpj():
            return False, "Formato de CNPJ inválido!"

        # Verifica se alterou o CNPJ para um que já pertence a outro fornecedor
        todos = self.fornecedor_dao.listar()
        for f in todos:
            if f.cnpj == cnpj and f.codigo != codigo:
                return False, "Erro: Este CNPJ já está sendo usado por outro fornecedor!"

        sucesso = self.fornecedor_dao.atualizar(fornecedor_editado)
        if sucesso:
            return True, "Fornecedor atualizado com sucesso!"
        return False, "Erro ao atualizar dados do fornecedor."

    def excluir_fornecedor(self, codigo: int) -> tuple[bool, str]:
        """R.N. 2: Impede a exclusão se houver produtos vinculados, informando a quantidade."""
        total_vinculados = self.fornecedor_dao.contar_produtos_vinculados(codigo)
        if total_vinculados > 0:
            return False, f"Não é possível excluir! Existem {total_vinculados} produto(s) vinculado(s) a este fornecedor."

        sucesso = self.fornecedor_dao.excluir(codigo)
        if sucesso:
            return True, "Fornecedor removido com sucesso!"
        return False, "Erro interno ao excluir fornecedor."

    def listar_fornecedores(self) -> list[Fornecedor]:
        return self.fornecedor_dao.listar()

    def filtrar_fornecedores(self, termo: str = "") -> list[Fornecedor]:
        """R.F. 12: Filtra fornecedores por nome ou CNPJ (busca parcial)."""
        todos = self.fornecedor_dao.listar()
        if not termo:
            return todos

        termo_lower = termo.lower()
        return [f for f in todos if termo_lower in f.nome.lower() or termo_lower in f.cnpj.lower()]