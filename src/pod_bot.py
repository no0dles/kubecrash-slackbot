from src.pod_condition import PodCondition
from src.pod_container_status import PodContainerStatus
from kubernetes.client import CoreV1Api, AppsV1beta2Api, V1beta2Deployment, V1Event
from src.notifier import Notifier


class PodBot(object):
    def __init__(self, notifier: Notifier, v1: CoreV1Api, apps: AppsV1beta2Api):
        self.v1 = v1
        self.apps = apps
        self.notifier = notifier

    def test(self, deploy: V1beta2Deployment):
        pass

    def run(self):
        #list = self.apps.list_deployment_for_all_namespaces()
        #""":type : V1beta2DeploymentList"""
        #for deployment in list.items:
            #self.test(deployment)
            #print(deployment.metadata)
        #node_list = self.v1.list_node()
        #for item in node_list.items:
        #    print(item)

        #return


        return

        pod_list = self.v1.list_pod_for_all_namespaces()
        for item in pod_list.items:
            #for container in item.spec.containers:
                #logs = self.v1.read_namespaced_pod_log(item.metadata.name, item.metadata.namespace, container=container.name, tail_lines=100)
                #print(logs)

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
