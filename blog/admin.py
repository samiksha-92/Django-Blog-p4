from django.contrib import admin
from .models import Post,Comment
from django_summernote.admin import SummernoteModelAdmin
# Register your models here.


@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    prepopulated_fields = {'slug' : ('title',)}
    list_filter = ('status', 'published_on',)
    list_display = ('title', 'slug','status','published_on')
    search_fields = ['title','text']
    summernote_fields = ('text',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
   list_filter = ('created_on','approved',)
   list_display = ('name','body','post','created_on','approved',)
   search_fields = ['name','email','body']
   acttions = ['approve_comments']

   def approve_comments(self, request, queryset):
        queryset.update(approved=True)




  
  
