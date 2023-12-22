from django.contrib import admin, messages
from .models import Movie, Director, Actor, DressingRoom
from django.db.models import QuerySet
# Register your models here.


admin.site.register(Actor)
#admin.site.register(DressingRoom)
#admin.site.register(Director)
#admin.site.register(Movie, MovieAdmin) # принудительная регистрация
@admin.register(DressingRoom) # рега через декоратор
class DressingRoomAdmin(admin.ModelAdmin):
    list_display = ['floor', 'number', 'actor'] # первое поле будет ссылкой на объект и не может быть в редакируемом поле снизу


class BudgetFilter(admin.SimpleListFilter):
    title = 'фильтр по бюджету'
    parameter_name = 'budget'

    def lookups(self, request, model_admin):
        return [
            ('<50', 'мало'),
            ('от 50 до 99', 'норм'),
            ('от 100 до 149', 'много'),
            ('>=150', 'дофига'),
        ]
    def queryset(self, request, queryset:QuerySet):
        if self.value()=='<50':
            return queryset.filter(budget__lt=50)
        if self.value()=='от 50 до 99':
            return queryset.filter(budget__gte=50).filter(budget__lt=100)
        if self.value()=='от 100 до 149':
            return queryset.filter(budget__gte=100).filter(budget__lt=150)
        if self.value()=='>=150':
            return queryset.filter(budget__gte=150)
        return queryset
class RatingFilter(admin.SimpleListFilter):
    title = 'фильтр по рейтингу'
    parameter_name = 'rating'
    def lookups(self, request, model_admin):
        return [
            ('<40', 'низкий'),
            ('от 40 до 59', 'средний'),
            ('от 60 до 79', 'высокий'),
            ('>=80', 'высочайший'),
        ]

    def queryset(self, request, queryset:QuerySet):
        if self.value()=='<40':
            return queryset.filter(rating__lt=40)
        if self.value()=='от 40 до 59':
           return queryset.filter(rating__gte=40).filter(rating__lt=60)
        if self.value()=='от 60 до 79':
           return queryset.filter(rating__gte=60).filter(rating__lt=80)
        if self.value()=='>=80':
           return queryset.filter(rating__gte=80)
        return queryset

@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('first_name', 'last_name')}
    list_display = ['first_name', 'last_name', 'slug']
    list_editable = ['slug']


@admin.register(Movie) # рега через декоратор
class MovieAdmin(admin.ModelAdmin):
    #fields = ['name', 'rating']
    #exclude = ['slug']
    #readonly_fields = ['budget'] поле только для чтения, без возможности изменения
    prepopulated_fields = {'slug': ('name', )}
    list_display = ['name', 'rating', 'director', 'budget', 'rating_status'] # первое поле будет ссылкой на объект и не может быть в редакируемом поле снизу
    list_editable = ['rating', 'director', 'budget']
    #ordering = ['-rating', '-name']
    list_per_page = 10
    actions = ['set_dollars', 'set_euros']
    search_fields = ['name__istartswith', 'rating']
    list_filter = ['currency', RatingFilter, BudgetFilter]
    filter_horizontal = ['actors']

    @admin.display(ordering='rating', description='Статус')
    def rating_status(self, mov:Movie):
        if mov.rating < 50:
            return f'зачем это смотреть?!'
        if mov.rating < 70:
            return f'разок можно глянуть'
        if mov.rating <= 85:
            return f'зачет'
        return 'топчик'

    @admin.action(description='Установить валюту в доллар')
    def set_dollars(self, request, qs:QuerySet):
        qs.update(currency=Movie.USD)

    @admin.action(description='Установить валюту в евро')
    def set_euros(self, request, qs:QuerySet):
        count_updated = qs.update(currency=Movie.EURO)
        self.message_user(
            request,
        f'Было обновлено {count_updated} записей',
        messages.ERROR
        )

