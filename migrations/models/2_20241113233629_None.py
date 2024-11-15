from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "permissions" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(50) NOT NULL,
    "codename" VARCHAR(50) NOT NULL,
    "path" VARCHAR(50) NOT NULL
);
CREATE TABLE IF NOT EXISTS "users" (
    "id" VARCHAR(50) NOT NULL  PRIMARY KEY,
    "username" VARCHAR(50) NOT NULL
);
CREATE TABLE IF NOT EXISTS "user_permissions" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "permission_id" INT NOT NULL REFERENCES "permissions" ("id") ON DELETE CASCADE,
    "user_id" VARCHAR(50) NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
