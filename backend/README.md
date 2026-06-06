# Task Manager API

API REST para gerenciamento de tarefas, construída com Flask e SQLAlchemy.

Este é o backend de um projeto maior (frontend estático + PostgreSQL + Jenkins). Para
orquestração com Docker Compose e a pipeline de CI/CD, veja o [README na raiz](../README.md).

## 📋 Características

- ✅ CRUD de tarefas + atualização de status
- ✅ PostgreSQL em produção, com **fallback automático para SQLite** em desenvolvimento
- ✅ API RESTful, com mensagens e rótulos de status em **pt-BR**
- ✅ CORS habilitado (Flask-CORS)
- ✅ Testes automatizados (pytest) com cobertura ~96%

## 🛠️ Pré-requisitos

- Python 3.11 ou superior
- pip (ambiente virtual recomendado)

## 📦 Instalação

```bash
cd backend

# Criar e ativar um ambiente virtual (opcional, recomendado)
python -m venv venv
# Windows:        venv\Scripts\activate
# macOS/Linux:    source venv/bin/activate

pip install -r requirements.txt
```

## 🚀 Como Executar

```bash
python app.py
```

A API ficará disponível em `http://localhost:5000` (modo debug ligado por padrão).

## 🗄️ Banco de Dados

O `app.py` monta a URI do banco nesta ordem de precedência:

1. `SQLALCHEMY_DATABASE_URI` (se definida)
2. `DATABASE_URL` (se definida)
3. As variáveis `DB_HOST` / `DB_PORT` / `DB_NAME` / `DB_USER` / `DB_PASSWORD` (usadas pelo `docker-compose.yml`)
4. **Fallback automático para SQLite local** (`sqlite:///tasks.db`)

Rodando direto com `python app.py` e sem nenhuma dessas variáveis, ele usa SQLite — nenhuma
configuração extra é necessária para desenvolvimento.

## 📡 Endpoints da API

As rotas são registradas **sem prefixo `/api`** (base = `http://localhost:5000`).

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/` | Mensagem de status da API (JSON) |
| `GET` | `/tasks` | Lista todas as tarefas |
| `POST` | `/tasks` | Cria uma nova tarefa (`title` obrigatório) |
| `GET` | `/tasks/<id>` | Retorna uma tarefa específica |
| `PUT` | `/tasks/<id>` | Atualiza título, descrição e/ou status |
| `PATCH` | `/tasks/<id>/status` | Atualiza apenas o status |
| `DELETE` | `/tasks/<id>` | Remove uma tarefa |
| `GET` | `/statuses` | Lista os status válidos com rótulos (pt-BR) |
| `GET` | `/ui` | Serve um `index.html` estático via Flask (a UI oficial roda separada na porta 8080) |

Status válidos (`VALID_STATUSES` em `routes.py`): `pending`, `in_progress`, `done`.
`GET /statuses` devolve os rótulos pt-BR correspondentes: **Aguardando**, **Em andamento**, **Concluída**.

## 📚 Modelo de Dados — Task

| Campo       | Tipo    | Descrição                              |
|-------------|---------|----------------------------------------|
| id          | Integer | Identificador único (chave primária)   |
| title       | String  | Título da tarefa (obrigatório)         |
| description | String  | Descrição da tarefa (opcional)         |
| status      | String  | Status da tarefa (padrão: `pending`)   |

## 📁 Estrutura

```
backend/
├── app.py                   # Flask app factory + configuração do banco
├── database.py              # Instância compartilhada do SQLAlchemy (db)
├── models.py                # Modelo Task + to_dict()
├── routes.py                # Endpoints da API (Blueprint "api")
├── send_email.py            # Envio de e-mail (usado pela pipeline Jenkins)
├── requirements.txt         # Dependências da aplicação
├── jenkins_requirements.txt # Dependências instaladas no Jenkins
├── Dockerfile               # Imagem Docker do backend
└── tests/                   # Testes (pytest)
```

## 🔧 Dependências principais

- **Flask 3.0.2** — framework web
- **Flask-SQLAlchemy 3.1.1** — ORM
- **Flask-Cors 4.0.0** — CORS habilitado em `app.py`
- **psycopg2-binary 2.9.9** — adaptador PostgreSQL
- **python-dotenv** — carrega variáveis de um `.env` local
- **pytest** / **pytest-cov** — testes e cobertura

## 🧪 Testes

Os testes usam um SQLite **em memória** configurado em `tests/conftest.py` (uma base nova por teste).

```bash
cd backend

pytest -q

# Com relatório de cobertura (HTML), como na pipeline
pytest --cov=. --cov-report=html
```

Cobertura atual: ~96% (veja `image.png`).

## 🐳 Docker

O `Dockerfile` já existe nesta pasta (`python:3.11-slim`, expõe `5000`, roda `python app.py`):

```bash
docker build -t task-manager .
docker run -p 5000:5000 task-manager
```

Para subir o backend junto com Postgres, frontend e Jenkins, use `docker compose up --build`
na raiz do projeto (recomendado) — veja o [README na raiz](../README.md).

## 📝 Notas

- Sem autenticação — todos os endpoints são abertos.
- Mensagens de erro e rótulos de status em pt-BR.
- O frontend é um app estático **separado** em `../frontend` (servido na porta 8080).
  Veja [`frontend/README.md`](../frontend/README.md).
