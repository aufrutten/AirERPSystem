# Aufrutten Template

> This template should help get you started developing with Vue 3 in Vite and with Django in python.
> To change if it not yet more **template**!

## Description

---
### The project has:

- Kubernetes
- HTTPS
- Docker-compose
- CI/CD
- Auto Setup
- Self tests
- OAuth2 (Google, Facebook, Apple)

### The main library's or frameworks

1. Backend

   - Django
   - DRF (Django REST Framework)
   - Social Django
   - CorsHeaders
   - DRF Spectacular
   - JWT (uses both methods for auth: Cookie, JWT)
2. Frontend

   - Vite
   - Vue3
   - Jquery
   - Bootstrap5
   - Axios
   - Favicon Plugin
    

> This template already have the Kubernetes CI/CD and HTTPS
> with different subdomains: 
> api.example.com - backend, 
> example.com - frontend;
> docker-compose is for development environment
> kubernetes is for deployment environment


### Photo's

---


![dark_theme](https://i.imgur.com/gNeFTvr.png)
![login](https://i.imgur.com/gfY8F8E.png)
![white_theme](https://i.imgur.com/dYLAI7d.png)
![profile](https://i.imgur.com/wE03tDZ.png)


## Recommended IDE's

[PyCharm](https://www.jetbrains.com/pycharm/) + [WebStorm](https://www.jetbrains.com/webstorm/)


## Recommendation for project 

---

- You can use that template for your project like fork
or do updates to this template and make the pull request
- If you just developer of project (your are not maintainer)
you doesn't require to configure the Docker; CI/CD; K8s

> TODO LIST: Using PyCharm or WebStorm you can use the "# TODO: " 
> in the project to indicate to do part of code 

> ### All code must be covered and tested!!!

## Production setup

---
#### `kubernetes/README.md`

## CI/CD setup

---
#### `.github/workflows/README.md`

## Developing setup

---
### Change permission for execution

```sh
chmod -R +x ./scripts/
```

### Install environment variables
```sh
./scripts/setup-env.sh
```

### Setup deployment domain

```sh
sudo ./scripts/dev-hosts.sh
```

### Run dev server

```sh
docker-compose up
```

## Dev domains

---

> Dev domain is indicated in public.env

```
API - api.localhost

UI/UX - localhost
```
 
