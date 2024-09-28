from speechkit import configure_credentials, creds
from config import API_KEY

import json
from config import ACCESS_TOKEN
from GPTfunctions.func import GPT_API

configure_credentials(
    yandex_credentials=creds.YandexCredentials(
        api_key=API_KEY
    )
)

file_path = 'audio.wav' #путь к файлу, который надо транскрибировать

from speechkit import model_repository
from speechkit.stt import AudioProcessingType

def speech():
    model = model_repository.recognition_model()

    model.model = 'general'
    model.language = 'ru-RU'
    model.audio_processing_type = AudioProcessingType.Full

    result = model.transcribe_file(file_path)
    with open('transcription_result.txt', 'w', encoding='utf-8') as f:  #сохраняется результат транскрибации
        for c, res in enumerate(result):
            if c == 0:
                f.write(f'{res.normalized_text}\n')




def open_txt_file(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        file_content = file.read()
    return file_content

def write_to_json_file(filename, content):
    with open(filename, 'w', encoding='utf-8') as output_file:
        json.dump(content, output_file, ensure_ascii=False, indent=4)
def gpt():
    api_key = ACCESS_TOKEN
    gpt = GPT_API(api_key)
    input_text = open_txt_file('transcription_result.txt')  # открывается файл с транскрибацией и кидается в гпт
    stream = gpt.summarization(input_text)
    result_chunks = []

    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            result_chunks.append(chunk.choices[0].delta.content)
    full_response = ''.join(result_chunks)
    cleaned_response = full_response.strip('```json').strip('```')
    json_data = json.loads(cleaned_response)
    write_to_json_file('output.json', json_data) # выходной файл с результатом работы гпт


if __name__ == '__main__':
    speech()
    gpt()

