from google.cloud import speech
import subprocess
import os

def speech_to_text(config, audio):
    client = speech.SpeechClient.from_service_account_json("pk_new.json")
    response = client.recognize(config=config, audio=audio)
    response.results
    return print_sentences(response)

def print_sentences(response):
    for result in response.results:
        best_alternative = result.alternatives[0]
        transcript = best_alternative.transcript
    return transcript

config = speech.RecognitionConfig(
language_code = "uk_UK",
enable_automatic_punctuation = True,
audio_channel_count = 1
)

def get_text():
    command = "ffmpeg -i voice.oga voice.wav"
    subprocess.call(command, shell=True)

    with open('voice.wav', 'rb') as f1:
        byte_data = f1.read()
    audio = speech.RecognitionAudio(content=byte_data)
    os.remove('voice.wav')
    return(speech_to_text(config, audio))

import logging
from aiogram import Bot, Dispatcher, executor
from aiogram.types import Message

logging.basicConfig(level=logging.INFO)

bot=Bot(token="6281566192:AAGauV3CBiZdBlv2OOvb2nHUhHmy__x_7Vw")
dp=Dispatcher(bot)

@dp.message_handler(content_types=["voice"])
async def voice_message_handler(message: Message):
    file_id = message.voice.file_id
    file = await bot.get_file(file_id)
    path = file.file_path
    await bot.download_file(path, "voice.oga")
    await message.reply(get_text())

if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True)