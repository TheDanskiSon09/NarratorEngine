"""The module contains base terminal class"""

from sys import stdout
from time import sleep
import platform
import ctypes
from os import system, name
from NarratorEngine.constants import TXT_COLOR_DEFAULT, PB_DEFAULT_FUELLED_SLOT, PB_DEFAULT_MISSING_SLOT, PB_DEFAULT_BARRIER
from NarratorEngine.subsystem import SubSystem


class Terminal(SubSystem):
    subsystem_name = 'terminal'

    @classmethod
    def on_subsystem_init(cls):
        cls.graphic: bool = False
        if cls.game.get_entry_point() in ('Interpreter', 'EXE'):
            cls.graphic = True
            cls.set_window_title(cls(), cls.game.game_title)
            cls.set_window_fullscreen(cls())

    def typewrite(
            self,
            message: str,
            typewrite_delay=0.1,
            sleep_after=0,
            clear_after: bool = False
    ) -> str:
        for symbol in message:
            stdout.write(symbol)
            stdout.flush()
            sleep(typewrite_delay)
        sleep(sleep_after)
        if clear_after:
            self.clear_terminal()
        return ''
    

    def set_window_title(self,
                         new_title: str
                         ) -> None:
        if self.graphic:
            if name == 'nt':
                system(f'title {new_title}')
            else:
                print('\033]0;{new_title}\007')

    def set_window_fullscreen(self) -> None:
        if self.graphic:
            if platform.system() == 'Windows':
                self._fullscreen_windows()
            elif platform.system() == 'Linux':
                self._fullscreen_linux()
            elif platform.system() == 'Darwin':
                self._fullscreen_mac()
                

    def clear_terminal(self) -> None:
        if self.graphic:
            system('cls' if name == 'nt' else 'clear')
            

    @staticmethod
    def set_terminal_cursor_visible(visible: bool) -> None:
        if platform.system() == 'Windows':
            import ctypes
            handle = ctypes.windll.kernel32.GetStdHandle(-11)

            class CONSOLE_CURSOR_INFO(ctypes.Structure):
                _fields_ = [('dwSize', ctypes.c_uint),
                            ('bVisible', ctypes.c_bool)]
            cursor_info = CONSOLE_CURSOR_INFO()
            ctypes.windll.kernel32.GetConsoleCursorInfo(handle, ctypes.byref(cursor_info))
            cursor_info.bVisible = visible
            ctypes.windll.kernel32.SetConsoleCursorInfo(handle, ctypes.byref(cursor_info))
        else:
            if visible:
                stdout.write(f'\033[?25h')
            else:
                stdout.write(f'\033[?25l')
            stdout.flush()

    @staticmethod
    def _fullscreen_windows() -> None:
        kernel32 = ctypes.windll.kernel32
        console = kernel32.GetConsoleWindow()
        if console != 0:
            ctypes.windll.user32.ShowWindow(console, 3)

    @staticmethod
    def _fullscreen_linux() -> None:
        print('\033[9;1t', end='', flush=True)
        print('\033[5t', end='', flush=True)

    @staticmethod
    def _fullscreen_mac() -> int:
        from subprocess import call
        script = r'''
        tell application "Terminal"
            activate
            tell application "System Events"
                key code 3 using {command down, control down} -- Cmd+Ctrl+F
            end tell
        end tell
        '''
        return call(['osascript', '-e', script])

    @staticmethod
    def get_progress_bar(
            current_value,
            max_value,
            length,
            color: str = TXT_COLOR_DEFAULT,
            bar_title: str = '',
            fuelled_slot: str = PB_DEFAULT_FUELLED_SLOT,
            missing_slot: str = PB_DEFAULT_MISSING_SLOT,
            barrier: str = PB_DEFAULT_BARRIER
    ) -> str:
        remaining_bars = round(current_value / max_value * length)
        lost_bars = max_value - remaining_bars
        return (f'{bar_title}'
                f'{barrier}'
                f'{color}'
                f'{remaining_bars * fuelled_slot}'
                f'{lost_bars * missing_slot}'
                f'{TXT_COLOR_DEFAULT}'
                f'{barrier}')
