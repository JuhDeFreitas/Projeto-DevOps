# Frontend — Task Manager UI

Interface web em HTML/CSS/JavaScript puro (sem build step) que consome a Task Manager API.

Faz parte de um projeto maior (backend Flask + PostgreSQL + Jenkins). Para orquestração com
Docker Compose e a pipeline de CI/CD, veja o [README na raiz](../README.md).

## Arquivos

Todos os arquivos ficam diretamente em `frontend/` (não existe subpasta `static/`):

- `index.html` — board principal: colunas **Aguardando / Em andamento / Concluídas**, drag & drop entre colunas e busca por título
- `edit.html` — página de edição de uma tarefa
- `app.js` — lógica do board (listar, criar, buscar, remover, mudar status por drag & drop)
- `edit.js` — lógica da página de edição
- `styles.css` — estilos
- `package.json` + `tests/` — suíte de testes (Jest)

## Como funciona

A base da API vem de `window.API_BASE`, definida no topo de `index.html` e `edit.html`:

```html
<script>
  window.API_BASE = 'http://localhost:5000';
</script>
```

Se `window.API_BASE` não estiver definida, o cliente usa `window.location.origin` como fallback
(`const apiBase = window.API_BASE || window.location.origin;`).

O backend **já tem CORS habilitado** (`Flask-CORS` em `backend/app.py`), então o frontend pode ser
servido em outra origem (porta 8080) e chamar a API em `:5000` sem nenhuma configuração extra. Para
apontar para outro host/porta do backend, basta editar `window.API_BASE` nos dois arquivos HTML.

> A busca por nome é feita **no próprio frontend**: `app.js` baixa `GET /tasks` e filtra a lista no
> navegador. Não há endpoint de busca no backend.

## Como Rodar

### Servidor estático (desenvolvimento)

```bash
cd frontend
python -m http.server 8080
```

Abra `http://localhost:8080`. Garanta que o backend esteja rodando em `http://localhost:5000`
(veja [`backend/README.md`](../backend/README.md)).

### Via Docker / Compose

O `Dockerfile` serve os arquivos com `python -m http.server 8080`. O modo recomendado é
`docker compose up --build` na raiz, que sobe frontend, backend, Postgres e Jenkins juntos —
veja o [README na raiz](../README.md).

## 🧪 Testes

Suíte **Jest** (ambiente jsdom) cobrindo `app.js` e `edit.js`. Requer **Node.js 18+** e npm.

```bash
cd frontend
npm ci

npm test                # roda a suíte
npm run test:coverage   # roda com relatório de cobertura
```

A configuração do Jest está em `package.json` e impõe um limite mínimo de **90%** de cobertura
(statements, branches, functions e lines). Os testes ficam em `tests/`:

- `tests/app.test.js` — funções exportadas de `app.js` (listar, criar, buscar, remover, status, modal)
- `tests/app.dom.test.js` — integração do `DOMContentLoaded` (botões, drag & drop, delegação de clique)
- `tests/edit.test.js` — funções de `edit.js` e resolução de id (query string / `localStorage`)

Essa mesma suíte roda na stage **Testes Frontend** da pipeline Jenkins.
