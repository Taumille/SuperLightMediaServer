import re, os


class Cleaner:
    def __init__(self, path=None):
        self.name_history = []
        self.mediatype = None
        self.date = 1900
        self.episode = "S00E00"
        self.path = path
        try:
            self.filename = os.path.basename(path)
        except TypeError:
            self.filename = ""

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
            print(f"Date : {self.date}")
        else:
            # If no year is found, take the whole name
            title_part = name
            self.date = 1900
            print(f"no date {self.date}")

        self.filename = title_part
        return title_part

    def clean_from_episodes(self, orig: str):
        name = orig
        # Find date between 1900 and 2039
        match = re.search(r'\bS\d{1,2}E\d{1,2}\b', name)

        if match:
            # Extract everything before the seasons/episode
            title_part = name[:match.start()]
            self.episode = match.group(0)
        else:
            # If no year is found, take the whole name
            title_part = name

        self.filename = title_part
        return title_part

    def replace_dot_with_space(self, orig: str):
        self.filename = orig.replace('.', ' ').strip()
        self.filename = self.filename.replace('_', ' ').strip()
        return self.filename

    def remove_site(self, orig: str):
        name = orig
        name = re.sub(r'^\[.*?\]\s*', '', name)
        if (name[-1] in ['(', '[']):
            name = name[:-1]
        self.filename = name
        return name

    def full_clean_movie(self, path: str):
        self.path = path
        self.filename = os.path.basename(path)
        self.clean_extension(self.filename)
        self.clean_from_date(self.filename)
        self.remove_site(self.filename)
        self.replace_dot_with_space(self.filename)

        return self.filename

    def full_clean_series(self, path: str):
        self.path = path
        self.filename = os.path.basename(path)
        self.clean_extension(self.filename)
        self.clean_from_episodes(self.filename)
        self.clean_from_date(self.filename)
        self.remove_site(self.filename)
        self.replace_dot_with_space(self.filename)

        return self.filename
