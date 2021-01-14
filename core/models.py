from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.html import format_html

from core.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    email = models.EmailField(db_index=True, unique=True, verbose_name='Email')
    name = models.CharField(max_length=100, verbose_name='Имя')

    is_active = models.BooleanField(default=True, verbose_name='Активен')
    is_superuser = models.BooleanField(default=False, verbose_name='Суперпользователь')
    is_staff = models.BooleanField(default=False, verbose_name='Персонал')

    objects = UserManager()

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        result = super().save(*args, **kwargs)
        if not self.auth_tokens.exists():
            self.auth_tokens.create()
        return result


class Restaurant(models.Model):
    owner = models.ForeignKey('core.User', related_name='restaurants', on_delete=models.CASCADE,
                              verbose_name='Владелец')
    name = models.CharField(max_length=100, verbose_name='Название ресторана')
    city = models.CharField(max_length=100, verbose_name='Город')
    address = models.TextField(verbose_name='Адрес')
    phone = models.CharField(max_length=20, verbose_name='Телефон')

    class Meta:
        verbose_name = 'ресторан'
        verbose_name_plural = 'Рестораны'

    def __str__(self):
        return self.name


class RestaurantImage(models.Model):
    restaurant = models.ForeignKey('core.Restaurant', related_name='restaurant_images', on_delete=models.CASCADE,
                                   verbose_name='Ресторан')
    image = models.ImageField(blank=True, null=True, upload_to='restaurant_images/', verbose_name='Фото ресторана')

    class Meta:
        verbose_name = 'фото ресторана'
        verbose_name_plural = 'Фото ресторанов'

    def __str__(self):
        return f'Фото ресторана {self.restaurant}'


class Place(models.Model):
    restaurant = models.ForeignKey('core.Restaurant', related_name='places', on_delete=models.CASCADE,
                                   verbose_name='Ресторан')
    hall_number = models.PositiveSmallIntegerField(null=True, blank=True, default=1, verbose_name='Номер зала')
    table_number = models.PositiveSmallIntegerField(verbose_name='Номер стола')
    max_places = models.PositiveSmallIntegerField(verbose_name='Максимальное количество мест')
    image = models.ImageField(blank=True, null=True, upload_to='places_images/', verbose_name='Фото стола')

    class Meta:
        verbose_name = 'место'
        verbose_name_plural = 'Места'
        ordering = ['restaurant']

    def __str__(self):
        return f'Стол №{self.table_number}(мест {self.max_places}) - {self.restaurant}'


class Reservation(models.Model):
    restaurant = models.ForeignKey('core.Restaurant', related_name='reservations', on_delete=models.CASCADE,
                                   verbose_name='Ресторан')
    place = models.ForeignKey('core.Place', related_name='reservations', on_delete=models.CASCADE, verbose_name='Место')
    reserved_at = models.DateTimeField(verbose_name='Зарезервировано на')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания записи')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    name = models.CharField(max_length=100, blank=True, null=True, verbose_name='Бронь на имя')
    places = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='Количество мест')

    class Meta:
        verbose_name = 'бронь'
        verbose_name_plural = 'Брони'

    def __str__(self):
        return f'Бронь в {self.restaurant}, мест - {self.places}, бронь на имя - {self.name}'

    def get_phone_as_href(self):
        return format_html(
            '<a href="tel:{}">{}</a>',
            self.phone,
            self.phone,
        )

    get_phone_as_href.short_description = 'Телефон'
