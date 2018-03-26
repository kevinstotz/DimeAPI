class FileNameConverter:
    regex = '\d+_.*\.[a-z0-9A-Z]{3,}'

    def to_python(self, value):
        return value

    def to_url(self, value):
        return value
