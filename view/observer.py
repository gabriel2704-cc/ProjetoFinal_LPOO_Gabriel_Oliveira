import datetime
from tkinter import messagebox
from model.interfaces import Observer

class AlertaEstoqueObserver(Observer):
    def __init__(self):
        self.log_filename = "estoque_critico.log"

    def atualizar(self, produto) -> None:
        """Método disparado automaticamente pelo padrão Observer (R.N. 4)."""
        # 1. R.F. 8: Alerta Visual em Tela (Popup)
        mensagem_popup = (
            f"⚠️ ALERTA DE ESTOQUE CRÍTICO! ⚠️\n\n"
            f"O produto '{produto.nome}' atingiu o nível de segurança!\n"
            f"Quantidade Atual: {produto.quantidade_atual}\n"
            f"Quantidade Mínima Configurada: {produto.quantidade_minima}"
        )
        messagebox.showwarning("Aviso de Estoque", mensagem_popup)

        # 2. R.F. 9: Gerar arquivo físico de Log (.log)
        data_hora_atual = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        linha_log = (
            f"[{data_hora_atual}] PRODUTO CRÍTICO: {produto.nome} (Código: {produto.codigo}) | "
            f"Qtd Atual: {produto.quantidade_atual} | Qtd Mínima: {produto.quantidade_minima}\n"
        )
        
        try:
            # Abre o arquivo em modo 'append' (anexa texto ao final sem apagar o anterior)
            with open(self.log_filename, "a", encoding="utf-8") as arquivo_log:
                arquivo_log.write(linha_log)
        except Exception as e:
            print(f"Falha ao escrever no arquivo de log: {e}")