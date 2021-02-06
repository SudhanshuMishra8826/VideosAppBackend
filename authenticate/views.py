from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import exceptions
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import ensure_csrf_cookie
from .serializers import UserSerializer
from django.views.decorators.csrf import csrf_protect
from .utils import generate_access_token, generate_refresh_token
import jwt
@api_view(['POST'])
@permission_classes([AllowAny])
@ensure_csrf_cookie
def doLogin(request):
    User = get_user_model()
    email = request.data.get('email')
    password = request.data.get('password')
    response = Response()
    if (email is None) or (password is None):
        raise exceptions.AuthenticationFailed(
            'username and password required')
    user = User.objects.filter(email=email).first()
    if(user is None):
        raise exceptions.AuthenticationFailed('user not found')
    if (not user.check_password(password)):
        raise exceptions.AuthenticationFailed('wrong password')
    serialized_user = UserSerializer(user).data
    access_token = generate_access_token(user)
    refresh_token = generate_refresh_token(user)
    response.set_cookie(key='refreshtoken', value=refresh_token, httponly=True)
    response.data = {
        'access_token': access_token,
        'refreshtoken': refresh_token,
        'user': serialized_user,
    }
    return response

