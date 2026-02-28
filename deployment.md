# Deployment / CI-CD

Этот файл описывает, как устроен деплой сервиса `Time Server API` с помощью GitHub Actions, Docker и GitHub Container Registry (GHCR).

## Общая схема

1. При пуше в ветку `main` запускается workflow `.github/workflows/deploy.yml`.
2. Первая job **build-and-push**:
   - клонирует репозиторий;
   - логинится в GitHub Container Registry (GHCR);
   - собирает Docker-образ из `Dockerfile` в корне проекта;
   - пушит образ в GHCR с тегами:
     - `ghcr.io/<owner>/time-server-api:latest`;
     - `ghcr.io/<owner>/time-server-api:<SHA коммита>`.
3. Вторая job **deploy**:
   - ожидает завершения `build-and-push`;
   - по SSH подключается к удалённому серверу;
   - логинится в GHCR;
   - скачивает последний образ (`:latest`);
   - останавливает и удаляет старый контейнер (если он есть);
   - запускает новый контейнер с именем `time-server-api` и пробрасывает порт `8000`.

## Файл workflow

Workflow находится по пути: `.github/workflows/deploy.yml`.

В нём определены две job:

- `build-and-push` — сборка и публикация образа в GHCR;
- `deploy` — деплой на удалённый сервер по SSH.

## Секреты GitHub Actions

Создать в репозитории (или организации) в разделе **Settings → Secrets and variables → Actions**:

- `SSH_HOST` — хост удалённого сервера (IP или домен);
- `SSH_PORT` — порт SSH (обычно `22`);
- `SSH_USERNAME` — пользователь на сервере, под которым выполняются Docker-команды;
- `SSH_PRIVATE_KEY` — приватный SSH-ключ в текстовом виде (как в `~/.ssh/id_rsa`, без парольной фразы или с заранее настроенным `ssh-agent`);
- `GHCR_USERNAME` — логин пользователя/бота, который имеет доступ к GHCR;
- `GHCR_TOKEN` — персональный токен доступа (PAT) с правами хотя бы `read:packages` (и `write:packages`, если через него тоже пушить образы).

## Что происходит на сервере

Во второй job по SSH выполняется примерно такой сценарий:

1. Логин в GHCR:

   ```bash
   echo "$GHCR_TOKEN" | docker login ghcr.io -u "$GHCR_USERNAME" --password-stdin
   ```

2. Загрузка свежего образа:

   ```bash
   docker pull ghcr.io/<owner>/time-server-api:latest
   ```

3. Остановка и удаление старого контейнера (если есть):

   ```bash
   docker stop time-server-api || true
   docker rm time-server-api || true
   ```

4. Запуск нового контейнера:

   ```bash
   docker run -d \
     --name time-server-api \
     --restart=always \
     -p 8000:8000 \
     ghcr.io/<owner>/time-server-api:latest
   ```

При необходимости можно добавить монтирование томов, переменные окружения и т.п. прямо в команду `docker run` в `deploy.yml`.

