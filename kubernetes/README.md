# Production deployment 


---

### Pre-requirements


   - Kubernetes Cluster (2 or more nodes)
   - Domain (Full access with write dns configuration)
   - Have the yml config of K8s cluster
   - Have Docker account 
   - Have GitHub account


## Production setup


---
### Kubeconfig.yml


> You should move your kubeconfig yaml file
> in the /kubernetes/ with name kubeconfig.yml 
> it should look like: 
> 
> #### /kubernetes/kubeconfig.yml

### CD/CD Configuration

> Go to the:
> #### /.github/workflows/README.md


### Setup public.env

> The next step after CI/CD that is configuring
> the public.env 

| key           | value              |
|---------------|--------------------|
| BACKEND_HOST  | api.yourDomain.com |
| FRONTEND_HOST | yourDomain.com     |

### Uploading the manifests

```sh
chmod +x ./k8s-install.sh && ./k8s-install.sh
```

> After uploading (This process is very longer)
> you will see the external ip of your
> LoadBalancer and you should configure your DNS
> like in this example

#### Example: 

----

| domain          | A               |
|-----------------|-----------------|
| api.example.com | XXX.XXX.XXX.XXX |
| example.com     | XXX.XXX.XXX.XXX |


### Installing certs and ingress

---

> After configuring of your dns and installing manifests,
> install the HTTPS and entry in your k8s 

```sh
chmod +x ./k8s-install-cert.sh && ./k8s-install-cert.sh
```

## Done
