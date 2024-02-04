# Deploy IP Ask on AWS EKS

Non-comprehensive guide for running IP Ask (or any similar application) in [AWS EKS](https://aws.amazon.com/eks/).

---

## Prerequisites

- AWS account

- AWS user with an access key and [sufficient rights](https://eksctl.io/usage/minimum-iam-policies/)

- Domain with a DNS zone managed by [AWS Route 53](https://aws.amazon.com/route53/)

- Some free time

---

## Software installation and configuration

- Install and configure [awscli](https://aws.amazon.com/cli/)

  ```sh
  $ pacman -S aws-cli-v2
  ...
  $ aws configure
  AWS Access Key ID [None]: <your_key_id>
  AWS Secret Access Key [None]: <secret_access_key>
  Default region name [None]: us-east-1
  Default output format [None]: json
  $
  ```

- Install [eksctl](https://eksctl.io/)

  ```sh
  pacman -S eksctl
  ```

- Install [kubectl](https://kubernetes.io/docs/reference/kubectl/)

  ```sh
  pacman -S kubectl
  ```

- Request a public SSL/TLS certificate from [AWS ACM](https://aws.amazon.com/certificate-manager/) and validate it with a DNS record

  ```sh
  aws acm request-certificate \
  --domain-name ipask.me \
  --subject-alternative-names "ipask.me" "*.ipask.me" \
  --key-algorithm EC_secp384r1 \
  --validation-method DNS \
  --idempotency-token 1000 \
  --options CertificateTransparencyLoggingPreference=ENABLED
  ```

  Note that `CertificateTransparencyLoggingPreference` must be `enabled`.

- Set and export environment variables that are required for some of the commands later on

  ```sh
  export AWS_EKS_CLUSTER_NAME=my_eks_cluster
  export AWS_EKS_REGION=$(aws configure get region)
  export AWS_EKS_VERSION=1.28
  export AWS_EKS_CIDR="10.250.0.0/16"
  export AWS_IAM_CERT_ARN="SSL/TLS certificate's ARN"
  export IPASK_VERSION="The latest tag for the prestigen/ipask image"
  ```

---

## Create the AWS EKS cluster

- Create

  All `AWS_EKS_*` environment variables must be set.

  ```sh
  envsubst < eks-cluster.yaml | eksctl create cluster -f -
  ```

- Test

  ```sh
  $ kubectl get nodes
  NAME                            STATUS   ROLES    AGE   VERSION
  ip-192-168-10-86.ec2.internal   Ready    <none>   1m    v1.28.3-eks-e71965b
  ip-192-168-44-82.ec2.internal   Ready    <none>   1m    v1.28.3-eks-e71965b
  $
  ```

---

## Install AWS LB Controller for the Kubernetes cluster

Follow the [official guide](https://docs.aws.amazon.com/eks/latest/userguide/aws-load-balancer-controller.html)

---

## Install [Kubernetes Metrics Server](https://github.com/kubernetes-sigs/metrics-server)

```sh
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/high-availability-1.21+.yaml
```

---

## Install [k9s](https://k9scli.io/)

```sh
pacman -S k9s
```

---

## Build and push the container to hub.docker.com

Handled by the CI/CD

---

## Deploy the web application to AWS EKS

The `IPASK_VERSION` environment variable must be set.

```sh
envsubst < k8s/ipask.yaml | kubectl apply -f -
```

---

## Create the K8s Ingress resource(s) and the AWS Application Load Balancer

The `AWS_IAM_CERT_ARN` environment variable must be set.

Choose option `A` **_or_** `B`.

- (Option A): All HTTP requests are automatically redirected to HTTPS

  ```sh
  envsubst < alb-ingress.yaml | kubectl apply -f -
  ```

  Note: Due to the fact that `curl` does not automatically follow the new location when the server returns 301, it must be supplied with either the protocol (`https://`) or the `-L` flag:

  ```sh
  curl -L ipask.me
  curl https://ipask.me
  ```

- (Option B): All HTTP requests except the ones coming from `curl` are redirected to HTTPS

  ```sh
  envsubst < alb-ingress-curl-workaround.yaml | kubectl apply -f -
  ```

  With this solution, the HTTP-to-HTTPS redirection is disabled for `curl`, which is why the following command will work but the communication will be unencrypted:

  ```sh
  curl ipask.me
  ```

  `wget` on the other hand automatically initiates a new connection to the new HTTPS location provided in the `301` response:

  ```sh
  wget -qO - ipask.me
  ```

---

## Create DNS "A" record that points to the Application Load Balancer
