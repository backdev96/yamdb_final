from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from users.models import CustomUser
from .permissions import IsAdminPermission
from .serializers import ConfirmCodeSerializer, CustomUserSerializer
from api_yamdb import settings


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def obtain_conf_code(request):
    ''' Получение confirmation code.
    Метод для передачи запроса - POST, запрос разрешен любому пользователю.
    В случае успешного запроса пользователю отправляется confirmation code
    на электронный адрес, указанный в запросе.

    '''
    if not CustomUser.objects.filter(email=request.data['email']).exists():
        ''' Проверяет наличие пользователя с электронным адресом,
        переданным в запросе.

        '''
        return Response(status=status.HTTP_204_NO_CONTENT)

    user = get_object_or_404(CustomUser, email=request.data['email'])
    # генерирование confirmation code через генератор токенов
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        'Yamdb: Comfirmation code',
        f'Your confirmation code is {confirmation_code}',
        settings.DEFAULT_FROM_EMAIL,  # адрес отправки прописан в настройках
        [f"{request.data['email']}"],
        fail_silently=False,
    )
    return Response({'Check you email.'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def obtain_token(request):
    ''' Получение токена.
    Сравнивается пользователь и ранее выданный confirmation code.

    '''
    email = request.data['email']
    user = get_object_or_404(CustomUser, email=email)
    confirmation_code = request.data['confirmation_code']
    # проверка соответствия confirmation code и пользователя
    if not default_token_generator.check_token(user, confirmation_code):
        return Response(status=status.HTTP_403_FORBIDDEN)
    # создание токена
    token = AccessToken.for_user(user)
    return Response({
        'token': str(token)},
        status=status.HTTP_200_OK)


@api_view(['POST'])
def refresh_token(request):
    ''' Обновление токена.
    Сравнивается пользователь и confirmation code, выданный ранее.

    '''
    serializer = ConfirmCodeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.data.get('email')
    confirmation_code = serializer.data.get('confirmation_code')
    user = get_object_or_404(CustomUser, email=email)
    if default_token_generator.check_token(user, confirmation_code):
        token = RefreshToken.for_user(user)
        return Response({'token': f'{token}'}, status=status.HTTP_200_OK)
    return Response(
        {'confirmation_code': 'Неверный код подтверждения'},
        status=status.HTTP_400_BAD_REQUEST
    )


class CustomUserViewSet(viewsets.ModelViewSet):
    ''' Вьюсет для обработки запросов к /users.

    Поле для поиска объектов - username.

    '''
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    lookup_field = 'username'
    permission_classes = (permissions.IsAuthenticated,
                          IsAdminPermission,)

    @action(methods=['patch', 'get'], detail=False,
            permission_classes=[permissions.IsAuthenticated], url_name='me',
            url_path='me'
            )
    def my_profile(self, request):
        ''' Описание запросов типа users/me.
        Декоратор @action описывает допустимые методы, пермишены,
        определяет часть url, к которой относится. Флаг detail=False
        говорит о том, что метод распространяется не на отдельный объект,
        а на всю коллекцию.

        '''
        if request.method == 'GET':
            serializer = CustomUserSerializer(self.request.user)
        else:
            serializer = CustomUserSerializer(self.request.user,
                                              data=request.data,
                                              partial=True
                                              )
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return Response(serializer.data)
