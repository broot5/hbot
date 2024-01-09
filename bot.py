import asyncio
import aiohttp
import os
import subprocess
import json
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
)
from PIL import Image
from telegraph import Telegraph

BOT_NAME = os.environ["BOT_NAME"]
SITE = os.environ["SITE"]
DL_URL = os.environ["DL_URL"]
TOKEN = os.environ["TOKEN"]


def download(number: int):
    if os.path.isdir(f"dl/{str(number)}"):
        return 0

    result = subprocess.run(
        [
            "gallery-dl",
            DL_URL.format(number),
            "-D",
            f"dl/{str(number)}",
            "--write-info-json",
        ],
        capture_output=True,
        text=True,
    )
    print("STDOUT:", result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)


def read_info(number: int, key: str):
    with open(f"dl/{number}/info.json", "r") as file:
        data = json.load(file)
    return data.get(key)


async def convert_image_task(number: int, count: int):
    # 각 이미지 변환 작업에 대한 비동기 태스크 생성
    tasks = [convert_image(number, i) for i in range(1, count + 1)]

    # 모든 이미지 변환 작업을 병렬로 실행
    await asyncio.gather(*tasks)


async def convert_image(number: int, i: int, executor=None):
    webp_path = f"dl/{number}/{SITE}_{number}_{str(i).zfill(3)}.webp"
    png_path = f"dl/{number}/{SITE}_{number}_{str(i).zfill(3)}.png"

    loop = asyncio.get_running_loop()

    # 동기적으로 실행되는 이미지 처리 함수를 스레드 풀에서 비동기적으로 실행
    await loop.run_in_executor(executor, sync_convert_image, webp_path, png_path)

    print(f"Converted {webp_path} to {png_path}")


# 이미지 로드 및 변환을 동기적으로 수행하는 함수
def sync_convert_image(webp_path, png_path):
    webp_image = Image.open(webp_path)
    png_image = webp_image.convert("RGBA")
    png_image.save(png_path, "PNG")


async def upload_img_task(number: int, count: int) -> list:
    tasks = [upload_img(number, i) for i in range(1, count + 1)]

    result = await asyncio.gather(*tasks)
    return result


async def upload_img(number: int, i: int) -> str:
    img_path = f"dl/{number}/{SITE}_{number}_{str(i).zfill(3)}.png"

    # aiohttp를 사용하여 파일 업로드
    async with aiohttp.ClientSession() as session:
        url = "https://telegra.ph/upload"
        # 'files' 파라미터를 multipart form data로 구성
        data = aiohttp.FormData()
        data.add_field(
            "file",
            open(img_path, "rb"),
            filename=f"image_{i}.png",
            content_type="image/png",
        )

        # POST 요청을 비동기적으로 전송하고 응답을 받음
        async with session.post(url, data=data) as response:
            # 응답을 json 형태로 파싱
            result = await response.json()

            # 이미지 용량이 커서 업로드 되지 않는 경우... 이미지 압축? 이미지 crop후 나눠서 업로드??

            # 업로드된 이미지의 URL을 반환
            if result and isinstance(result, list) and "src" in result[0]:
                return result[0]["src"]

    # 오류 발생 시 Image not found 이미지 반환
    print(f"Error occured while uploading {img_path}")
    return "/file/723a4a969cab6322ce831.jpg"  # Image not found!


def generate_html(img_urls: list) -> str:
    result = ""
    for i in range(len(img_urls)):
        result += f"<img src='{img_urls[i]}'/>\n"

    return result


# TODO: 함수 분리해서 진행 상황 보고 가능할 듯
async def process(bot_name: str, number: int) -> str:
    # nurl.json 존재 확인하고 없으면 생성
    if not os.path.isfile("nurl.json"):
        nurl = dict()
        with open("nurl.json", "w") as outfile:
            json.dump(nurl, outfile)

    # nurl.json 불러오고 해당하는 number 존재하면 그에 해당하는 url 리턴
    with open("nurl.json", "r") as file:
        nurl = json.load(file)
    if str(number) in nurl:
        return nurl.get(str(number))

    # gallery-dl 이용하여 이미지들 다운
    download(number)
    count = read_info(number, "count")

    # info.json 검사
    if str(number) != str(read_info(number, "gallery_id")):
        new_number = int(read_info(number, "gallery_id"))
        os.rename(f"dl/{str(number)}", f"dl/{str(read_info(number, 'gallery_id'))}")
        number = new_number

    # webp를 png로 변환
    await convert_image_task(number, count)

    # telegraph에 업로드(이미지 각자 업로드 -> 전체 html 파일 업로드)
    telegraph = Telegraph()
    print(telegraph.create_account(short_name=bot_name, author_name=bot_name))

    img_urls = await upload_img_task(number, count)

    title = f"{read_info(number, 'title')}-{number}"
    html = generate_html(img_urls)

    response = telegraph.create_page(title, html_content=html, author_name=bot_name)

    print(response)

    # nurl.json에 number-url 쌍 저장
    nurl[str(number)] = response.get("url")
    with open("nurl.json", "w") as outfile:
        json.dump(nurl, outfile)

    return nurl.get(str(number))


async def get(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = await context.bot.send_message(
        chat_id=update.effective_chat.id, text="처리 중..."
    )
    url = await process(BOT_NAME, int(context.args[0]))
    await context.bot.edit_message_text(
        chat_id=update.effective_chat.id,
        message_id=msg.message_id,
        text=url,
    )


if __name__ == "__main__":
    application = ApplicationBuilder().token(TOKEN).build()

    get_handler = CommandHandler("get", get)

    application.add_handler(get_handler)

    application.run_polling()
