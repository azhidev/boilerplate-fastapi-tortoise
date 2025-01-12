from dotenv import load_dotenv

import os
load_dotenv()

SQL_URL = os.getenv("SQL_URL") # postgres://postgres:sfadfsadfsafsd@mywebapp.com:38716
# print(SQL_URL, "*"*100)

TORTOISE_ORM = {
    "connections": {
        "default": SQL_URL
    },
    "apps": {
        "models": {
            "models": ["app.models", "aerich.models"],
            "default_connection": "default",
        },
    },
    "use_tz": False,
    "timezone": "UTC"
}
