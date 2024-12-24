from django.contrib import admin, messages
from .models import Movie
from django.db.models import QuerySet
# Register your models here.


class RatingFilter(admin.SimpleListFilter):
    title = 'Фильтр по рэйтингу'
    parameter_name = 'rating'
    def lookups(self, request, model_admin):
        return [
            ('<40', 'низкий'),
            ('от 40 до 59', 'средний'),
            ('от 60 до 79', 'высокий'),
            ('>=80', 'высочайший'),
        ]

    def queryset(self, request, queryset: QuerySet):
        if self.value() == '<40':
            return queryset.filter(rating__lt=40)
        if self.value() == 'от 40 до 59':
            return queryset.filter(rating__gte=40).filter(rating__lt=60)
        if self.value() == 'от 60 до 79':
            return queryset.filter(rating__gte=60).filter(rating__lt=79)
        if self.value() == '>=80':
            return queryset.filter(rating__gte=80)




@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['name', 'rating', 'currency', 'budget', 'rating_status']
    list_editable = ['rating', 'currency', 'budget']
    actions = ['set_dollars', 'set_euro']
    #ordering = ['-rating']
    list_per_page = 10
    search_fields = ['name__startswith']
    list_filter = ['name', 'currency', RatingFilter]

    @admin.display(ordering='rating', description='Статус')
    def rating_status(self, mov: Movie):
        if mov.rating < 50:
            return 'Зачем это смотреть?!'
        if mov.rating < 70:
            return 'Разок можно глянуть'
        if mov.rating <= 85:
            return 'Зачет'
        return 'Топчик'

    @admin.action(description='Установить валюту в доллар')
    def set_dollars(self, request, qs: QuerySet):
        qs.update(currency=Movie.USD)

    @admin.action(description='Установить валюту в евро')
    def set_euro(self, request, qs: QuerySet):
        count_updated = qs.update(currency=Movie.EUR)
        self.message_user(request,
            f'Было обновлено {count_updated} записей')
        messages.ERROR
