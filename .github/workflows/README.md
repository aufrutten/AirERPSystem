# Setup CI/CD

## Description

---
> If you are **not** (owner,
> maintainer or consumer) 
> of this project || repository isn't require to do this!!!
> If you fork this repository, should to do this

---
### Requirements

- Docker Account
- GitHub Account

## Setup pre-requirements

---

In Docker account get or create:
- Take username
- Token read-only (Kubernetes)
- Token read-write (CI/CD)


## Setup

---
### Change permission for execution

```sh
chmod -R +x ../scripts/
```

### Install environment variables
```sh
../scripts/setup-env.sh
```

### Configure the private.env

---

| key             | value           |
|-----------------|-----------------|
| DOCKER_USERNAME | your_username   |
| DOCKER_TOKEN    | TOKEN_READ_ONLY |

### Configure the GitHub Secrets

---

| key                | value                     |
|--------------------|---------------------------|
| DOCKERHUB_USERNAME | your_username             |
| DOCKERHUB_TOKEN    | TOKEN_READ_WRITE          |
| KUBECONFIG         | Your kube config yml file |


# Done