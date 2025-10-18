import re


class Cleaner:
    def __init__(self, filename=None):
        self.name_history = []
        self.mediatype = None
        self.filename = filename
        self.date = 1900

    def clean_extension(self, orig: str):
        self.filename = orig.rsplit('.', 1)[0]
        return self.filename

    def clean_from_date(self, orig: str):
        name = orig
        # Find date between 1900 and 2039
        match = re.search(r'(19\d{2}|20[0-3]\d)', name)

        if match:
            # Extract everything before the year
            title_part = name[:match.start()]
            self.date = int(match.group(0))
        else:
            # If no year is found, take the whole name
            title_part = name

        self.filename = title_part
        return title_part

    def replace_dot_with_space(self, orig: str):
        self.filename = orig.replace('.', ' ').strip()
        return self.filename

    def remove_site(self, orig: str):
        name = orig
        name = re.sub(r'^\[.*?\]\s*', '', name)
        self.filename = name
        return name

    def full_clean(self, orig: str):
        self.filename = orig
        self.clean_extension(self.filename)
        self.clean_from_date(self.filename)
        self.remove_site(self.filename)
        self.replace_dot_with_space(self.filename)

        return self.filename
