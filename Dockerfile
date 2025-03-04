FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10

WORKDIR /srv/

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

# Copy poetry.lock* in case it doesn't exist in the repo
COPY ./pyproject.toml ./poetry.lock* /srv/
ENV PYTHONPATH=/srv
RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then poetry install --no-root ; else poetry install --no-root --only main ; fi"

COPY . /srv/

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
