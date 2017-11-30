
## Manual Installation

cluster_role.yaml
```yaml
kind: ClusterRole
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name:kubemonitor-clusterrole
  namespace: kube-system
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["list"]
```

service_account.yaml
```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: kubemonitor
  namespace: kube-system
```

cluster_role_binding.yaml
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: kubemonitor-binding
  namespace: kube-system
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: kubemonitor-clusterrole
subjects:
- kind: ServiceAccount
  name: kubemonitor
  namespace: kube-system
```

deployment.yaml
```yaml
apiVersion: apps/v1beta2
kind: Deployment
metadata:
  name: kubemonitor
  namespace: kube-system
spec:
  replicas: 1
  selector:
    matchLabels:
      app: kubemonitor
  template:
    metadata:
      labels:
        app: kubemonitor
    spec:
      containers:
      - name: kubemonitor
        image: no0dles/kubemonitor-slackbot
        env:
        - name: SLACK_ACCESS_TOKEN
          value: xoxb-123456789012-123456789012345678901234
        - name: SLACK_CHANNEL
          value: kubernetes-cluster
      serviceAccountName: kubemonitor
```
