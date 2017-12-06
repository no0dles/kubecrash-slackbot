# Kube Monitor Slackbot
![CI](https://ci.bertschi.io/api/badges/no0dles/kubemonitor-slackbot/status.svg)

KubeMonitor is a monitoring slackbot for Kubernetes clusters. It informs about failing pods in the cluster in realtime and helps to troubleshoot them.

![Slackbot](docs/screenshot.png)

## Getting Started

[<img src="https://platform.slack-edge.com/img/add_to_slack.png">](https://slack.com/oauth/authorize?client_id=276786832352.277688463872&scope=bot,channels:read,chat:write:bot)

## Requirements
- Kubernetes 1.7+
- RBAC

## Features
- Monitoring pod condition and container statuses
- Monitoring job and cron status (development)
- Monitoring logs (planned)

## Documentation
- [Manual Installation](docs/ManualInstallation.md)
- [Docker Hub](https://hub.docker.com/r/no0dles/kubecrash-slackbot/)

## License

WTFPL