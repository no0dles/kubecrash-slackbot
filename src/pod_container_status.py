from src.pod import Pod


class PodContainerStatus(Pod):
    key: str
    reason: str
    message: str

    def identifier(self):
        return "PCS:%s:%s:%s" % (self.key, self.namespace, self.name)

    def status_value(self):
        return self.reason

    def is_error(self):
        return self.message is not None

    def message_title(self):
        return "pod %s status is %s" % (self.name, self.reason)

    def message_content(self):
        return self.message
