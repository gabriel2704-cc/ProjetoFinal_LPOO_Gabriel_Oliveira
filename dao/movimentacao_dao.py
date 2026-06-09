from conexao import ConexaoBD
from model.movimentacao import Movimentacao
from produto_dao import ProdutoDAO
from conexao import ConexaoBD
from produto_dao import ProdutoDAO
from dao.conexao import ConexaoBD
from dao.produto_dao import ProdutoDAO

class MovimentacaoDAO:
    def __init__(self):
        self.db = ConexaoBD()
        self.produto_dao = ProdutoDAO()

    def salvar(self, movimentacao: Movimentacao) -> bool:
        """Registra uma entrada ou saída no histórico."""
        conexao = self.db.conectar()
        if not conexao: return False

        # Deixamos o banco gerar o timestamp automaticamente através do default configurado
        sql = """INSERT INTO movimentos (tipo, quantidade, observacao, produto_codigo) 
                 VALUES (%s, %s, %s, %s) RETURNING codigo, data_hora;"""
        try:
            cursor = conexao.cursor()
            cursor.execute(sql, (movimentacao.tipo, movimentacao.quantidade, 
                                 movimentacao.observacao, movimentacao.produto.codigo))
            retorno = cursor.fetchone()
            movimentacao.codigo = retorno[0]
            movimentacao.data_hora = retorno[1] # Atualiza o objeto com o horário gerado pelo Postgres
            conexao.commit()
            cursor.close()
            return True
        except Exception as e:
            conexao.rollback()
            print(f"Erro ao salvar movimentação: {e}")
            return False
        finally:
            self.db.desconectar()

    def listar_por_produto(self, produto_codigo: int) -> list:
        """R.F. 10: Retorna o histórico de movimentações ordenado do mais recente ao mais antigo."""
        conexao = self.db.conectar()
        historico = []
        if not conexao: return historico

        sql = """SELECT codigo, tipo, quantidade, data_hora, observacao 
                 FROM movimentos WHERE produto_codigo = %s ORDER BY data_hora DESC;"""
        try:
            cursor = conexao.cursor()
            cursor.execute(sql, (produto_codigo,))
            resultados = cursor.fetchall()
            cursor.close()

            # Busca o produto uma única vez para associar à lista de movimentações
            produto_obj = self.produto_dao.buscar_por_id(produto_codigo)

            for linha in resultados:
                m = Movimentacao(codigo=linha[0], tipo=linha[1], quantidade=linha[2], 
                                 data_hora=linha[3], observacao=linha[4], produto=produto_obj)
                historico.append(m)
        except Exception as e:
            print(f"Erro ao listar histórico de movimentações: {e}")
        finally:
            self.db.desconectar()
        return historico