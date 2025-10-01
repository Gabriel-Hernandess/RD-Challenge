from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Probe
from .serializers import ProbeSerializer, ProbeCreateSerializer, ProbeMoveSerializer
from .services import move_probe, InvalidCommandError
from django.shortcuts import render, redirect
from django.views import View
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

class ProbeViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    """
    ViewSet para gerenciar sondas:
    - list: listar todas as sondas
    - create: lançar nova sonda
    - move (custom action): mover sonda existente
    - destroy: deletar sonda

    Necessario autenticacao (jwt em cookies)
    """

    def list(self, request):
        probes = Probe.objects.all()
        serializer = ProbeSerializer(probes, many=True)
        return Response({'probes': serializer.data})
    
    def retrieve(self, request, pk=None):
        probe = get_object_or_404(Probe, pk=pk)
        serializer = ProbeSerializer(probe)
        return Response(serializer.data)

    def create(self, request):
        serializer = ProbeCreateSerializer(data=request.data)
        if serializer.is_valid():
            probe = serializer.save()
            return Response(ProbeSerializer(probe).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['put'])
    def move(self, request, pk=None):
        """
        Recebe {"commands": "MRML"} e atualiza a posição da sonda
        """
        probe = get_object_or_404(Probe, pk=pk)
        serializer = ProbeMoveSerializer(data=request.data)
        if serializer.is_valid():
            commands = serializer.validated_data['commands'].upper()
            try:
                move_probe(probe, commands)
            except InvalidCommandError as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
            return Response(ProbeSerializer(probe).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        probe = get_object_or_404(Probe, pk=pk)
        probe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class DashboardView(View):
    template_name = "probes/dashboard.html"

    def get(self, request):
        access_token = request.COOKIES.get("access_token")
        if not access_token:
            return redirect("/login/")

        # Validar token
        jwt_auth = JWTAuthentication()
        try:
            validated_token = jwt_auth.get_validated_token(access_token)
            user = jwt_auth.get_user(validated_token)
        except (TokenError, InvalidToken):
            return redirect("/login/")

        # Buscar sondas
        probes = Probe.objects.all()
        return render(request, self.template_name, {"probes": probes})