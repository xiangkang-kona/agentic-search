import os

from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_DIR = os.path.join(DATA_DIR, "db")
VECTOR_DB_DIR = os.path.join(DATA_DIR, "vector_db")
CODE_REPO_DIR = os.path.join(DATA_DIR, "code_repo")
LOGS_DIR = os.path.join(DATA_DIR, "logs")
KEYWORD_INDEX_DIR = os.path.join(DATA_DIR, "keyword_index")

DB_PATH = os.path.join(DB_DIR, "enterprise.db")

LLM_API_KEY = os.environ.get("DASHSCOPE_API_KEY", "")
LLM_BASE_URL = os.environ.get("DASHSCOPE_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1")
LLM_MODEL = os.environ.get("DASHSCOPE_MODEL", "qwen3.6-plus")

# Streamlit Cloud 部署时密钥通过 Secrets 提供（st.secrets），本地开发时通过环境变量/.env 提供
if not LLM_API_KEY:
    try:
        import streamlit as st
        LLM_API_KEY = st.secrets.get("DASHSCOPE_API_KEY", "")
    except Exception:
        pass

MAX_SEARCH_ROUNDS = 20

for d in [DATA_DIR, DB_DIR, VECTOR_DB_DIR, CODE_REPO_DIR, LOGS_DIR, KEYWORD_INDEX_DIR]:
    os.makedirs(d, exist_ok=True)
