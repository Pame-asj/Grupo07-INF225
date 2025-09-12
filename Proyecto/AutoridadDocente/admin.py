from django.contrib import admin
from .models import Tema, Pregunta, Ensayo, Tag

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name", "slug")

admin.site.register(Tema)
admin.site.register(Pregunta)
admin.site.register(Ensayo)
