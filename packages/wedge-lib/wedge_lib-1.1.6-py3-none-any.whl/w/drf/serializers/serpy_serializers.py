from w.serializers import serializer


class UserSerializer(serializer.SerpySerializer):
    id = serializer.IntField()
    username = serializer.Field()
    first_name = serializer.Field()
    last_name = serializer.Field()
    email = serializer.Field()
    is_active = serializer.BoolField()


class UserWithDateSerializer(UserSerializer):
    date_joined = serializer.DateField()
