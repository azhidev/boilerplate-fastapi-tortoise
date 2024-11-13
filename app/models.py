from tortoise import fields, models

# from tortoise.contrib.pydantic import pydantic_model_creator


class User(models.Model):
    id = fields.CharField(pk=True, max_length=50)
    username = fields.CharField(max_length=50)
    
    class Meta:
        table = "users"


class Permission(models.Model):
    id = fields.IntField(pk=True, index=True)
    name = fields.CharField(max_length=50)
    codename = fields.CharField(max_length=50)
    path = fields.CharField(max_length=50)

    # Many-to-many relation with User
    users = fields.ManyToManyField("models.User", related_name="permissions", through="user_permissions")

    class Meta:
        table = "permissions"


class UserPermissions(models.Model):
    id = fields.IntField(max_length=50, pk=True, index=True)
    user = fields.ForeignKeyField("models.User", related_name="user_permissions")
    permission = fields.ForeignKeyField("models.Permission", related_name="user_permissions")

    class Meta:
        table = "user_permissions"



# class Operation(models.Model):
#     id = fields.CharField(pk=True, max_length=50)

#     class Meta:
#         app = "sim"
#         table = "operations"
#         indexes = [
#         ]


# class SubOperation(models.Model):
#     operation = fields.ForeignKeyField("sim.Operation", related_name="sub_operations", null=True, on_delete=fields.CASCADE)

#     class Meta:
#         app = "sim"
#         table = "sub_operations"
#         indexes = [
#             ("operation_id", "record_time"),
#         ]
