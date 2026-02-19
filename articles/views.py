from rest_framework import viewsets
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer
from rest_framework.permissions import AllowAny # 👈 On importe la permission "Libre"
from rest_framework.permissions import IsAuthenticated
from .serializers import UserProfileSerializer
from rest_framework import permissions
from rest_framework import filters



# Crée une permission personnalisée
class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Lecture autorisée pour tous (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True
        # Écriture autorisée UNIQUEMENT à l'auteur de l'article
        # return obj.author == request.user
        return obj.author == request.user or request.user.is_staff

class PostViewSet(viewsets.ModelViewSet):
    # On indique à Django quels objets récupérer
    queryset = Post.objects.all().order_by('-created_at')
    # On indique quel traducteur (serializer) utiliser
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    # On ajoute les filtres de recherche
    filter_backends = [filters.SearchFilter]
    # On définit sur quels champs la recherche doit porter
    search_fields = ['title', 'content']
    
    def perform_create(self, serializer):
        # Enregistre automatiquement l'utilisateur connecté comme auteur
        serializer.save(author=self.request.user)
    



class RegisterView(APIView):
    # 🔓 Cette ligne permet à n'importe qui d'accéder à l'inscription
    permission_classes = [AllowAny] 

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Utilisateur créé ! ✅"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UserProfileView(APIView):
    # 🔒 Seul un utilisateur avec un Token valide peut accéder à cette vue
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # On récupère l'utilisateur connecté
        user = request.user
        # On transforme ses données avec le serializer
        serializer = UserProfileSerializer(user)
        # On renvoie le résultat
        return Response(serializer.data)
    
    # 👇 AJOUTE CETTE MÉTHODE POUR LA MODIFICATION
    def patch(self, request):
        user = request.user
        # partial=True permet de ne modifier que certains champs (ex: juste le prénom)
        serializer = UserProfileSerializer(user, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)