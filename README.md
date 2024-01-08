# hbot
A telegram bot that helps downloading and uploading images

## Run with docker
### Build image
```console
git clone https://github.com/broot5/hbot.git
cd hbot
docker buildx build -t hbot .
```

### docker run
```console
docker run --name hbot \
    -e BOT_NAME="hbot" \
    -e SITE="gallery-dl supported site" \
    -e DL_URL="url" \
    -e TOKEN="tg bot token" \
    -v ./nurl.json:/app/nurl.json \
    hbot
```

### docker compose
```yaml
services:
  hbot:
    image: hbot
    container_name: hbot
    restart: unless-stopped
    environment:
        - BOT_NAME="hbot"
        - SITE="gallery-dl supported site"
        - DL_URL="url"
        - TOKEN="tg bot token"
    volumes:
        - ./nurl.json:/app/nurl.json
```

