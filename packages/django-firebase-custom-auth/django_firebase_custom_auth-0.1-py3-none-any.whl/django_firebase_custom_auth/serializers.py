from rest_framework import serializers

class CredentialSerializer(serializers.Serializer):
	username = serializers.CharField()
	password = serializers.CharField()


class TokenSerializer(serializers.Serializer):
	token = serializers.CharField()
