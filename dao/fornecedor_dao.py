from dao.conexao import ConexaoBD
from model.fornecedor import Fornecedor


class FornecedorDAO:
    def __init__(self):
        self.db = ConexaoBD()

    def salvar(self, fornecedor: Fornecedor) -> bool:
        """Insere um novo fornecedor no banco de dados."""
        conexao = self.db.conectar()
        if not conexao: return False
        
        sql = """INSERT INTO fornecedores (nome, cnpj, telefone, email, status) 
                 VALUES (%s, %s, %s, %s, %s) RETURNING codigo;"""
        try:
            cursor = conexao.cursor()
            cursor.execute(sql, (fornecedor.nome, fornecedor.cnpj, fornecedor.telefone, fornecedor.email, fornecedor.status))
            # Captura o ID gerado pelo SERIAL e atribui de volta ao objeto
            fornecedor.codigo = cursor.fetchone()[0]
            conexao.commit()
            cursor.close()
            return True
        except Exception as e:
            conexao.rollback()
            print(f"Erro ao salvar fornecedor: {e}")
            return False
        finally:
            self.db.desconectar()

    def atualizar(self, fornecedor: Fornecedor) -> bool:
        """Atualiza os dados de um fornecedor existente."""
        conexao = self.db.conectar()
        if not conexao: return False

        sql = """UPDATE fornecedores SET nome=%s, cnpj=%s, telefone=%s, email=%s, status=%s 
                 WHERE codigo=%s;"""
        try:
            cursor = conexao.cursor()
            cursor.execute(sql, (fornecedor.nome, fornecedor.cnpj, fornecedor.telefone, fornecedor.email, fornecedor.status, fornecedor.codigo))
            conexao.commit()
            cursor.close()
            return True
        except Exception as e:
            conexao.rollback()
            print(f"Erro ao atualizar fornecedor: {e}")
            return False
        finally:
            self.db.desconectar()

    def excluir(self, codigo: int) -> bool:
        """Exclui um fornecedor. Retorna False se violar a restrição ON DELETE RESTRICT (R.N. 2)."""
        conexao = self.db.conectar()
        if not conexao: return False

        sql = "DELETE FROM fornecedores WHERE codigo = %s;"
        try:
            cursor = conexao.cursor()
            cursor.execute(sql, (codigo,))
            conexao.commit()
            cursor.close()
            return True
        except Exception as e:
            conexao.rollback()
            # Esse print capturará o erro caso haja um produto associado a este fornecedor
            print(f"Erro ao excluir fornecedor (pode haver produtos vinculados): {e}")
            return False
        finally:
            self.db.desconectar()

    def listar(self) -> list:
        """Retorna uma lista de objetos do tipo Fornecedor."""
        conexao = self.db.conectar()
        lista_fornecedores = []
        if not conexao: return lista_fornecedores

        sql = "SELECT codigo, nome, cnpj, email, telefone, status FROM fornecedores ORDER BY nome;"
        try:
            cursor = conexao.cursor()
            cursor.execute(sql)
            resultados = cursor.fetchall()
            for linha in resultados:
                # Transforma a tupla do banco de volta em um objeto do pacote Model
                f = Fornecedor(codigo=linha[0], nome=linha[1], cnpj=linha[2], email=linha[3], telefone=linha[4], status=linha[5])
                lista_fornecedores.append(f)
            cursor.close()
        except Exception as e:
            print(f"Erro ao listar fornecedores: {e}")
        finally:
            self.db.desconectar()
        return lista_fornecedores

    def contar_produtos_vinculados(self, codigo: int) -> int:
        """Conta quantos produtos estão vinculados a este fornecedor (usado na R.N. 2)."""
        conexao = self.db.conectar()
        if not conexao: return 0

        sql = "SELECT COUNT(*) FROM produtos WHERE fornecedor_codigo = %s;"
        try:
            cursor = conexao.cursor()
            cursor.execute(sql, (codigo,))
            total = cursor.fetchone()[0]
            cursor.close()
            return total
        except Exception as e:
            print(f"Erro ao contar produtos vinculados: {e}")
            return 0
        finally:
            self.db.desconectar()

    def buscar_por_id(self, codigo: int) -> Fornecedor:
        """Busca um fornecedor específico pelo seu código."""
        conexao = self.db.conectar()
        if not conexao: return None

        sql = "SELECT codigo, nome, cnpj, email, telefone, status FROM fornecedores WHERE codigo = %s;"
        try:
            cursor = conexao.cursor()
            cursor.execute(sql, (codigo,))
            linha = cursor.fetchone()
            cursor.close()
            if linha:
                return Fornecedor(codigo=linha[0], nome=linha[1], cnpj=linha[2], email=linha[3], telefone=linha[4], status=linha[5])
        except Exception as e:
            print(f"Erro ao buscar fornecedor: {e}")
        finally:
            self.db.desconectar()
        return None