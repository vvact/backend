from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'star_display', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('product__name', 'user__username')
    ordering = ('-created_at',)

    def star_display(self, obj):
        return '★' * obj.rating + '☆' * (5 - obj.rating)
    star_display.short_description = 'Stars'
