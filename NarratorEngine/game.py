"""The module contains implementation of game class"""

from NarratorEngine.level import Level
from NarratorEngine.terminal import Terminal
from NarratorEngine.controller import Controller


class Game:

    def __init__(
            self,
            game_title: str,
            start_level,
            start_level_section: str = None,
            enable_audio: bool = True,
            post_mortem_input: list = None,
            error_post_mortem_input: list = None,
            terminal_class=Terminal(),
            controller_class=Controller(),
            level_class=Level(),
            extra_subsystems: list = None
    ) -> None:
        if not error_post_mortem_input:
            error_post_mortem_input = ['Interpreter']
        if not post_mortem_input:
            post_mortem_input = ['Interpreter', 'IDLE']
        try:
            self.game_title = game_title
            self.enable_audio = enable_audio
            self.current_level = None
            self.current_level_section = None
            self._entity_data = {}
            self._init_subsystems([
                terminal_class,
                controller_class,
                level_class
            ])
            if extra_subsystems:
                self._init_subsystems(extra_subsystems)
            self.change_level(start_level, start_level_section)
            if self.get_entry_point() in post_mortem_input:
                input('Game process finished\nPress Enter to quit')
        except Exception as exception:
            if self.get_entry_point() in error_post_mortem_input:
                print(f'{exception.__class__.__name__}: {exception}')
                input('Press Enter to quit')
            else:
                raise

    def _init_subsystems(
            self,
            subsystems: list
    ) -> None:
        for subsystem in subsystems:
            if subsystem:
                subsystem.init_subsystem(self)

    def change_level(
            self,
            new_level,
            new_level_section: str = None
    ) -> None:
        from NarratorEngine.constants import LEVEL_SECTION_PREFIX
        if self.current_level:
            self.current_level.close()
        self.current_level = new_level
        self.current_level_section = None
        self.current_level.open()
        if new_level_section:
            self.current_level_section = new_level_section
            section_func = getattr(self.current_level, LEVEL_SECTION_PREFIX + new_level_section)
            section_func()

    @staticmethod
    def get_entry_point() -> str:
        import sys
        if getattr(sys, 'frozen', False):
            return 'EXE'
        if 'idlelib' in sys.modules:
            return 'IDLE'
        return 'Interpreter'

    @staticmethod
    def is_android() -> bool:
        from platform import platform
        if 'android' in platform().lower():
            return True
        return False
