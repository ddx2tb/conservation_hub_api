# Project Configuration

- Generate a random SECRET_KEY and update its value in `settings.py`:

```shell
openssl rand -hex 32
```

- Install the required packages for the project.

```shell
pip install -r requirements.txt
```

# Database

![Database Diagram](/assets/images/conservation_hub_api_database.png "Database Diagram")