from django.db import models
from django.urls import reverse
from django.utils.text import slugify # работает только с латиницей
from django.utils.text import slugify # для работы с кириллицей и латиницей
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.
class DressingRoom(models.Model):
    floor = models.IntegerField()
    number = models.IntegerField()

    def __str__(self):
        return f'Актриса {self.floor} {self.number}'


class Actor(models.Model):
    MALE = 'M'
    FEMALE = 'F'

    GENDERS = [
        (MALE, 'Мужчина'),
        (FEMALE, 'Женщина'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDERS, default=MALE)
    slug = models.SlugField(default='', null=False, db_index=True)
    dressing = models.OneToOneField(DressingRoom, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        if self.gender == self.MALE:
            return f'Актер {self.first_name} {self.last_name}'
        return f'Актриса {self.first_name} {self.last_name}'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.get_full_name(), allow_unicode=True)
        return super().save(*args, **kwargs)

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'
    def get_url(self):
        return reverse('actor-detail', args=(self.slug,))


class Director(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    director_email = models.EmailField()
    slug = models.SlugField(default='', null=False, db_index=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.get_full_name(), allow_unicode=True)
        return super().save(*args, **kwargs)

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'
    def get_url(self):
        return reverse('director-detail', args=(self.slug,))

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Movie(models.Model):
    EURO = 'EUR'
    USD = 'USD'
    RUB = 'RUB'
    YEN = 'YEN'

    CURRENCY_CHOICES = [
        (EURO, 'Euro'),
        (USD, 'Dollar'),
        (RUB, 'Rubles'),
        (YEN, 'Yena')
    ]

    name = models.CharField(max_length=40)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])
    year = models.IntegerField(null=True, blank=True)
    budget = models.IntegerField(default=1000000, validators=[MinValueValidator(1)], blank=True)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default=RUB)
    slug = models.SlugField(default='', null=False, db_index=True)
    director = models.ForeignKey(Director, on_delete=models.CASCADE, null=True, related_name='movies') # rel_name это будет псеводним связи к таблице ( будет использоваться в хтмле)
        # при удалении, каскадно удалит все записи из других таблиц (например все фильмы этого режиссера)
    # director = models.ForeignKey(Director, on_delete=models.SET_NULL, null=True)
        # при удалении, поставит NULL в поле связанных таблиц
    # director = models.ForeignKey(Director, on_delete=models.PROTECT, null=True)
        # не позволит удалить, если поле связазно с другой таблицей
    actors = models.ManyToManyField(Actor, related_name='movies')
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Movie, self).save(*args, **kwargs)

    def get_url(self):
        return reverse('movie-detail', args=(self.slug,))
    def __str__(self):
        return f'{self.name} - {self.rating}%'


# from movie_app.models import Movie