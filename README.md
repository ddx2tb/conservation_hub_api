# Project Configuration

- Generate a random SECRET_KEY and update its value in `settings.py`:

```shell
openssl rand -hex 32
```

- Install the required packages for the project.

```shell
pip install -r requirements.txt
```

## Getting Started

First, run the development server:

```bash
python3 -m venv venv
# and
source venv/bin/activate
# and
pip install -r requirements.txt
# and
uvicorn main:app
```

# CRUD

View and test CRUD

- [users](http://127.0.0.1:8000/docs#/users/)
    * [JWT](http://127.0.0.1:8000/docs#/users/login_for_access_token_users_token_post) (Get JWT token)
- [ecosystems](http://127.0.0.1:8000/docs#/ecosystems/)
- [projects](http://127.0.0.1:8000/docs#/projects/)
- [tasks](http://127.0.0.1:8000/docs#/tasks/)
- [resources](http://127.0.0.1:8000/docs#/resources/)
- [resources_assignment](http://127.0.0.1:8000/docs#/resources_assignment/)

# Security / Login

- UUID(s)
- JWT

# Database

![Database Diagram](/assets/images/conservation_hub_api_database.png "Database Diagram")