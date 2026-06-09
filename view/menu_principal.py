import tkinter as tk
from tkinter import ttk, messagebox
from view.fornecedor_view import FornecedorView
from view.produto_view import ProdutoView
from view.movimentacao_view import MovimentacaoView

class MenuPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Controle de Estoque e Fornecedores")
        self.geometry("600x350")
        
        # Centralização da janela na tela principal
        self.eval('tk::PlaceWindow . center')
        
        self._criar_menu_superior()
        self._criar_corpo_boas_vindas()

    def _criar_menu_superior(self):
        barra_menus = tk.Menu(self)

        # Menu Cadastros
        menu_cadastros = tk.Menu(barra_menus, tearoff=0)
        menu_cadastros.add_command(label="Fornecedores", command=self._abrir_fornecedores)
        menu_cadastros.add_command(label="Produtos", command=self._abrir_produtos)
        menu_cadastros.add_command(label="Sair", command=self.quit)
        barra_menus.add_cascade(label="Cadastros", menu=menu_cadastros)

        # Menu Operações
        menu_operacoes = tk.Menu(barra_menus, tearoff=0)
        menu_operacoes.add_command(label="Movimentações de Estoque", command=self._abrir_movimentacoes)
        barra_menus.add_cascade(label="Estoque", menu=menu_operacoes)

        # Menu Ajuda
        menu_ajuda = tk.Menu(barra_menus, tearoff=0)
        menu_ajuda.add_command(label="Sobre o Sistema", command=self._exibir_tela_sobre)
        barra_menus.add_cascade(label="Ajuda", menu=menu_ajuda)

        self.config(menu=barra_menus)

    def _criar_corpo_boas_vindas(self):
        lbl_titulo = ttk.Label(self, text="Controle de Estoque Desktop", font=("Arial", 16, "bold"))
        lbl_titulo.pack(pady=40)

        lbl_desc = ttk.Label(
            self, 
            text="Utilize a barra de menus superior para navegar\nentre os módulos de cadastro e movimentação física.",
            justify="center", font=("Arial", 11)
        )
        lbl_desc.pack(pady=10)

    def _abrir_fornecedores(self):
        FornecedorView(self)

    def _abrir_produtos(self):
        ProdutoView(self)

    def _abrir_movimentacoes(self):
        MovimentacaoView(self)

    def _exibir_tela_sobre(self):
        """R.F. 13: Exibe metadados de autoria da APS e LPOO."""
        dados_sobre = (
            "📦 Sistema de Controle de Estoque e Fornecedores\n\n"
            "Descrição: Aplicação desktop offline para gerenciamento de insumos.\n"
            "Responsável: Gabriel de Oliveira\n"
            "Disciplina: Análise e Projeto de Sistemas (APS) +\n"
            "            Linguagem e Programação Orientada a Objetos (LPOO)\n"
            "Curso: Bacharelado em Ciência da Computação\n"
            "Semestre/Ano: 1º Semestre / 2026"
        )
        messagebox.showinfo("Sobre o Projeto", dados_sobre)