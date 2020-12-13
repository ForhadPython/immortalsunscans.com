from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin

from product.models import Product, Chapter, ChapterImage


# Register your models here.


class ChapterInline(admin.TabularInline):
    model = Chapter
    extra = 0


class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'image_tag']
    readonly_fields = ('image_tag',)
    inlines = [ChapterInline]
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Product, ProductAdmin)


class ChapterImageInline(admin.TabularInline):
    model = ChapterImage
    extra = 0


class ChapterModel(admin.ModelAdmin):
    list_display = ["__str__"]
    search_fields = ["__str__"]
    inlines = [ChapterImageInline]

    class Meta:
        Model = Chapter


admin.site.register(Chapter, ChapterModel)
