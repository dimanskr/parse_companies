import re
import sys


class ProgressBarMixin:
    """
    Миксин с методом для отображения прогресса загрузки данных в консоли
    """
    @staticmethod
    def show_progress(current: int, total: int):
        """
        Статический метод вывода процесса загрузки.
        :param current:
        :param total:
        """
        progress = (current + 1) / total
        bar_length = 50
        block = round(bar_length * progress)
        progress_text = f"\rЗагрузка: [{'#' * block + '-' * (bar_length - block)}] {progress * 100:.0f}%"
        sys.stdout.write(progress_text)
        sys.stdout.flush()


class CleanTagsMixin:
    """
    Миксин с методом для удаления тегов из строки
    """
    @staticmethod
    def clean_tags(text: str | None) -> str:
        """
        Удаляет теги из строки с использованием регулярного выражения.
        :param text: str
        :return: text without tags
        """
        clean = re.compile('<.*?>')
        if text:
            return re.sub(clean, '', text)
        return text
