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
export DL_URL="url/{}"
export TOKEN="sdsafasd123124"

python bot.py
```

## Run with docker
### docker run
```console
docker run --name hbot \
    -e BOT_NAME="hbot" \
    -e SITE="gallery-dl_supported_site" \
    -e DL_URL="url/{}" \
    -e TOKEN="sdsafasd123124" \
    -v ./save:/app/save \
    ghcr.io/broot5/hbot
```

### docker compose
```yaml
version: "3.8"

services:
  hbot:
    image: ghcr.io/broot5/hbot
    container_name: hbot
    restart: unless-stopped
    volumes:
      - ./save:/app/save
    environment:
      - BOT_NAME=hbot
      - SITE=gallery-dl_supported_site
      - DL_URL=url/{}
      - TOKEN=asdsafasd123124
```
