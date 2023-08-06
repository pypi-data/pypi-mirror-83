

class SystemNotSupport(Exception):
    msg = "Current system {name} is not supported."

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.message = self.msg.format(**kwargs)

    def __str__(self):
        return self.message
