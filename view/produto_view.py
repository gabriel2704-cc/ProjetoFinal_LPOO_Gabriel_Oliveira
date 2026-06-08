import tkinter as tk
from tkinter import ttk, messagebox
from controller.produto_controller import ProdutoController
from controller.fornecedor_controller import FornecedorController

class ProdutoView(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Gerenciamento de Produtos")
        self.geometry("800 roundedx480")
        self.controller = ProdutoController()
        self.forn_controller = FornecedorController()
        
        self.txt_codigo = tk.StringVar()
        self.txt_nome = tk.StringVar()
        self.txt_preco = tk.StringVar()
        self.txt_qtd_atual = tk.StringVar()
        self.txt_qtd_minima = tk.StringVar(value="5")
        self.txt_categoria = tk.StringVar()
        
        self.lista_fornecedores_banco = []

        self._criar_componentes()
        self._carregar_combobox()
        self._atualizar_tabela()

    def _criar_componentes(self):
        frame_form = ttk.LabelFrame(self, text=" Dados do Produto ")
        frame_form.pack(fill="x", padx=10, pady=5)

        ttk.Label(frame_form, text="Código:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(frame_form, textvariable=self.txt_codigo, state="readonly", width=10).grid(row=0, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(frame_form, text="Nome:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        ttk.Entry(frame_form, textvariable=self.txt_nome, width=35).grid(row=0, column=3, padx=5, pady=5, sticky="w")

        ttk.Label(frame_form, text="Preço (R$):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(frame_form, textvariable=self.txt_preco, width=15).grid(row=1, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(frame_form, text="Categoria:").grid(row=1, column=2, padx=5, pady=5, sticky="w")
        ttk.Entry(frame_form, textvariable=self.txt_categoria, width=35).grid(row=1, column=3, padx=5, pady=5, sticky="w")

        ttk.Label(frame_form, text="Qtd Atual:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(frame_form, textvariable=self.txt_qtd_atual, width=15).grid(row=2, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(frame_form, text="Qtd Mínima:").grid(row=2, column=2, padx=5, pady=5, sticky="w")
        ttk.Entry(frame_form, textvariable=self.txt_qtd_minima, width=15).grid(row=2, column=3, padx=5, pady=5, sticky="w")

        ttk.Label(frame_form, text="Fornecedor:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.combo_fornecedor = ttk.Combobox(frame_form, state="readonly", width=32)
        self.combo_fornecedor.grid(row=3, column=1, columnspan=3, padx=5, pady=5, sticky="w")

        # Filtros (R.F. 11)
        frame_filtros = ttk.LabelFrame(self, text=" Filtros de Busca ")
        frame_filtros.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(frame_filtros, text="Filtrar por Nome:").pack(side="left", padx=5, pady=5)
        self.ent_busca_nome = ttk.Entry(frame_filtros, width=25)
        self.ent_busca_nome.pack(side="left", padx=5, pady=5)
        self.ent_busca_nome.bind("<KeyRelease>", lambda event: self._filtrar())

        frame_botoes = ttk.Frame(self)
        frame_botoes.pack(fill="x", padx=10, pady=5)

        ttk.Button(frame_botoes, text="Salvar Novo", command=self._cadastrar).pack(side="left", padx=5)
        ttk.Button(frame_botoes, text="Salvar Edição", command=self._editar).pack(side="left", padx=5)
        ttk.Button(frame_botoes, text="Excluir", command=self._excluir).pack(side="left", padx=5)

        self.tabela = ttk.Treeview(self, columns=("id", "nome", "preco", "qtd", "qtd_min", "fornecedor"), show="headings")
        self.tabela.heading("id", text="Cód.")
        self.tabela.heading("nome", text="Nome Produto")
        self.tabela.heading("preco", text="Preço")
        self.tabela.heading("qtd", text="Estoque")
        self.tabela.heading("qtd_min", text="Estoque Mín.")
        self.tabela.heading("fornecedor", text="Fornecedor")
        
        self.tabela.column("id", width=50)
        self.tabela.column("nome", width=220)
        self.tabela.column("preco", width=80)
        self.tabela.column("qtd", width=80)
        self.tabela.column("qtd_min", width=90)
        self.tabela.column("fornecedor", width=180)
        self.tabela.pack(fill="both", expand=True, padx=10, pady=5)
        self.tabela.bind("<<TreeviewSelect>>", self._carregar_campos_selecionados)

    def _carregar_combobox(self):
        self.lista_fornecedores_banco = self.forn_controller.listar_fornecedores()
        nomes = [f"{f.codigo} - {f.nome}" for f in self.lista_fornecedores_banco if f.status]
        self.combo_fornecedor['values'] = nomes

    def _atualizar_tabela(self, lista_customizada=None):
        for i in self.tabela.get_children():
            self.tabela.delete(i)
        
        produtos = lista_customizada if lista_customizada is not None else self.controller.listar_produtos()
        for p in produtos:
            forn_nome = p.fornecedor.nome if p.fornecedor else "Não associado"
            self.tabela.insert("", "end", values=(p.codigo, p.nome, f"R$ {p.preco:.2f}", p.quantidade_atual, p.quantidade_minima, forn_nome))

    def _filtrar(self):
        termo = self.ent_busca_nome.get()
        produtos_filtrados = self.controller.filtrar_produtos(nome_parcial=termo)
        self._atualizar_tabela(produtos_filtrados)

    def _obter_fornecedor_selecionado(self):
        index = self.combo_fornecedor.current()
        if index != -1:
            return self.lista_fornecedores_banco[index]
        return None

    def _cadastrar(self):
        try:
            sucesso, msg = self.controller.cadastrar_produto(
                self.txt_nome.get(), float(self.txt_preco.get()), int(self.txt_qtd_atual.get()),
                int(self.txt_qtd_minima.get()), self.txt_categoria.get(), self._obter_fornecedor_selecionado()
            )
            if sucesso:
                messagebox.showinfo("Sucesso", msg)
                self._atualizar_tabela()
            else:
                messagebox.showerror("Erro", msg)
        except ValueError:
            messagebox.showerror("Erro", "Preço e Quantidades devem ser numéricos!")

    def _editar(self):
        if not self.txt_codigo.get(): return
        try:
            sucesso, msg = self.controller.atualizar_produto(
                int(self.txt_codigo.get()), self.txt_nome.get(), float(self.txt_preco.get()),
                int(self.txt_qtd_atual.get()), int(self.txt_qtd_minima.get()), self.txt_categoria.get(), self._obter_fornecedor_selecionado()
            )
            if sucesso:
                messagebox.showinfo("Sucesso", msg)
                self._atualizar_tabela()
        except ValueError:
            messagebox.showerror("Erro", "Campos numéricos inválidos.")

    def _excluir(self):
        if not self.txt_codigo.get(): return
        if messagebox.askyesno("Confirmação", "Excluir este produto?"):
            sucesso, msg = self.controller.excluir_produto(int(self.txt_codigo.get()))
            if sucesso:
                self._atualizar_tabela()

    def _carregar_campos_selecionados(self, event):
        item = self.tabela.selection()
        if item:
            valores = self.tabela.item(item, "values")
            self.txt_codigo.set(valores[0])
            self.txt_nome.set(valores[1])
            self.txt_preco.set(valores[2].replace("R$ ", ""))
            self.txt_qtd_atual.set(valores[3])
            self.txt_qtd_minima.set(valores[4])
            
            prod = self.controller.produto_dao.buscar_por_id(int(valores[0]))
            if prod and prod.fornecedor:
                self.txt_categoria.set(prod.categoria)
                for i, f in enumerate(self.lista_fornecedores_banco):
                    if f.codigo == prod.fornecedor.codigo:
                        self.combo_fornecedor.current(i)
                        break