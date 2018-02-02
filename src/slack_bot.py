import slackclient
from src.settings import SLACK_ACCESS_TOKEN
from kubernetes.client import CoreV1Api
import time
import src.settings
from tabulate import tabulate
import re


def print_as_code(text: str):
    return "```%s```" % (text,)


class Mute(object):
    pattern = r'mute|shutup|shut up|silence|fuck off|quite'

    def run(self):
        src.settings.MUTED = True
        return 'ay ay Captain'


class Unmute(object):
    pattern = r'unmute|speak'

    def run(self):
        src.settings.MUTED = False
        return 'As you wish Milord'


class Status(object):
    pattern = r'status|how are you'

    def run(self):
        if src.settings.MUTED:
            return 'I\'m not allowed to speak (muted)'
        else:
            return 'I\'m allowed to speak (unmuted)'


class GetPods(object):
    pattern = r'get pods|get pod|get po'

    def __init__(self, v1: CoreV1Api):
        self.v1 = v1

    def run(self):
        rows = []
        for pod in self.v1.list_namespaced_pod('default').items:
            rows.append([pod.metadata.namespace, pod.metadata.name])
        return print_as_code(tabulate(rows, headers=['Namespace', 'Name'], tablefmt='plain'))


class GetLogs(object):
    pattern = r'logs (.*)'

    def __init__(self, v1: CoreV1Api):
        self.v1 = v1

    def run(self, name):
        return print_as_code(self.v1.read_namespaced_pod_log(name, 'default', tail_lines=10))


class SlackBot(object):
    commands = []

    def __init__(self, v1: CoreV1Api):
        self.commands.append(GetPods(v1))
        self.commands.append(GetLogs(v1))
        self.commands.append(Mute())
        self.commands.append(Status())
        self.commands.append(Unmute())

        self.sc = slackclient.SlackClient(SLACK_ACCESS_TOKEN)
        if self.sc.rtm_connect():
            while True:
                events = self.sc.rtm_read()
                for event in events:
                    if 'type' not in event or event['type'] != 'message':
                        continue

                    if str(event['text']).startswith('<@U85LDEFSL>'):
                        try:
                            self.process_message(event['channel'], event['text'][13:])
                        except:
                            self.sc.rtm_send_message(event['channel'], 'I got some errors...')

                time.sleep(0.5)

    def process_message(self, channel: str, text: str):
        for cmd in self.commands:
            m = re.match(cmd.pattern, text)
            if m:
                response = cmd.run(*m.groups())
                self.sc.rtm_send_message(channel, response)
                return

        self.sc.rtm_send_message(channel, 'I didn''t understand that')
