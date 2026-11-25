import { PortalApiService } from "../../core/servicios/portal-api.service";
import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { IonicModule } from '@ionic/angular';
import { ActivatedRoute } from '@angular/router';
import { CrudService } from '../../core/servicios/crud.service';
import { entidades } from '../../core/modelos/entidades';
@Component({standalone:true,imports:[CommonModule,FormsModule,IonicModule],templateUrl:'./crud.page.html'})
export class CrudPage implements OnInit {
 api=inject(CrudService); route=inject(ActivatedRoute);
 departments:any[]=[]; employees:any[]=[]; profile:any=null;
 entity=''; records:any[]=[]; form:any={}; id:number|null=null; mode='list'; error=''; notice=''; query='';
 roles=["Recursos Humanos","Contabilidad","Desarrollo Organizacional","Consulta","Administrador"];
 canEdit=false;
 get fields(){return Object.keys(entidades[this.entity]||{});}
 get visible(){return this.records.filter(r=>JSON.stringify(r).toLowerCase().includes(this.query.toLowerCase()));}
 ngOnInit(){this.apiAccess();this.route.paramMap.subscribe(p=>{this.entity=this.route.snapshot.data['entidad']||p.get('entidad')||'';this.load();this.api.list("departamentos").subscribe({next:r=>this.departments=r,error:()=>{}});this.api.list("colaboradores").subscribe({next:r=>this.employees=r,error:()=>{}});});}
 apiAccess(){this.portal.get<any>("/api/me").subscribe({next:r=>this.canEdit=this.entity==="cuentas"?r.usuario.rol==="Administrador":["Administrador","Recursos Humanos"].includes(r.usuario.rol)});}
 portal=inject(PortalApiService);
 labels:Record<string,string>={empleado_id:'Código de empleado',nombre:'Nombre',empresa:'Empresa',departamento:'Departamento',cargo:'Cargo',activo:'Estado',fecha:'Fecha',hora:'Hora',tipo_marcacion:'Movimiento',tipo:'Tipo',dia_semana:'Día de la semana (0 = lunes)',hora_entrada:'Entrada',hora_salida:'Salida',tolerancia_min:'Tolerancia (minutos)',nombres:'Nombres',apellidos:'Apellidos',fecha_inicio:'Inicio',fecha_fin:'Fin',estado:'Estado',codigo_pago:'Código de pago',username:'Usuario',first_name:'Nombres',last_name:'Apellidos',email:'Correo',is_active:'Estado',password:'Contraseña',rol:'Rol'};
 label(k:string){return this.labels[k]||k;}
 display(v:any){return typeof v==='boolean'?(v?'Activo':'Inactivo'):v;}
 fail(e:any){this.notice='';const d=e.error||e.message;this.error=typeof d==='object'&&d!==null?Object.entries(d).map(([k,v])=>this.label(k)+': '+(Array.isArray(v)?v.join(', '):String(v))).join(' · '):String(d); }
 load(){this.mode='list';this.profile=null;this.error='';this.records=[];if(entidades[this.entity])this.api.list(this.entity).subscribe({next:r=>this.records=r,error:e=>this.fail(e)});}
 create(){this.id=null;this.form={...entidades[this.entity]};this.mode='edit';this.error='';this.notice='';}
 detail(id:number,edit=false){this.error='';this.notice='';this.api.detail(this.entity,id).subscribe({next:r=>{this.id=id;this.form={...r};for(const k of this.fields)if(k.startsWith('fecha_')&&this.form[k])this.form[k]=this.form[k].slice(0,16);this.mode=edit?'edit':'detail';if(!edit&&this.entity==='colaboradores')this.api.profile(r.empleado_id).subscribe({next:x=>this.profile=x,error:e=>this.fail(e)});},error:e=>this.fail(e)});}
 type(k:string){return k==='password'?'password':k==='fecha'?'date':k.startsWith('fecha_')?'datetime-local':k.startsWith('hora')?'time':['dia_semana','tolerancia_min'].includes(k)?'number':'text';}
 save(){const d:any={};for(const k of this.fields)if(!(k==='password'&&!this.form[k]&&this.id!==null))d[k]=this.form[k];this.api.save(this.entity,this.id,d).subscribe({next:()=>{this.notice='Registro guardado';this.load();},error:e=>this.fail(e)});}
 remove(id:number){if(confirm('¿Eliminar este registro?'))this.api.remove(this.entity,id).subscribe({next:()=>{this.notice='Registro eliminado';this.load();},error:e=>this.fail(e)});}
}
