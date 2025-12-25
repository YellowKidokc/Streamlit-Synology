FROM python:3.11-slim

WORKDIR /srv
ENV PIP_NO_CACHE_DIR=1

COPY requirements.txt ./
RUN python -m venv /venv \
    && /venv/bin/pip install --upgrade pip \
    && /venv/bin/pip install -r requirements.txt

COPY streamlit_app.py ./
COPY apps ./apps

ENV PATH="/venv/bin:${PATH}" \
    APP_ROOT=/apps

EXPOSE 8501

CMD ["streamlit", "run", "streamlit_app.py", "--server.address=0.0.0.0", "--server.port=8501"]
