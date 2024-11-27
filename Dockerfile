FROM python:3.13-slim

WORKDIR /opt/app

ADD pyproject.toml ./

# Poetry
ENV PATH="${PATH}:/root/.poetry/bin"

RUN : \
&& pip install poetry \
&& POETRY_VIRTUALENVS_CREATE=false poetry install --no-interaction --no-ansi \
&& :

# To COPY the remote files at working directory in container
COPY . .

# Now the structure looks like this '/opt/app/cad_webapp/main.py'
CMD ["python", "main.py"]