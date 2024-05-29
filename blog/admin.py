from django.contrib import admin
from .models import Post,Comment,Tag,Category
from django_summernote.admin import SummernoteModelAdmin
# Register your models here.


@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    prepopulated_fields = {'slug' : ('title',)}
    list_filter = ('status', 'published_on',)
    list_display = ('title', 'slug','status','published_on')
    search_fields = ['title','text']
    summernote_fields = ('text',)
    filter_horizontal = ('tags',)  # Makes it easier to manage many-to-many fields in the admin


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
   list_filter = ('created_on','approved',)
   list_display = ('name','body','post','created_on','approved',)
   search_fields = ['name','email','body']
   actions = ['approve_comments']

   def approve_comments(self, request, queryset):
        queryset.update(approved=True)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
  
  
