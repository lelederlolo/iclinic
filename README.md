# Virtual Environment

Please install the virtual environment via `requirements.txt` file.

```bash
conda create --name fastapi_postgres_env python=3.11
conda activate fastapi_postgres_env
pip install -r requirements.txt
```

# Run the FastAPI server

```bash
uvicorn main:app --reload
```