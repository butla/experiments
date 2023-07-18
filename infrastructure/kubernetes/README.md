# Kubernetes sample

## K3s notes

- DNS for services is working
- ingress works, but can't be created at immediately after creating the pods and the service

### Connecting with kubectl

- start k3s: sudo k3s server
- mkdir ~/.kube
- sudo cp /etc/rancher/k3s/k3s.yaml ~/.kube/config
- sudo chown butla:butla ~/.kube/config

### Wiping k3s cluster
https://github.com/k3s-io/k3s/issues/84#issuecomment-468464353

sudo umount `cat /proc/self/mounts | awk '{print $2}' | grep '^/run/k3s'`
sudo umount `cat /proc/self/mounts | awk '{print $2}' | grep '^/var/lib/rancher/k3s'`
sudo rm -rf /var/lib/rancher/k3s
sudo rm -rf /etc/rancher/k3s
