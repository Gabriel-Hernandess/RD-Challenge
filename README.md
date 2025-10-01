# 🚀 RD Station Challenge (Django + DRF)

Este projeto é uma API desenvolvida em **Django Rest Framework**, com autenticação, gestão de sondas (`probes`) e suporte a testes automatizados com **pytest**.
Implementei um simples **Frontend** com templates do Django para simular melhor uma aplicação real, com exibição das malhas e suas respectivas funções de forma mais dinâmica com **JS**.
Junto de tudo isso, ainda conteinerizei a aplicação com **Docker** e utilizei **Poetry** para gerenciamento de dependências e **PostgreSQL** como banco de dados.

---

## 🛠️ Tecnologias utilizadas
- Python 3.13  
- Django 5.x  
- Django Rest Framework  
- JavaScript (para templates dinâmicos do frontend, diretos nos arquivos HTML) 
- Poetry (para gerenciamento de dependências)  
- Pytest + Pytest-Django  
- Docker + Docker Compose  
- PostgreSQL  

---

## ⚙️ Como rodar o projeto

### 1. Clone o repositório
git clone https://github.com/Gabriel-Hernandess/RD-Challenge.git
cd RD-Challenge

### 2. Suba o ambiente com Docker
docker compose up --build

### 3. Aplique as migrações
docker compose exec backend python manage.py makemigrations
docker compose exec backend python manage.py migrate

### 4. Crie um superusuário para testar o sistema
docker compose exec backend python manage.py createsuperuser

### 5. Rodando os testes
docker compose exec backend pytest

---

# 📡 Endpoints principais

## 🔑 Autenticação
POST /auth/login/ → login do usuário  
POST /auth/logout/ → logout do usuário  

## 🛰️ Probes
POST /probes/ → cria nova sonda  
PUT /probes/{id}/move/ → movimenta a sonda (respeita bordas da malha e ignora comandos inválidos)  
DELETE /probes/{id}/ → deleta a sonda  

---

# 🧪 Testes

Os testes estão em apps/*/tests.py e usam **pytest + pytest-django**, com um `conftest` na raiz do projeto para utilização de fixtures, evitando repetições desnecessárias de código.

**Principais cenários testados:**
- Login/logout  
- Criação de sondas  
- Movimentação válida e inválida de sondas  
- Respeito às bordas da malha  
- Exclusão de sondas