import json
import os

from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""

    api_key: str = os.getenv('YT_API_KEY')

    def __init__(self, channel_id: str) -> None:
        """
        Экземпляр инициализируется по id канала.
        Дальше все данные будут подтягиваться по API.
        """

        self.channel = \
            self.get_service().channels().list(
                id=channel_id, part='snippet,statistics').execute()
        self.title = self.channel['items'][0]['snippet']['title']
        self.description = self.channel['items'][0]['snippet']['description']
        self.url = \
            f"https://www.youtube.com/channel/{self.channel['items'][0]['id']}"
        self.subscriber_count = \
            self.channel['items'][0]['statistics']['subscriberCount']
        self.video_count = self.channel['items'][0]['statistics']['videoCount']
        self.view_count = self.channel['items'][0]['statistics']['viewCount']
        self.__channel_id = self.channel['items'][0]['id']

    @property
    def channel_id(self):
        return self.__channel_id

    def to_json(self, name: str):
        """ Создает файл {name_of_channel}.json' c данными по каналу"""
        with open(f"../src/{name}", mode='w+') as file:
            json.dump(self.channel, file, indent=2, ensure_ascii=False)

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        self.printj(self.channel)

    @classmethod
    def get_service(cls):
        """Получает объект для работы с API вне класса"""
        return build('youtube', 'v3',
                     developerKey=cls.api_key)

    @staticmethod
    def printj(dict_to_print: dict) -> None:
        """Выводит словарь в json-подобном удобном формате с отступами"""
        print(json.dumps(dict_to_print, indent=2, ensure_ascii=False))
