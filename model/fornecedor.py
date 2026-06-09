class Fornecedor:
    def __init__(self, nome, cnpj, email, telefone, status=True, codigo=None):
        self.codigo = codigo  
        self.nome = nome
        self.cnpj = cnpj       # Esperado no formato: XX.XXX.XXX/XXXX-XX
        self.telefone = telefone
        self.email = email
        self.status = status

    def validar_cnpj(self) -> bool:
        # 1. Validação do tamanho com máscara (XX.XXX.XXX/XXXX-XX possui 18 caracteres)
        if len(self.cnpj) != 18:
            return False

        # 2. Validação dos caracteres separadores nas posições exatas
        if (self.cnpj[2] != '.' or 
            self.cnpj[6] != '.' or 
            self.cnpj[10] != '/' or 
            self.cnpj[15] != '-'):
            return False

        # 3. Extração e validação dos dígitos numéricos
        # Vamos fatiar a string removendo as posições dos separadores
        partes_numericas = (
            self.cnpj[0:2] +   # XX
            self.cnpj[3:6] +   # XXX
            self.cnpj[7:10] +  # XXX
            self.cnpj[11:15] + # XXXX
            self.cnpj[16:18]   # XX
        )

        # Verifica se todos os caracteres restantes são de fato números e somam 14 dígitos
        if not partes_numericas.isdigit() or len(partes_numericas) != 14:
            return False

        return True