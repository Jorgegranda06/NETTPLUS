from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Departamento, Colaborador, Marcacion, Horario, Permiso
@receiver(pre_save, sender=Colaborador)
def departamento(sender, instance, **kwargs):
    instance.departamento_ref = Departamento.objects.get_or_create(nombre=instance.departamento)[0] if instance.departamento else None
@receiver(pre_save, sender=Marcacion)
@receiver(pre_save, sender=Horario)
@receiver(pre_save, sender=Permiso)
def colaborador(sender, instance, **kwargs):
    instance.colaborador_ref = Colaborador.objects.filter(empleado_id=instance.empleado_id).first()
@receiver(post_save, sender=Colaborador)
def vincular(sender, instance, **kwargs):
    for model in (Marcacion, Horario, Permiso):
        model.objects.filter(empleado_id=instance.empleado_id).update(colaborador_ref=instance)
