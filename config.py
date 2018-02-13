class Config(dict):
    def __getattr__(self, name):
        return self[name] if self.has_key(name) else None
    def __setattr__(self, name, value):
        self[name] = value