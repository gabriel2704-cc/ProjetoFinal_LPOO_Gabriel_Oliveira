import psycopg2 

class ConexaoBD:
    def __init__(self):
        # Parâmetros de configuração do seu banco de dados PostgreSQL
        self.host = "localhost"
        self.database = "lpoo_projeto_Gabriel_Oliveira"
        self.usuario = "postgres"
        self.senha = "postgres" 
        self._conexao = None

    def conectar(self):
        """Abre e retorna uma conexão válida com o banco de dados."""
        try:
            if self._conexao is None or self._conexao.closed:
                self._conexao = psycopg2.connect(
                    host=self.host,
                    database=self.database,
                    user=self.usuario,
                    password=self.senha
                )
            return self._conexao
        except Exception as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
            return None

    def desconectar(self):
        """Fecha a conexão atual se ela estiver aberta."""
        if self._conexao and not self._conexao.closed:
            self._conexao.close()