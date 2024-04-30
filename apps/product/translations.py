from modeltranslation.translator import translator, TranslationOptions

from .models import (
        Category,
        Tag,
        Product
        )


class ProductTranslationOptions(TranslationOptions):
    fields = ('name', )


class TagTranslationOptions(TranslationOptions):
    fields = ('name', )


class ProductTranslations(TranslationOptions):
    fields = ('name', 'description', )


translator.register(Product, ProductTranslations)
translator.register(Category, TagTranslationOptions)
translator.register(Tag, ProductTranslations)