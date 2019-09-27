import re


class reUtils:

    def find_all_search(self, pattern, content, default_text):
        result = re.search(pattern, content)
        if result is None or result == "":
            return default_text
        return result.group()

    def find_all(self, pattern, content, default_text):
        result = re.findall(pattern, content)
        if result is None or len(result) == 0:
            return default_text
        return result[0]
