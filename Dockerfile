FROM python:3.11-slim

WORKDIR /app

# 先复制依赖清单并安装，利用 Docker 层缓存加速重复构建
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 复制项目全部文件（含 data/ 下的演示数据，避免启动时重新生成）
COPY . .

ENV PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=utf-8

# CloudBase 云托管通过 PORT 环境变量分配端口，Streamlit 需监听该端口
CMD ["sh", "-c", "streamlit run app.py --server.port=${PORT:-8501} --server.address=0.0.0.0 --server.headless=true"]
