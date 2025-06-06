import re

class StringHelpers:
    @staticmethod
    def is_null_or_empty(string: str) -> bool:
        return string is None or string == ''

    @staticmethod
    def contains_alphabetic(text: str) -> bool:
        return any(char.isalpha() for char in text)

    @staticmethod
    def is_all_uppercase(text: str) -> bool:
        return bool(re.match(r'^[A-Z]+$', text.replace(" ", "")))

    @staticmethod
    def is_all_numeric(text: str) -> bool:
        return bool(re.match(r'^\d+$', text))

    @staticmethod
    def convert_to_integer(text: str) -> int:
        try:
            return int(text)
        except ValueError:
            print(f"Cannot convert '{text}' to an integer.")
            return None

    @staticmethod
    def clean_string(input_string: str) -> str:
        """
        Remove leading and trailing whitespace from a string and return None if the string is empty.

        Args:
            input_string (str): The input string.

        Returns:
            str or None: The cleaned string or None if the string is empty.
        """
        if input_string is None:
            return None

        cleaned_string = input_string.strip()
        if cleaned_string == "":
            return None
        return cleaned_string
