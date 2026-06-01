# Aulas 04 e 05 - Consumindo API FastAPI

Este pacote contém três projetos:

2. `frontend-js-puro`: consumo da API com HTML, CSS e JavaScript puro.
3. `frontend-vue`: consumo da mesma API com Vue + Vite.

## Ordem sugerida

1. Rodar a API FastAPI.
2. Testar a API no Swagger.
3. Abrir o front-end JS puro.
4. Rodar o front-end Vue.

## API

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Front-end Vue

```bash
cd frontend-vue
npm install
npm run dev
```
