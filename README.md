# Back-End-Development-Pictures

Pictures microservice — Flask REST API built for the IBM Back-End Development Capstone Project (Course 11 of the IBM Back-End Development Professional Certificate).

## Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/health` | Service health check |
| GET | `/pictures` | List all pictures |
| GET | `/pictures/count` | Number of pictures |
| GET | `/pictures/<id>` | Get one picture |
| POST | `/pictures` | Create a picture (`title`, `url`) |
| PUT | `/pictures/<id>` | Update a picture |
| DELETE | `/pictures/<id>` | Delete a picture |

## Run locally

```bash
pip install -r requirements.txt
python app.py        # serves on http://localhost:5001
```

## Tests

```bash
pytest -v
```

## Docker

```bash
docker build -t pictures-service .
docker run -p 5001:5001 pictures-service
```
