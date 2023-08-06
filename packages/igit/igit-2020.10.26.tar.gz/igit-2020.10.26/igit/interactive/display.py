import os
import emoji
from emoji import EMOJI_ALIAS_UNICODE
from termcolor import colored


class Display:

    def __init__(self, os_type=os.name) -> None:
        self.os_type = os_type

    def message(self, text, color='white', icon='poop'):
        _emoji, _emoji_render_method = self.emojize(icon)
        self._display(f'{_emoji} - {text}', color, _emoji_render_method)

    def list(self, text, items, color, icon):
        _emoji, _emoji_render_method = self.emojize(icon)
        self._display(f'{_emoji} - {text}:', color, _emoji_render_method)
        for item in items:
            self._display(" " * 8 + item, 'white', _emoji_render_method)

    def emojize(self, icon):
        icon = f':{icon}:'
        if self.os_type == 'nt':
            import psutil
            res_icon = '*'
            shell = psutil.Process(os.getpid()).parent().parent().name()
            if shell == 'powershell.exe':
                res_icon = EMOJI_ALIAS_UNICODE[icon]
            return res_icon, lambda *args, **kwargs: args[0]
        else:
            return icon, emoji.emojize

    @classmethod
    def diff(cls, diff):
        if diff.startswith('+++') or diff.startswith('---'):
            print(colored(diff, 'white'))
        elif diff.startswith('+'):
            print(colored(diff, 'green'))
        elif diff.startswith('-'):
            print(colored(diff, 'red'))
        else:
            print(colored(diff, 'white'))

    @staticmethod
    def _display(text, color, emoji_method=lambda *args, **kwargs: args):
        print(colored(emoji_method(text, use_aliases=True), color))


if __name__ == '__main__':

    display = Display(os_type='nt')
    display.message('hello', 'green', 'thumbsup')
    display.list('hello', ['item1', 'item2'], 'green', 'thumbsup')
