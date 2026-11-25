from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import serializers,viewsets,permissions
from django.contrib.auth.models import Group
from django.db import transaction
from .models import Auditoria
U=get_user_model()
ROLES=["Administrador","Recursos Humanos","Contabilidad","Desarrollo Organizacional","Consulta"]
class UsuarioSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True,required=False,min_length=8)
    rol=serializers.ChoiceField(choices=ROLES,required=False)
    def to_representation(self,obj):
        data=super().to_representation(obj)
        data["rol"]="Administrador" if obj.is_superuser else (obj.groups.first().name if obj.groups.exists() else "Consulta")
        return data
    class Meta:
        model=U
        fields=['id','username','first_name','last_name','email','is_active','password','rol']
    def validate_password(self,value):
        try: validate_password(value)
        except ValidationError as e: raise serializers.ValidationError(e.messages)
        return value
    def validate(self,data):
        if not self.instance and not data.get('password'): raise serializers.ValidationError({'password':'Obligatoria'})
        if self.instance and self.instance.is_superuser and data.get('is_active') is False: raise serializers.ValidationError('No desactive un administrador')
        if data.get("rol")=="Administrador" and not (self.instance and self.instance.is_superuser): raise serializers.ValidationError({"rol":"Los superusuarios se crean mediante Django Admin"})
        if self.instance and self.instance.is_superuser and data.get("rol","Administrador")!="Administrador": raise serializers.ValidationError({"rol":"No se puede cambiar este perfil"})
        return data
    @transaction.atomic
    def create(self,data):
        rol=data.pop("rol","Consulta"); obj=U.objects.create_user(**data); obj.groups.set([Group.objects.get_or_create(name=rol)[0]]); return obj
    @transaction.atomic
    def update(self,obj,data):
        rol=data.pop("rol",None)
        password=data.pop('password',None)
        for k,v in data.items(): setattr(obj,k,v)
        if password: obj.set_password(password)
        obj.save()
        if rol and not obj.is_superuser: obj.groups.set([Group.objects.get_or_create(name=rol)[0]])
        return obj
class SoloAdmin(permissions.BasePermission):
    def has_permission(self,r,v): return r.user.is_authenticated and r.user.is_superuser
class UsuarioViewSet(viewsets.ModelViewSet):
    queryset=U.objects.all().order_by('pk')
    serializer_class=UsuarioSerializer
    permission_classes=[SoloAdmin]
    def perform_create(self,s):
        obj=s.save(); Auditoria.objects.create(usuario=self.request.user.username,accion=f"Crear cuenta #{obj.pk}")
    def perform_update(self,s):
        obj=s.save(); Auditoria.objects.create(usuario=self.request.user.username,accion=f"Actualizar cuenta #{obj.pk}")
    def perform_destroy(self,obj):
        if obj.is_superuser or obj.pk==self.request.user.pk: raise serializers.ValidationError('No se puede eliminar este administrador')
        pk=obj.pk; obj.delete(); Auditoria.objects.create(usuario=self.request.user.username,accion=f"Eliminar cuenta #{pk}")

