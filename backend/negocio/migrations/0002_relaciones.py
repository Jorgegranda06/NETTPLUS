from django.db import migrations, models
import django.db.models.deletion

def vincular(apps, schema_editor):
    D=apps.get_model('negocio','Departamento'); C=apps.get_model('negocio','Colaborador')
    for c in C.objects.all():
        if c.departamento:
            c.departamento_ref=D.objects.get_or_create(nombre=c.departamento)[0]; c.save(update_fields=['departamento_ref'])
        for name in ('Marcacion','Horario','Permiso'):
            apps.get_model('negocio',name).objects.filter(empleado_id=c.empleado_id).update(colaborador_ref=c)
class Migration(migrations.Migration):
    dependencies=[('negocio','0001_initial')]
    operations=[migrations.AddField(model_name='colaborador',name='departamento_ref',field=models.ForeignKey(blank=True,null=True,on_delete=django.db.models.deletion.SET_NULL,to='negocio.departamento'))]+[migrations.AddField(model_name=n,name='colaborador_ref',field=models.ForeignKey(blank=True,null=True,on_delete=django.db.models.deletion.SET_NULL,to='negocio.colaborador')) for n in ('marcacion','horario','permiso')]+[migrations.RunPython(vincular,migrations.RunPython.noop)]
