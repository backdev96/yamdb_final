from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    ''' Создание изменнного класса на замену классу User.

    Класс наследуется от класса AbstractUser путем добавления необходимых полей
    и переопределения предустановленного поля email.
    Важно прописать эту модель в файле настроек как модель пользователей
    для всего проекта AUTH_USER_MODEL = 'users.CustomUser'
    Модель создается и настраивается ДО первой миграции.

    '''
    class UserStatus(models.TextChoices):
        ''' Организация выбора из предустановленных значений в поле role.

        '''
        USER = 'user'
        MODERATOR = 'moderator'
        ADMIN = 'admin'

    first_name = models.CharField(verbose_name='Имя', max_length=30,
                                  blank=True)
    last_name = models.CharField(verbose_name='Фамилия', max_length=150,
                                 blank=True)
    role = models.CharField(verbose_name='Роль пользователя',
                            max_length=30, choices=UserStatus.choices,
                            default=UserStatus.USER)
    bio = models.TextField(verbose_name='О себе', blank=True)
    email = models.EmailField(verbose_name='email address', blank=True,
                              unique=True)

    @property
    def is_moderator(self):
        ''' Преобразование функции в свойство класса.

        Упростит создание пермишена.

        '''
        return self.role == self.UserStatus.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.UserStatus.ADMIN or self.is_superuser
