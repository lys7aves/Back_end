from rest_framework import serializers
from management_system.models import Authenticators, GameServers, WaitingLine, GameResult, UserInfo


class AuthenticatorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Authenticators
        fields = ['X_Auth_Token', 'auth_key']


class GameServersSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameServers
        fields = ['auth_key', 'problem', 'time', 'status']


class WaitingLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = WaitingLine
        fields = ['_id', '_from']


class GameResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameResult
        fields = ['win', 'lose', 'taken']


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ['_id', 'grade']