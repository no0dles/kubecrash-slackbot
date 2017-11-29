from src.pod_condition import PodCondition
from src.pod_container_status import PodContainerStatus


class PodBot(object):
    def __init__(self, notifier, client):
        self.v1 = client.CoreV1Api()
        self.notifier = notifier

    def run(self):
        pod_list = self.v1.list_pod_for_all_namespaces()
        for item in pod_list.items:
            if item.status.conditions:
                last_condition = item.status.conditions[-1]

                pod_status = PodCondition()
                pod_status.namespace = item.metadata.namespace
                pod_status.name = item.metadata.name
                pod_status.type = last_condition.type
                pod_status.reason = last_condition.reason
                pod_status.message = last_condition.message

                self.notifier.send_pod_info(pod_status)

            if item.status.container_statuses:
                last_status = item.status.container_statuses[-1]

                if last_status.last_state.terminated:
                    pod_container_status = PodContainerStatus()
                    pod_container_status.key = 'last_state'
                    pod_container_status.namespace = item.metadata.namespace
                    pod_container_status.name = item.metadata.name
                    pod_container_status.reason = last_status.last_state.terminated.reason
                    pod_container_status.message = last_status.last_state.terminated.message

                    self.notifier.send_pod_info(pod_container_status)

                if last_status.state.waiting:
                    pod_container_status = PodContainerStatus()
                    pod_container_status.key = 'state'
                    pod_container_status.namespace = item.metadata.namespace
                    pod_container_status.name = item.metadata.name
                    pod_container_status.reason = last_status.state.waiting.reason
                    pod_container_status.message = last_status.state.waiting.message

                    self.notifier.send_pod_info(pod_container_status)
