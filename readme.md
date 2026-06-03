# Projeto Final LPOO — Sistema de Vendas de Camisetas Esportivas

## 1. Descrição Geral

Este projeto é um sistema desktop desenvolvido em Python para a disciplina de Linguagem de Programação Orientada a Objetos — LPOO.

O sistema tem como objetivo gerenciar vendas de camisetas esportivas, com foco em camisas de seleções. A aplicação permite cadastrar clientes, cadastrar camisetas, registrar vendas e controlar o estoque de forma simples.

O projeto utiliza Programação Orientada a Objetos, interface gráfica, persistência em banco de dados PostgreSQL, padrão DAO e padrão Factory.

## 2. Objetivo Acadêmico

Atender todos os requisitos da Atividade Final de LPOO, incluindo:

* Linguagem Python;
* Uso de Programação Orientada a Objetos;
* Organização em módulos/pacotes;
* Uso de PostgreSQL;
* Implementação do padrão DAO;
* Implementação do padrão Factory;
* Criação de interface gráfica;
* Operações CRUD;
* Relacionamento entre entidades com chave estrangeira;
* Documentação do projeto;
* Diagrama UML;
* Versionamento no GitHub.

## 3. Tecnologias Utilizadas

* Python
* Tkinter
* PostgreSQL
* psycopg2
* Git/GitHub
* Programação Orientada a Objetos
* Padrão DAO
* Padrão Factory

## 4. Estrutura Prevista do Projeto

```text
Sports-Shirts_Sales-System/
│
├── main.py
├── README.md
│
│
├── model/
│   ├── cliente.py
│   ├── camiseta.py
│   └── venda.py
│
├── dao/
|   ├── db_config.py
│   ├── cliente_dao.py
│   ├── camiseta_dao.py
│   └── venda_dao.py
│
├── factory/
│   └── camiseta_factory.py
│
├── controller/
│   ├── cliente_controller.py
│   ├── camiseta_controller.py
│   └── venda_controller.py
│
├── view/
│   ├── menu_view.py
│   ├── cliente_view.py
│   ├── camiseta_view.py
│   ├── venda_view.py
│   └── sobre_view.py
```

## 5. Entidades do Sistema

### 5.1 Cliente

Representa uma pessoa que compra camisetas.

Atributos:

* id
* nome
* cpf
* telefone
* email

Regras básicas:

* nome é obrigatório
* CPF é obrigatório
* email deve conter `@`, se informado.

### 5.2 Camiseta

Representa uma camiseta esportiva de seleção.

Atributos:

* id
* selecao
* modelo
* tamanho
* preco
* estoque
* tipo

Tipos previstos:

* JOGADOR
* RETRO
* TREINO
* TORCEDOR

Regras básicas:

* seleção é obrigatória
* modelo é obrigatório
* tamanho é obrigatório
* preço deve ser maior que zero
* estoque deve ser maior ou igual a zero.

### 5.3 Venda

Representa uma venda simples de uma camiseta para um cliente.

Atributos:

* id
* cliente
* camiseta
* quantidade
* valor_total
* data_venda

Regras básicas:

* quantidade deve ser maior que zero
* não deve ser possível vender quantidade maior que o estoque disponível
* o valor total da venda deve ser calculado por: quantidade × preço da camiseta
* ao registrar uma venda, o estoque da camiseta deve ser reduzido.

## 6. Relacionamentos

O sistema possui os seguintes relacionamentos:

```text
Cliente 1:N Venda
Camiseta 1:N Venda
```

Isso significa que:

* um cliente pode realizar várias vendas;
* uma venda pertence a um único cliente;
* uma camiseta pode estar presente em várias vendas;
* uma venda está relacionada a uma única camiseta.

No banco de dados, a tabela `venda` possui duas chaves estrangeiras:

```text
ID_CLIENTE  → CLIENTE_ID
ID_CAMISETA → CAMISETA_ID
```

Essas chaves estrangeiras garantem o relacionamento obrigatório entre as classes persistidas.

## 7. Script Completo do Banco de Dados

```sql
CREATE DATABASE lpoo_projeto_lucas-teixeira;

CREATE TABLE IF NOT EXISTS tb_cliente (
    ID_CLIENTE SERIAL PRIMARY KEY,
    NOME VARCHAR(100) NOT NULL,
    CPF VARCHAR(14) NOT NULL,
    TELEFONE VARCHAR(20),
    EMAIL VARCHAR(100),

    CONSTRAINT cliente_cpf_unique UNIQUE (CPF)
);

CREATE TABLE IF NOT EXISTS tb_camiseta (
    ID_CAMISETA SERIAL PRIMARY KEY,
    SELECAO VARCHAR(80) NOT NULL,
    MODELO VARCHAR(80) NOT NULL,
    TAMANHO VARCHAR(10) NOT NULL,
    PRECO NUMERIC(10,2) NOT NULL,
    ESTOQUE INTEGER NOT NULL,
    TIPO VARCHAR(30) NOT NULL,

    CONSTRAINT camiseta_tipo_check 
        CHECK (TIPO IN ('JOGADOR', 'TORCEDOR', 'TREINO', 'RETRO'))
);

CREATE TABLE IF NOT EXISTS tb_venda (
    ID_VENDA SERIAL PRIMARY KEY,
    CLIENTE_ID INTEGER NOT NULL,
    CAMISETA_ID INTEGER NOT NULL,
    QUANTIDADE INTEGER NOT NULL,
    VLTOTAL NUMERIC(10,2) NOT NULL,
    DAVENDA TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_venda_cliente 
        FOREIGN KEY (CLIENTE_ID)
        REFERENCES tb_cliente (ID_CLIENTE)
        ON DELETE RESTRICT,

    CONSTRAINT fk_venda_camiseta
        FOREIGN KEY (CAMISETA_ID)
        REFERENCES tb_camiseta (ID_CAMISETA)
        ON DELETE RESTRICT
);

CREATE INDEX IF NOT EXISTS idx_venda_cliente ON tb_venda (CLIENTE_ID);

CREATE INDEX IF NOT EXISTS idx_venda_camiseta ON tb_venda (CAMISETA_ID);

CREATE INDEX IF NOT EXISTS idx_camiseta_selecao ON tb_camiseta (SELECAO);
```

## 8. Padrão DAO

## 9. Padrão Factory

## 10. Interface Gráfica


## Autor

Lucas de Sousa Teixeira

Curso: Bacharelado em Ciência da Computação

Disciplina: Linguagem de Programação Orientada a Objetos — LPOO

Professora: Vanessa Lago Machado

Período: 2026/1

## Declaração de Uso de Inteligência Artificial
