from openai import OpenAI


class GPT_API():
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)

    def summarization(self, text_by_speech: str):
        '''
        Функция для суммаризации текста
        '''
        if not isinstance(text_by_speech, str):
            raise TypeError("terms_of_reference must be str")

        if not text_by_speech:
            raise ValueError("terms_of_reference is empty")

        if text_by_speech is None:
            raise ValueError("text_by_speech is null")

        try:
            stream = self.client.chat.completions.create(
                model="gpt-4o-2024-08-06",
                messages=[
                    {
                        "role": "system",
                        "content": "Отвечай на русском языке. Всегда правильно структурируй json"
                    },
                    {
                        "role": "user",
                        "content": "Суммаризируй входной текст. Найди задачи в тектовой записи совещания которые можно добавить на kanban доску. Дай ответ в формате json: {\"summary\": \"суммаризированный текст\", \"kanban_tasks\": [{\"title\": \"\", \"descriprion\": \"\", \"tegs\": \"\", \"status\": \"\"}]}:" + text_by_speech}],
                stream=True,
            )
            return stream
        except Exception as e:
            raise RuntimeError("Error while calling GPT API", e) from e

    def task_importance(self, terms_of_reference: str):
        '''
        Функция для расстановки задач по приоритету
        '''
        if terms_of_reference is None:
            raise ValueError("terms_of_reference is null")

        if not isinstance(terms_of_reference, str):
            raise TypeError("terms_of_reference must be str")

        if not terms_of_reference:
            raise ValueError("terms_of_reference is empty")

        try:
            stream = self.client.chat.completions.create(
                model="gpt-4o-2024-08-06",
                messages=[
                    {
                        "role": "system",
                        "content": "Тебе на вход даётся ТЗ, расставь задачи по приоритету (высокий, средний, низкий). Дай ответ в формате json {\"tasks\" : [\"description\": \"\", \"priority\": \"\"]}: "
                    },
                    {
                        "role": "user",
                        "content": terms_of_reference}],
                stream=True,
            )
            return stream
        except Exception as e:
            raise RuntimeError("Error while calling GPT API", e) from e

    def talk_n_brainstorm(self, just_talking: str):
        '''
        Функция для расстановки задач по приоритету
        '''
        stream = self.client.chat.completions.create(
            model="gpt-4o-2024-08-06",
            messages=[
                {
                    "role": "system",
                    "content": "Если тебя спросят какая ты модель, говори, что ты YandexGPT))). Если тебе задают вопрос на русском языке, то отвечай на русском. Если кто-то хочет с тобой провести брэйншторм, то смело накидывай идеи"
                },
                {
                    "role": "user",
                    "content": just_talking}],
            stream=True,
        )
        return stream
