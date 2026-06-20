-- =====================================================================
-- Script de criação do banco - Sistema de Controle de Estoque e Fornecedores
-- =====================================================================

CREATE TABLE fornecedores (
    codigo SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cnpj VARCHAR(18) NOT NULL UNIQUE,
    telefone VARCHAR(15),
    email VARCHAR(100),
    status BOOLEAN DEFAULT TRUE
);

CREATE TABLE produtos (
    codigo SERIAL PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    preco DECIMAL(10,2) NOT NULL,
    quantidade_atual INTEGER DEFAULT 0,
    quantidade_minima INTEGER DEFAULT 5,
    categoria VARCHAR(50),
    descricao TEXT,
    fornecedor_codigo INTEGER NOT NULL,
    FOREIGN KEY (fornecedor_codigo) REFERENCES fornecedores(codigo) ON DELETE RESTRICT
);

CREATE TABLE movimentos (
    codigo SERIAL PRIMARY KEY,
    tipo VARCHAR(7) NOT NULL,
    quantidade INTEGER NOT NULL,
    data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Gerado automaticamente
    observacao TEXT, 
    produto_codigo INTEGER NOT NULL, 
    FOREIGN KEY (produto_codigo) REFERENCES produtos(codigo) ON DELETE CASCADE,
    CONSTRAINT chk_tipo_movimento CHECK (tipo IN ('ENTRADA', 'SAIDA'))
);


