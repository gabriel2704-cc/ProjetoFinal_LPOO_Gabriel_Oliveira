import tkinter as tk
from tkinter import ttk, messagebox
from controller.estoque_controller import EstoqueController
from controller.produto_controller import ProdutoController
from view.observer import AlertaEstoqueObserver

class MovimentacaoView(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Movimentação de Estoque")
        self.geometry("750x450")
        self.estoque_controller = EstoqueController()
        self.produto_controller = ProdutoController()
        self.alerta_observer = AlertaEstoqueObserver() # Nosso Observer físico e visual

        self.lbl_info_produto = tk.StringVar(value="Selecione um produto abaixo...")
        self.txt_quantidade = tk.StringVar()
        self.txt_observacao = tk.StringVar()
        self.produto_selecionado_id = None

        self._criar_componentes()
        self._atualizar_tabela_produtos()

    def _criar_componentes(self):
        # Painel Superior (Execução da Movimentação)
        frame_op = ttk.LabelFrame(self, text=" Registrar Entrada / Saída ")
        frame_op.pack(fill="x", padx=10, pady=5)

        ttk.Label(frame_op, textvariable=self.lbl_info_produto, font=("Arial", 10, "bold")).grid(row=0, column=0, columnspan=4, padx=5, pady=5, sticky="w")

        ttk.Label(frame_op, text="Quantidade:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(frame_op, textvariable=self.txt_quantidade, width=15).grid(row=1, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(frame_op, text="Observação:").grid(row=1, column=2, padx=5, pady=5, sticky="w")
        ttk.Entry(frame_op, textvariable=self.txt_observacao, width=35).grid(row=1, column=3, padx=5, pady=5, sticky="w")

        frame_acoes = ttk.Frame(frame_op)
        frame_acoes.grid(row=2, column=0, columnspan=4, pady=10)
        
        ttk.Button(frame_acoes, text="📥 Registrar Entrada", command=self._registrar_entrada).pack(side="left", padx=10)
        ttk.Button(frame_acoes, text="📤 Registrar Saída", command=self._registrar_saida).pack(side="left", padx=10)
        ttk.Button(frame_acoes, text="📜 Ver Histórico", command=self._exibir_historico).pack(side="left", padx=10)

        # Painel Inferior (Seleção do Produto)
        ttk.Label(self, text="Selecione o Produto Alvo:").pack(anchor="w", padx=10, pady=2)
        self.tabela_prod = ttk.Treeview(self, columns=("id", "nome", "qtd_disp", "qtd_min"), show="headings", height=8)
        self.tabela_prod.heading("id", text="Cód.")
        self.tabela_prod.heading("nome", text="Nome do Produto")
        self.tabela_prod.heading("qtd_disp", text="Estoque Disponível")
        self.tabela_prod.heading("qtd_min", text="Nível Mínimo")
        self.tabela_prod.pack(fill="both", expand=True, padx=10, pady=5)
        self.tabela_prod.bind("<<TreeviewSelect>>", self._selecionar_produto)

    def _atualizar_tabela_produtos(self):
        for i in self.tabela_prod.get_children():
            self.tabela_prod.delete(i)
        for p in self.produto_controller.listar_produtos():
            self.tabela_prod.insert("", "end", values=(p.codigo, p.nome, p.quantidade_atual, p.quantidade_minima))

    def _selecionar_produto(self, event):
        item = self.tabela_prod.selection()
        if item:
            valores = self.tabela_prod.item(item, "values")
            self.produto_selecionado_id = int(valores[0])
            self.lbl_info_produto.set(f"Produto Ativo: {valores[1]} (Estoque: {valores[2]})")

    def _registrar_entrada(self):
        if not self.produto_selecionado_id: return
        try:
            sucesso, msg = self.estoque_controller.registrar_entrada(
                self.produto_selecionado_id, int(self.txt_quantidade.get()), self.txt_observacao.get()
            )
            if sucesso:
                messagebox.showinfo("Entrada", msg)
                self._atualizar_tabela_produtos()
                self.txt_quantidade.set("")
                self.txt_observacao.set("")
            else:
                messagebox.showerror("Erro", msg)
        except ValueError:
            messagebox.showerror("Erro", "Informe uma quantidade inteira válida!")

    def _registrar_saida(self):
        if not self.produto_selecionado_id: return
        try:
            # UC04 & Diagrama de Sequência: Passamos o observer em formato de lista para injeção dinâmica
            sucesso, msg = self.estoque_controller.registrar_saida(
                self.produto_selecionado_id, int(self.txt_quantidade.get()), 
                self.txt_observacao.get(), lista_observers=[self.alerta_observer]
            )
            if sucesso:
                messagebox.showinfo("Saída", msg)
                self._atualizar_tabela_produtos()
                self.txt_quantidade.set("")
                self.txt_observacao.set("")
            else:
                messagebox.showerror("Erro", msg)
        except ValueError:
            messagebox.showerror("Erro", "Informe uma quantidade inteira válida!")

    def _exibir_historico(self):
        """R.F. 10: Abre uma janela contendo o histórico de auditoria cronológico."""
        if not self.produto_selecionado_id: return
        
        janela_hist = tk.Toplevel(self)
        janela_hist.title("Histórico de Movimentações")
        janela_hist.geometry("550x300")
        
        tree_hist = ttk.Treeview(janela_hist, columns=("data", "tipo", "qtd", "obs"), show="headings")
        tree_hist.heading("data", text="Data/Hora")
        tree_hist.heading("tipo", text="Operação")
        tree_hist.heading("qtd", text="Qtd.")
        tree_hist.heading("obs", text="Observação")
        
        tree_hist.column("data", width=130)
        tree_hist.column("tipo", width=80)
        tree_hist.column("qtd", width=50)
        tree_hist.column("obs", width=250)
        tree_hist.pack(fill="both", expand=True, padx=10, pady=10)

        dados = self.estoque_controller.obter_historico(self.produto_selecionado_id)
        for m in dados:
            dt_formatada = m.data_hora.strftime("%d/%m/%Y %H:%M") if m.data_hora else "N/D"
            tree_hist.insert("", "end", values=(dt_formatada, m.tipo, m.quantidade, m.observacao))