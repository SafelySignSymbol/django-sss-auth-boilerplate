# django sss auth boilerplate

## Install

```
$ https://github.com/SafelySignSymbol/django-sss-auth-boilerplate.git

$ docker compose up -d
```

## Environment

docker-compose.yml

```docker-compose.yml
version: '3'

services:
  server:
    build: ./docker
    ports:
      - 8000:8000
    volumes:
      - ./python:/workspace
    working_dir: /workspace
    command: python manage.py runserver 0.0.0.0:8000

```

Dockerfile

```Dockerfile
FROM python:3.9.5

ENV PYTHONUNBUFFERED 1
RUN mkdir /workspace

WORKDIR /workspace

ADD requirements.txt /workspace/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

```

requirements.txt

```requirements.txt
Django==4
django-bootstrap5
symbol-hkdf-python
```

## 動作手順

1. localhost:8000 を開く
2. 画面右上の登録ボタンを押下する
3. 任意のメールアドレスを入力
4. ユーザー名に Symbol アドレスを入力
5. ログインを押下
6. SSS を用いて認証を行う
