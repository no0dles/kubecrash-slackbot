# kubecrash-slackbot

## Installation

cluster_role.yaml
```yaml
kind: ClusterRole
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: kubecrash-minimal
  namespace: kube-system
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "list"]
```

service_account.yaml
```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: kubecrash
  namespace: kube-system
```

cluster_role_binding.yaml
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: kubecrash-minimal
  namespace: kube-system
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: kubecrash-minimal
subjects:
- kind: ServiceAccount
  name: kubecrash
  namespace: kube-system
```

deployment.yaml
```yaml
apiVersion: apps/v1beta2
kind: Deployment
metadata:
  name: kubecrash
  namespace: kube-system
spec:
  replicas: 1
  selector:
    matchLabels:
      app: kubecrash
  template:
    metadata:
      labels:
        app: kubecrash
    spec:
      containers:
      - name: kubecrash
        image: no0dles/kubecrash-slackbot
        env:
        - name: SLACK_ACCESS_TOKEN
          value: xoxb-123456789012-123456789012345678901234
        - name: SLACK_CHANNEL
          value: kubernetes-cluster
      serviceAccountName: kubecrash
```

## Links
[Docker Hub](https://hub.docker.com/r/no0dles/kubecrash-slackbot/)