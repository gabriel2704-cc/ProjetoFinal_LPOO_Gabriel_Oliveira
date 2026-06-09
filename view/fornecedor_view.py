from dao.conexao import ConexaoBD
import tkinter as tk
from tkinter import ttk, messagebox
from controller.fornecedor_controller import FornecedorController

class FornecedorView(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Gerenciamento de Fornecedores")
        self.geometry("750x450")
        self.controller = FornecedorController()
        
        # Elementos de Entrada (Campos de Texto)
        self.txt_codigo = tk.StringVar()
        self.txt_nome = tk.StringVar()
        self.txt_cnpj = tk.StringVar()
        self.txt_email = tk.StringVar()
        self.txt_telefone = tk.StringVar()
        self.status_var = tk.BooleanVar(value=True)

        self._criar_componentes()
        self._atualizar_tabela()

    def _criar_componentes(self):
        # Painel do Formulário
        frame_form = ttk.LabelFrame(self, text=" Dados do Fornecedor ")
        frame_form.pack(fill="x", padx=10, pady=5)

        ttk.Label(frame_form, text="Código:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(frame_form, textvariable=self.txt_codigo, state="readonly", width=10).grid(row=0, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(frame_form, text="Nome:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        ttk.Entry(frame_form, textvariable=self.txt_nome, width=40).grid(row=0, column=3, padx=5, pady=5, sticky="w")

        ttk.Label(frame_form, text="CNPJ:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(frame_form, textvariable=self.txt_cnpj, width=20).grid(row=1, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(frame_form, text="E-mail:").grid(row=1, column=2, padx=5, pady=5, sticky="w")
        ttk.Entry(frame_form, textvariable=self.txt_email, width=40).grid(row=1, column=3, padx=5, pady=5, sticky="w")

        ttk.Label(frame_form, text="Telefone:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(frame_form, textvariable=self.txt_telefone, width=20).grid(row=2, column=1, padx=5, pady=5, sticky="w")

        ttk.Checkbutton(frame_form, text="Ativo", variable=self.status_var).grid(row=2, column=3, padx=5, pady=5, sticky="w")

        # Painel de Botões
        frame_botoes = ttk.Frame(self)
        frame_botoes.pack(fill="x", padx=10, pady=5)

        ttk.Button(frame_botoes, text="Salvar Novo", command=self._cadastrar).pack(side="left", padx=5)
        ttk.Button(frame_botoes, text="Salvar Edição", command=self._editar).pack(side="left", padx=5)
        ttk.Button(frame_botoes, text="Excluir", command=self._excluir).pack(side="left", padx=5)
        ttk.Button(frame_botoes, text="Limpar Campos", command=self._limpar_campos).pack(side="left", padx=5)

        # Tabela para Exibição
        self.tabela = ttk.Treeview(self, columns=("id", "nome", "cnpj", "email", "status"), show="headings")
        self.tabela.heading("id", text="Cód.")
        self.tabela.heading("nome", text="Nome")
        self.tabela.heading("cnpj", text="CNPJ")
        self.tabela.heading("email", text="E-mail")
        self.tabela.heading("status", text="Status")
        
        self.tabela.column("id", width=50)
        self.tabela.column("nome", width=250)
        self.tabela.column("cnpj", width=140)
        self.tabela.column("email", width=180)
        self.tabela.column("status", width=80)
        self.tabela.pack(fill="both", expand=True, padx=10, pady=5)
        self.tabela.bind("<<TreeviewSelect>>", self._carregar_campos_selecionados)

    def _atualizar_tabela(self):
        for i in self.tabela.get_children():
            self.tabela.delete(i)
        for f in self.controller.listar_fornecedores():
            status_txt = "Ativo" if f.status else "Inativo"
            self.tabela.insert("", "end", values=(f.codigo, f.nome, f.cnpj, f.email, status_txt))

    def _cadastrar(self):
        sucesso, msg = self.controller.cadastrar_fornecedor(
            self.txt_nome.get(), self.txt_cnpj.get(), self.txt_email.get(), self.txt_telefone.get(), self.status_var.get()
        )
        if sucesso:
            messagebox.showinfo("Sucesso", msg)
            self._limpar_campos()
            self._atualizar_tabela()
        else:
            messagebox.showerror("Erro", msg)

    def _editar(self):
        if not self.txt_codigo.get():
            messagebox.showwarning("Aviso", "Selecione um fornecedor na lista para editar.")
            return
        sucesso, msg = self.controller.atualizar_fornecedor(
            int(self.txt_codigo.get()), self.txt_nome.get(), self.txt_cnpj.get(), self.txt_email.get(), self.txt_telefone.get(), self.status_var.get()
        )
        if sucesso:
            messagebox.showinfo("Sucesso", msg)
            self._limpar_campos()
            self._atualizar_tabela()
        else:
            messagebox.showerror("Erro", msg)

    def _excluir(self):
        if not self.txt_codigo.get():
            messagebox.showwarning("Aviso", "Selecione um fornecedor na lista para excluir.")
            return
        # R.N.F. 1: Pedir confirmação antes de apagar qualquer dado
        if messagebox.askyesno("Confirmar Exclusão", "Deseja realmente apagar este fornecedor?"):
            sucesso, msg = self.controller.excluir_fornecedor(int(self.txt_codigo.get()))
            if sucesso:
                messagebox.showinfo("Sucesso", msg)
                self._limpar_campos()
                self._atualizar_tabela()
            else:
                messagebox.showerror("Erro", msg)

    def _carregar_campos_selecionados(self, event):
        item = self.tabela.selection()
        if item:
            valores = self.tabela.item(item, "values")
            self.txt_codigo.set(valores[0])
            self.txt_nome.set(valores[1])
            self.txt_cnpj.set(valores[2])
            self.txt_email.set(valores[3])
            
            # Busca o telefone direto do banco para preencher, pois ele não aparece na árvore principal
            forn = self.controller.fornecedor_dao.buscar_por_id(int(valores[0]))
            if forn:
                self.txt_telefone.set(forn.telefone)
                self.status_var.set(forn.status)

    def _limpar_campos(self):
        self.txt_codigo.set("")
        self.txt_nome.set("")
        self.txt_cnpj.set("")
        self.txt_email.set("")
        self.txt_telefone.set("")
        self.status_var.set(True)