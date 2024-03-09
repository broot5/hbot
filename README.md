# hbot
A telegram bot that helps downloading and uploading images

## Run natively
```console
git clone https://github.com/broot5/hbot.git
cd hbot

python -m venv .venv # Optional
source .venv/bin/activate # Optional

pip install -r requirements.txt

export BOT_NAME="hbot"
export SITE="gallery-dl_supported_site"
export DL_URL="url"
export TOKEN="sdsafasd123124"

python bot.py
```

## Run with docker
### Build image
```console
git clone https://github.com/broot5/hbot.git
cd hbot
docker compose up -d
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
