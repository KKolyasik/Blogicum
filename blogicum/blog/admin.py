from django.contrib import admin
from blog.models import Category, Location, Post, Comments


class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'text',
        'pub_date',
        'author',
        'location',
        'category',
        'is_published',
        'created_at',
    )
    list_editable = (
        'text',
        'location',
        'category',
        'is_published',
    )
    list_filter = (
        'pub_date',
        'created_at',
        'category',
    )


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'description',
        'slug',
    )
    list_editable = (
        'description',
        'slug',
    )


class CommentsAdmin(admin.ModelAdmin):
    list_display = (
        'text',
        'post',
        'author',
        'created_at',
    )


admin.site.register(Category, CategoryAdmin)
admin.site.register(Location)
admin.site.register(Post, PostAdmin)
admin.site.register(Comments, CommentsAdmin)
