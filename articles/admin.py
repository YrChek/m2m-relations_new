from django.contrib import admin

from .models import Article, Scope, ArticleScope

from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet


class ArticleScopeInlineFormset(BaseInlineFormSet):
    def clean(self):
        counter = 0
        for form in self.forms:
            if form.cleaned_data and form.cleaned_data['is_main']:
                counter += 1

        if counter == 0:
            raise ValidationError('Выберите основной раздел статьи')

        if counter > 1:
            raise ValidationError('Основным может быть только один раздел')
        return super().clean()


class ArticleScopeInline(admin.TabularInline):
    model = ArticleScope
    formset = ArticleScopeInlineFormset


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ArticleScopeInline, ]


@admin.register(Scope)
class ScopeAdmin(admin.ModelAdmin):
    pass


@admin.register(ArticleScope)
class ArticleScopeAdmin(admin.ModelAdmin):
    list_display = ['tag', 'article', 'is_main']
