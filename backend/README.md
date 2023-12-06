# Backend
___

> The instructions of usage of backend part of 
> application

### Apps
___

To add new app you should to move your app in 
folder app and do segment list

1. App settings
   - Go to apps.py in your app 
   - Change the ---> 
   - From "name = 'nameApp'
   - To   "name = 'apps.nameApp'"

2. Do migrations
   - ```shell
     python3 ./manage.py migrate
     ```
     
### Developing environment setup

```sh
chmod -R +x ./scripts && ./scripts/developing_env_setup.sh
```

> Every time after installing new packages 
> will do new build of backend image and
> update the requirements.txt file.
> The command for update req file will below 

```sh
pip3 freeze > ./requirements.txt
```

### For coverage tests
#### Each commit must be coverage by 95~100% test and wrote localization

```sh
chmod -R +x ./scripts && ./scripts/coverage.sh
```