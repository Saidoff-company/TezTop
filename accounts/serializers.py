from django.contrib.auth.hashers import make_password

from rest_framework import serializers

from accounts import models


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['phone_number', 'password']

    def create(self, validated_data):
        user = models.User.objects.create(
            phone_number=validated_data['phone_number'],
            password=make_password(validated_data['password']),
            is_active=False,
        )
        code = user.create_verify_code()
        data = {
            'message': 'Telefon raqamingiga sms kod yuborildi',
            'code': f'{code}'
        }
        return data


class RegisterVerifySerializer(serializers.Serializer):
    code = serializers.CharField(max_length=5)


class ResendVerifyCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['phone_number']
