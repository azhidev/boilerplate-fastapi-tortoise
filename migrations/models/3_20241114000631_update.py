from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "users" ADD "password" VARCHAR(200) NOT NULL;
        CREATE UNIQUE INDEX "uid_users_usernam_266d85" ON "users" ("username");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP INDEX "idx_users_usernam_266d85";
        ALTER TABLE "users" DROP COLUMN "password";"""
