from view.menu_principal import MenuPrincipal

def main():
    # Inicializa a janela mestra do sistema (Tkinter)
    app = MenuPrincipal()
    
    # Mantém a aplicação rodando em loop aguardando interações do usuário
    app.mainloop()

if __name__ == "__main__":
    main()