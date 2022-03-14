from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from management_system.models import Authenticators, GameServers, WaitingLine, GameResult, UserInfo
from management_system.serializers import AuthenticatorsSerializer, GameServersSerializer, WaitingLineSerializer, GameResultSerializer, UserInfoSerializer
import random
import numpy as np
import hashlib
import time


def delete_objects(objects):
    for obj in objects:
        obj.delete()


# Create your views here.
@csrf_exempt
def start_api(request):

    if request.method == 'GET':
        authenticators = AuthenticatorsSerializer(Authenticators.objects.all(), many=True)
        game_servers = GameServersSerializer(GameServers.objects.all(), many=True)
        waiting_line = WaitingLineSerializer(WaitingLine.objects.all(), many=True)
        game_result = GameResultSerializer(GameResult.objects.all(), many=True)
        user_info = UserInfoSerializer(UserInfo.objects.all(), many=True)

        print(type(user_info))
        ret = {
            "authenticators": authenticators.data,
            "game_servers": game_servers.data,
            "waiting_line": waiting_line.data,
            "game_result": game_result.data,
            "user_info": user_info.data
        }
        return JsonResponse(ret, safe=False)

    if request.method == 'POST':
        data = JSONParser().parse(request)

        X_Auth_Token = data['X_Auth_Token']
        # X_Auth_Token 튜플이 없으면 새로 생성
        if len(Authenticators.objects.filter(X_Auth_Token=X_Auth_Token)) == 0:
            _ = Authenticators(X_Auth_Token=X_Auth_Token)
            _.save()
        authenticator = Authenticators.objects.get(X_Auth_Token=X_Auth_Token)

        # 기존에 auth_key로 진행 중이던 서버 종료
        auth_key = authenticator.auth_key
        if auth_key is not None:
            delete_objects(GameServers.objects.filter(auth_key=auth_key))
            delete_objects(WaitingLine.objects.filter(auth_key=auth_key))
            delete_objects(GameResult.objects.filter(auth_key=auth_key))
            delete_objects(UserInfo.objects.filter(auth_key=auth_key))
            delete_objects(UserInfo.objects.filter(auth_key=auth_key+'_guess'))

        # 해시 함수를 이용하여 auth_key 생성
        _hash = hashlib.sha1()
        _hash.update(str(time.time()).encode('utf-8'))
        _hash = str(_hash.hexdigest())
        auth_key = _hash[:8] + '-' + _hash[8:12] + '-' + _hash[12:16] + '-' + _hash[16:20] + '-' + _hash[20:32]
        
        # auth_key 수정 후, 저장
        authenticator.auth_key = auth_key
        authenticator.save()

        # 새로운 게임 서버 생성
        problem = data['problem']
        game_server = GameServers(
            auth_key=auth_key,
            problem=int(problem),
            time=0,
            status='ready'
        )
        game_server.save()

        # 유저 생성
        user_number = 30 if problem == 1 else 900
        rand_norm = np.random.normal(40000, 20000, user_number)
        for i in range(user_number):
            grade = int(rand_norm[i])
            if grade < 1000: grade = 1000
            if grade > 100000: grade = 100000
            # 나중에 중복 체크도 해야 됨.
            user_info = UserInfo(auth_key=auth_key, _id=i+1, grade=grade)
            user_info.save()

        ret = {
            'auth_key': auth_key,
            'problem': problem,
            'time': 0
        }
        return JsonResponse(ret, safe=False)

    if request.method == 'DELETE':
        delete_objects(Authenticators.objects.all())
        delete_objects(GameServers.objects.all())
        delete_objects(WaitingLine.objects.all())
        delete_objects(GameResult.objects.all())
        delete_objects(UserInfo.objects.all())

        return HttpResponse('200 OK')


@csrf_exempt
def waiting_line_api(request):
    if request.method == 'GET':
        data = JSONParser().parse(request)

        auth_key = data['Authorization']
        waiting_line = WaitingLineSerializer(WaitingLine.objects.filter(auth_key=auth_key), many=True)
        ret = {
            "waiting_line": waiting_line.data
        }

        return JsonResponse(ret, safe=False)


@csrf_exempt
def game_result_api(request):
    if request.method == 'GET':
        data = JSONParser().parse(request)

        auth_key = data['Authorization']
        game_result = GameResultSerializer(GameResult.objects.filter(auth_key=auth_key), many=True)
        ret = {
            "game_result": game_result.data
        }

        return JsonResponse(ret, safe=False)


@csrf_exempt
def user_info_api(request):
    if request.method == 'GET':
        data = JSONParser().parse(request)

        auth_key = data['Authorization'] + '_guess'
        user_info = UserInfoSerializer(UserInfo.objects.filter(auth_key=auth_key), many=True)
        ret = {
            "user_info": user_info.data
        }

        return JsonResponse(ret, safe=False)

