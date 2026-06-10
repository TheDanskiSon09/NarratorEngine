"""The module contains base controller class"""

from NarratorEngine.subsystem import SubSystem


class Controller(SubSystem):
    subsystem_name = 'controller'

    def give_options(
            self,
            options: list,
            prompt: str = '',
            allow_numbers: bool = True,
            allow_lowering: bool = True,
            clear_after: bool = True,
            clear_on_mistake: bool = True
    ) -> str:
        normalized = {}
        if allow_lowering:
            normalized = {str(option).lower(): option for option in options}
        while True:
            user_input = input(prompt).strip()
            if allow_numbers and user_input.isdigit():
                index = int(user_input) - 1
                if 0 <= index < len(options):
                    result = options[index]
                    break
            if user_input in options:
                result = user_input
                break
            if allow_lowering:
                key = user_input.lower()
                if key in normalized:
                    result = normalized[key]
                    break
            if clear_on_mistake:
                self.game.terminal.clear_terminal()
        if clear_after:
            self.game.terminal.clear_terminal()
        return result
