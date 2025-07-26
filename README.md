# 📐 Desafio Calculadora Kogui

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![Django](https://img.shields.io/badge/Django-5.x-green?logo=django)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

Portal web com **calculadora interativa**, **histórico de operações** e **autenticação de usuários**, desenvolvido para o desafio técnico da **Kogui**.

---

## 📑 Sumário

- [🚀 Tecnologias Utilizadas](#-tecnologias-utilizadas)
- [✨ Funcionalidades](#-funcionalidades)
- [📦 Estrutura do Projeto](#-estrutura-do-projeto)
- [⚙️ Como Rodar o Projeto](#️-como-rodar-o-projeto)
- [🔗 Endpoints Importantes](#-endpoints-importantes)
- [🧪 Rodando os Testes](#-rodando-os-testes)

---

## 🚀 Tecnologias Utilizadas

- **Python 3.x**
- **Django 5.x** – Framework web de alto nível
- **SQLite** – Banco de dados padrão
- **HTML5, CSS3, JavaScript** – Interface da calculadora
- **Git** – Controle de versão

---

## ✨ Funcionalidades

✅ **Autenticação de Usuários** (login e cadastro)  
✅ **Calculadora Avançada** – Operações básicas (soma, subtração, multiplicação, divisão)  
✅ **Histórico de Operações** – Armazena cálculos por usuário  
✅ **Limpeza de Histórico**  
✅ **Design Responsivo** (desktop e mobile)  
✅ **Testes Automatizados** (models e views)

---

## 📦 Estrutura do Projeto

```bash
.
├── portal/                 # Projeto Django principal
│   ├── settings.py         # Configurações globais
│   ├── urls.py             # URLs do projeto
│   └── wsgi.py, asgi.py
├── core/                   # App principal
│   ├── models.py           # Modelo Operacao
│   ├── views.py            # Lógica (calculadora, login, histórico)
│   ├── urls.py             # URLs do app
│   ├── admin.py            # Admin Django
│   └── tests.py            # Testes automatizados
├── templates/              # HTML
│   ├── registration/       # Login e cadastro
│   └── calculadora.html
├── static/                 # CSS / JS
│   ├── css/calculator.css
│   └── js/calculator.js
├── db.sqlite3              # Banco SQLite
├── manage.py               # Utilitário Django
└── README.md
```

## ⚙️ Como Rodar o Projeto

### **1. Clone o repositório**

```bash
git clone https://github.com/seu-usuario/desafio-calculadora-kogui.git
cd desafio-calculadora-kogui
```

### **2. Crie e ative um ambiente virtual**

```bash
python -m venv venv
# Ativar no Linux/Mac
source venv/bin/activate
# Ativar no Windows
venv\Scripts\activate
```

### **3. Instale as dependências**

```bash
pip install -r requirements.txt
```

### **4. Execute as migrações**

```bash
python manage.py migrate
```

### **5. Crie um superusuário (opcional, para acessar o admin)**

```bash
python manage.py createsuperuser
```

### **6. Inicie o servidor**

```bash
python manage.py runserver
```

Acesse:  
http://127.0.0.1:8000/

---

## 🔗 Endpoints Importantes

| URL          | Descrição             |
| ------------ | --------------------- |
| `/`          | Página da calculadora |
| `/login/`    | Login de usuário      |
| `/logout/`   | Logout de usuário     |
| `/register/` | Cadastro de usuário   |

---

## 🧪 Rodando os Testes

```bash
python manage.py test
```

Os testes cobrem **models** e **views** para garantir a integridade da aplicação.

---

## 📜 Licença

Este projeto está licenciado sob a **MIT License**. Veja o arquivo LICENSE para mais detalhes.
