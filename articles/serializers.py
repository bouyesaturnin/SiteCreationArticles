from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Post, Comment
from rest_framework.permissions import AllowAny # 👈 Importation cruciale


class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author_username', 'content', 'created_at']
        read_only_fields = ['author_username']

class PostSerializer(serializers.ModelSerializer):
    # Cette ligne permet d'afficher le pseudo au lieu de l'ID
    author_name = serializers.ReadOnlyField(source='author.username')
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'image', 'author', 'author_name', 'created_at', 'comments']
        # 👇 AJOUTE CETTE LIGNE ABSOLUMENT
        read_only_fields = ['author', 'author_name', 'created_at']

class RegisterSerializer(serializers.ModelSerializer):
    
    # ... ton code actuel ...
    class Meta:
        model = User
        fields = ('username', 'password', 'email')
        extra_kwargs = {'password': {'write_only': True}}
    
    

    def create(self, validated_data):
        # Cette méthode est appelée lors de la sauvegarde
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user
    
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # On choisit les champs que l'on veut exposer
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined']
        # On s'assure que ces données ne sont pas modifiables par erreur ici
        read_only_fields = ['id', 'date_joined']


