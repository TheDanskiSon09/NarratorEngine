from locale import getdefaultlocale
import json
import os


class LocalizationManager:

    def __init__(
            self,
            locales_path='locales',
            default_language='en'
    ):
        self.locales_path = locales_path
        self.default_language = default_language
        self.current_language = default_language
        self.translations = {}
        print(self.detect_system_language())

    @staticmethod
    def detect_system_language() -> str:
        '''
        Пытается определить язык системы.
        Возвращает код языка (ru, en, de...) или None.
        '''
        try:
            lang, _ = getdefaultlocale()
            if not lang:
                return None

            # 'ru_RU' -> 'ru'
            return lang.split('_')[0].lower()
        except Exception:
            return None

    @staticmethod
    def get_available_languages():
        '''
        Возвращает список доступных языков по папке locales
        '''
        if not os.path.isdir(self.locales_path):
            return []

        langs = []
        for filename in os.listdir(self.locales_path):
            if filename.endswith('.json'):
                langs.append(filename.replace('.json', ''))
        return langs

    def set_language(self, lang: str) -> bool:
        '''
        Устанавливает язык, если доступен.
        Возвращает True, если успешно.
        '''
        path = os.path.join(self.locales_path, f'{lang}.json')
        if not os.path.exists(path):
            return False

        try:
            with open(path, 'r', encoding='utf-8') as f:
                self.translations = json.load(f)

            self.current_language = lang
            return True
        except Exception:
            return False

    def init_language(self):
        '''
        Автоинициализация языка:
        1) язык системы
        2) fallback
        '''
        system_lang = self.detect_system_language()
        available = self.get_available_languages()

        if system_lang in available:
            self.set_language(system_lang)
        else:
            self.set_language(self.default_language)

    def translate(self, key: str) -> str:
        '''
        Получить перевод по ключу
        '''
        return self.translations.get(key, f'[{key}]')


if __name__ == '__main__':
    LocalizationManager()
