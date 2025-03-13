from rest_framework import serializers
from .models import *
from django.contrib.auth import password_validation


class TasksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tasks
        fields = ["id", "name", "content", "created_at"]

class AccountsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accounts
        fields = ["id", "username", "first_name", "last_name", "email", "phone", "created_at", "password"]
        extra_kwargs = {
            'password': {'write_only': True}  # Password should not be read from the response
        }

    def create(self, validated_data):
        password = validated_data.get('password')
        # Validate password
        if password:
            try:
                # This will raise ValidationError if password does not meet the validators
                password_validation.validate_password(password)
            except Exception as e:
                raise serializers.ValidationError({"password": str(e)})
        phone = validated_data.get('phone')
        
        # Create the Accounts instance without saving yet
        accounts_instance = Accounts(**validated_data)

        # Normalize the phone number
        accounts_instance.phone = accounts_instance.normalize_phone_number()

        # Save the instance to the database
        accounts_instance.save()

        return accounts_instance
