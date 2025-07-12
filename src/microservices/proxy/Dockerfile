FROM python:3.13 AS build

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /factory
COPY requirements.txt /factory/

RUN python -m pip install build
RUN python -m pip install -r requirements.txt

COPY pyproject.toml /factory/
COPY cinema_proxy /factory/cinema_proxy

RUN python -m build

FROM python:3.13 AS deploy

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/
RUN python -m pip install -r requirements.txt

COPY --from=build /factory/dist /dist/
RUN python -m pip install cinema-proxy -f /dist

COPY entrypoint.sh /app/
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT [ "/app/entrypoint.sh", "uv" ]