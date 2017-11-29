from src.pod import Pod


class PodCondition(Pod):
    type: str
    reason: str
    message: str

    def identifier(self):
        return "PC:%s:%s" % (self.namespace, self.name)

    def status_value(self):
        return self.type

    def is_error(self):
        return self.reason is not None or self.message is not None

    def message_title(self):
        return "pod %s condition is %s" % (self.name, self.reason)

    def message_content(self):
        return self.message