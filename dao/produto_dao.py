from dao.conexao import ConexaoBD
from dao.fornecedor_dao import FornecedorDAO
from model.produto import Produto

class ProdutoDAO:
    def __init__(self):
        self.db = ConexaoBD()
        self.fornecedor_dao = FornecedorDAO() # Usado para recompor a associação

    def salvar(self, produto: Produto) -> bool:
        conexao = self.db.conectar()
        if not conexao: return False

        sql = """INSERT INTO produtos (nome, preco, quantidade_atual, quantidade_minima, categoria, descricao, fornecedor_codigo) 
                 VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING codigo;"""
        try:
            cursor = conexao.cursor()
            cursor.execute(sql, (produto.nome, produto.preco, produto.quantidade_atual, 
                                 produto.quantidade_minima, produto.categoria, produto.descricao, produto.fornecedor.codigo))
            produto.codigo = cursor.fetchone()[0]
            conexao.commit()
            cursor.close()
            return True
        except Exception as e:
            conexao.rollback()
            print(f"Erro ao salvar produto: {e}")
            return False
        finally:
            self.db.desconectar()

    def atualizar(self, produto: Produto) -> bool:
        conexao = self.db.conectar()
        if not conexao: return False

        sql = """UPDATE produtos SET nome=%s, preco=%s, quantidade_atual=%s, quantidade_minima=%s, 
                 categoria=%s, descricao=%s, fornecedor_codigo=%s WHERE codigo=%s;"""
        try:
            cursor = conexao.cursor()
            cursor.execute(sql, (produto.nome, produto.preco, produto.quantidade_atual, 
                                 produto.quantidade_minima, produto.categoria, produto.descricao, 
                                 produto.fornecedor.codigo, produto.codigo))
            conexao.commit()
            cursor.close()
            return True
        except Exception as e:
            conexao.rollback()
            print(f"Erro ao atualizar produto: {e}")
            return False
        finally:
            self.db.desconectar()

    def excluir(self, codigo: int) -> bool:
        conexao = self.db.conectar()
        if not conexao: return False

        sql = "DELETE FROM produtos WHERE codigo = %s;"
        try:
            cursor = conexao.cursor()
            cursor.execute(sql, (codigo,))
            conexao.commit()
            cursor.close()
            return True
        except Exception as e:
            conexao.rollback()
            print(f"Erro ao excluir produto: {e}")
            return False
        finally:
            self.db.desconectar()

    def listar(self) -> list:
        conexao = self.db.conectar()
        lista_produtos = []
        if not conexao: return lista_produtos

        sql = "SELECT codigo, nome, preco, quantidade_atual, quantidade_minima, categoria, descricao, fornecedor_codigo FROM produtos;"
        try:
            cursor = conexao.cursor()
            cursor.execute(sql)
            resultados = cursor.fetchall()
            cursor.close()
            
            for linha in resultados:
                # Busca o objeto Fornecedor completo associado a este produto
                fornecedor_obj = self.fornecedor_dao.buscar_por_id(linha[7])
                
                p = Produto(codigo=linha[0], nome=linha[1], preco=linha[2], quantidade_atual=linha[3], 
                            quantidade_minima=linha[4], categoria=linha[5], descricao=linha[6], fornecedor=fornecedor_obj)
                lista_produtos.append(p)
        except Exception as e:
            print(f"Erro ao listar produtos: {e}")
        finally:
            self.db.desconectar()
        return lista_produtos

    def buscar_por_id(self, codigo: int) -> Produto:
        conexao = self.db.conectar()
        if not conexao: return None

        sql = "SELECT codigo, nome, preco, quantidade_atual, quantidade_minima, categoria, descricao, fornecedor_codigo FROM produtos WHERE codigo = %s;"
        try:
            cursor = conexao.cursor()
            cursor.execute(sql, (codigo,))
            linha = cursor.fetchone()
            cursor.close()
            if linha:
                fornecedor_obj = self.fornecedor_dao.buscar_por_id(linha[7])
                return Produto(codigo=linha[0], nome=linha[1], preco=linha[2], quantidade_atual=linha[3], 
                               quantidade_minima=linha[4], categoria=linha[5], descricao=linha[6], fornecedor=fornecedor_obj)
        except Exception as e:
            print(f"Erro ao buscar produto: {e}")
        finally:
            self.db.desconectar()
        return None
