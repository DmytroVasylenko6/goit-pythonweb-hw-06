# Start

## Run database in docker
```bash
docker run --name postgres -p 5432:5432 -e POSTGRES_PASSWORD=2020202020 -d postgres
```

## Install pipenv
```bash
pip install --user pipenv
```

## To “enter” inside the virtual environment, you need to execute:
```bash
pipenv shell
```

## Install 
```bash
pipenv install
```

## Test 

```bash
python3 ./app/seed.py 
```

```bash
python3 ./app/my_select.py
```


