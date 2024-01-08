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
    -e SITE="gallery-dl_supported_site" \
    -e DL_URL="url" \
    -e TOKEN="sdsafasd123124" \
    -v ./:/app/ \
    hbot
```

### docker compose
check [docker-compose.yml](./docker-compose.yml)
