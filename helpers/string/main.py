class StringCounter:
    def __init__(self, path, unique=True):
        self.strings = [line.strip() for line in open(path).read().split('\n')]
        if unique:
            self.strings = list(set(self.strings))
        self.index = 0

    def get(self):
        if self.index >= len(self.strings):
            raise Exception("No more strings")
        string = self.strings[self.index]
        self.index += 1
        return string

    def iter_get(self):
        if self.index >= len(self.strings):
            self.index = 0
        string = self.strings[self.index]
        self.index += 1
        return string

    def available(self):
        return len(self.strings) - self.index

    def count(self):
        return len(self.strings)
