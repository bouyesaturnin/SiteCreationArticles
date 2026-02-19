
 
# Register your models here.
from django.contrib import admin
from .models import Post, Comment

class PostAdmin(admin.ModelAdmin):
    # Les colonnes à afficher dans la liste
    list_display = ('title', 'created_at', 'image') 
    
    # Ajouter une barre de recherche sur le titre et le contenu
    search_fields = ('title', 'content')
    
    # Ajouter un filtre sur la date de création
    list_filter = ('created_at',)

# On enregistre le modèle AVEC sa configuration
admin.site.register(Post, PostAdmin)


class CommentAdmin(admin.ModelAdmin):
       list_display = ('post', 'author', 'content', 'created_at' ) 

admin.site.register( Comment, CommentAdmin)


