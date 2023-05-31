# API_Dataseed


## Como Rodar localmente

```
$ virutalenv fastapi && source fastapi/bin/activate & pip3 install -r requirements.txt
```

aplicar migrate
```
yoyo apply
```

export PYTHONPATH=$PWD/app

```
uvicorn main:app --reload
```
