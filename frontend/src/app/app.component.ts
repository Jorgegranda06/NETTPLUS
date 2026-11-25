import { PortalApiService } from './core/servicios/portal-api.service';
import { Router, RouterOutlet } from '@angular/router';
import { IonicModule } from '@ionic/angular';
import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpErrorResponse } from '@angular/common/http';

type User = {id:number;nombre:string;usuario:string;rol:string;activo?:number};
type Summary = {marcaciones:number;colaboradores:number;importaciones:number;ultimas:History[]};
type History = {archivo:string;fecha:string;total:number;insertados:number;duplicados:number;rechazados:number};
type ImportResult = {mensaje:string;total:number;insertados:number;duplicados:number;rechazados:number;errores:{fila:number;motivo:string}[]};

@Component({selector:'app-root',standalone:true,imports:[CommonModule,FormsModule,IonicModule,RouterOutlet],templateUrl:'./app.component.html'})
export class AppComponent implements OnInit {
  private http=inject(PortalApiService);
  private router=inject(Router);
  user:User|null=null;
  username='admin';password='';loading=false;notice='';error='';
  page='dashboard';menuOpen=false;
  summary:Summary={marcaciones:0,colaboradores:0,importaciones:0,ultimas:[]};
  file:File|null=null;auxFile:File|null=null;auxType='solicitudes';importResult:ImportResult|null=null;resultSource:''|'marcaciones'|'auxiliar'='';resultFileName='';
  colaboradoresS2:any[]=[]; asistenciaS2:any[]=[]; noIdentificadasS2:any[]=[];
  colaboradoresParaHorario:any[]=[];
  permisosS2:any[]=[]; horariosS2:any[]=[];
  indicadoresS2:any={marcaciones:0,empleados_identificados:0,dias_con_marcaciones:0};
  filtroEmpleado=''; filtroNombre=''; estadoS2='';
  fichaLaboral:any=null; horarioNuevo={empleado_id:'',dia_semana:0,hora_entrada:'08:00',hora_salida:'17:00',tolerancia_min:0};
  atrasosS2:any[]=[];resumenAtrasos:any={total_atrasos:0,dias_evaluados:0,dias_sin_horario:0,criterio:''};
  diasSemana=['Lunes','Martes','Miércoles','Jueves','Viernes','Sábado','Domingo'];
  users:User[]=[];newUser={nombre:'',usuario:'',password:'',rol:'Recursos Humanos'};
  reporteFiltros={desde:'',hasta:'',empleado_id:'',departamento:''};
  reporteDatos:any=null; reporteError=''; historialCompleto:History[]=[];
  consultarReporte(){this.reporteError='';this.reporteDatos=null;this.http.get<any>('/api/reportes/',{params:this.reporteFiltros}).subscribe({next:r=>this.reporteDatos=r,error:e=>this.reporteError=e.error?.error||'No se pudo consultar el reporte'});}
  descargarReporte(){this.reporteError='';this.http.download('/api/reportes/',{...this.reporteFiltros,formato:'xlsx'}).subscribe({next:b=>{const url=URL.createObjectURL(b);const a=document.createElement('a');a.href=url;a.download='NETTPLUS_reporte.xlsx';a.click();setTimeout(()=>URL.revokeObjectURL(url),30000);},error:()=>this.reporteError='No se pudo descargar el reporte'});}
  nav=[
    {group:'GENERAL',items:[{id:'dashboard',label:'Panel principal',icon:'▦',sprint:1},{id:'importaciones',label:'Importar archivos',icon:'⇧',sprint:1},{id:'historial',label:'Historial de importación',icon:'▤',sprint:1}]},
    {group:'GESTIÓN DE PERSONAL',items:[{id:'departamentos',label:'Departamentos',icon:'▤',sprint:1},{id:'colaboradores',label:'Colaboradores',icon:'♙',sprint:2},{id:'horarios',label:'Horarios',icon:'◷',sprint:2},{id:'marcaciones',label:'Marcaciones',icon:'▣',sprint:1},{id:'asistencia',label:'Asistencia y atrasos',icon:'▣',sprint:2},{id:'novedades',label:'Novedades y permisos',icon:'◈',sprint:2}]},
    {group:'ANÁLISIS Y REPORTES',items:[{id:'indicadores',label:'Indicadores',icon:'◫',sprint:2},{id:'reportes',label:'Reportes',icon:'▤',sprint:1}]},
    {group:'ADMINISTRACIÓN',items:[{id:'usuarios',label:'Usuarios y accesos',icon:'⚙',sprint:1},{id:'auditoria',label:'Auditoría',icon:'▤',sprint:1}]}
  ];
  gestion:Record<string,string>={departamentos:'departamentos',colaboradores:'colaboradores',horarios:'horarios',marcaciones:'marcaciones',novedades:'permisos',usuarios:'cuentas'};
  entities:any={departamentos:{nombre:''},colaboradores:{empleado_id:'',nombre:'',empresa:'',departamento:'',cargo:'',activo:true},marcaciones:{empleado_id:'',nombre:'',departamento:'',fecha:'',hora:'',tipo_marcacion:'Entrada',tipo:''},horarios:{empleado_id:'',dia_semana:0,hora_entrada:'08:00',hora_salida:'17:00',tolerancia_min:5},permisos:{empleado_id:'',nombres:'',apellidos:'',departamento:'',fecha_inicio:'',fecha_fin:'',estado:'Pendiente',codigo_pago:''}};
  entity='colaboradores'; records:any[]=[]; form:any={}; editId:number|null=null;
  get fields(){return Object.keys(this.entities[this.entity]);}
  loadCrud(){this.editId=null;this.form={...this.entities[this.entity]};this.http.get<any[]>('/api/'+this.entity+'/').subscribe({next:r=>this.records=r,error:e=>this.error=JSON.stringify(e.error)});}
  editCrud(id:number){this.http.get<any>('/api/'+this.entity+'/'+id+'/').subscribe({next:r=>{this.editId=id;this.form=r},error:e=>this.error=JSON.stringify(e.error)});}
  saveCrud(){const url='/api/'+this.entity+'/'+(this.editId?this.editId+'/':'');const data=Object.fromEntries(this.fields.map(k=>[k,this.form[k]]));(this.editId?this.http.put(url,data):this.http.post(url,data)).subscribe({next:()=>{this.notice='Guardado';this.error='';this.loadCrud()},error:e=>this.error=JSON.stringify(e.error)});}
  deleteCrud(id:number){if(!confirm('Eliminar registro de prueba?'))return;this.http.delete('/api/'+this.entity+'/'+id+'/').subscribe({next:()=>this.loadCrud(),error:e=>this.error=JSON.stringify(e.error)});}
  get pageTitle(){return this.nav.flatMap(n=>n.items).find(n=>n.id===this.page)?.label || 'Panel principal'}
  get sprint(){return this.nav.flatMap(n=>n.items).find(n=>n.id===this.page)?.sprint || 1}
  get canImport(){return this.user?.rol==='Administrador'||this.user?.rol==='Recursos Humanos'}
  get isAdmin(){return this.user?.rol==='Administrador'}
  ngOnInit(){if(sessionStorage.getItem('nettplus_token'))this.http.get<{usuario:User}>('/api/me').subscribe({next:r=>{this.user=r.usuario;this.refresh();this.cargarSprint2()},error:()=>sessionStorage.removeItem('nettplus_token')});}
  login(){this.loading=true;this.error='';this.http.post<{token:string;usuario:User}>('/api/login',{usuario:this.username,password:this.password}).subscribe({next:r=>{sessionStorage.setItem('nettplus_token',r.token);this.user=r.usuario;this.password='';this.loading=false;this.refresh();this.cargarSprint2()},error:(e:HttpErrorResponse)=>{this.error=e.error?.error||'No se pudo iniciar sesión';this.loading=false}})}
  logout(){this.http.post('/api/logout',{}).subscribe({next:()=>this.clearSession(),error:()=>this.clearSession()});}
  clearSession(){this.router.navigateByUrl('/');sessionStorage.removeItem('nettplus_token');this.user=null;this.page='dashboard';this.error='';this.notice='';}
  auditoriaDatos:any[]=[];
  cargarAuditoria(){this.http.get<any>("/api/auditoria/").subscribe({next:r=>this.auditoriaDatos=r.registros,error:()=>this.error="No se pudo consultar auditoría"});}
  go(id:string){if(["usuarios","auditoria"].includes(id)&&!this.isAdmin)return;if(id==="auditoria")this.cargarAuditoria();this.router.navigateByUrl(this.gestion[id]?'/gestion/'+this.gestion[id]:'/');this.page=id;this.error='';this.notice='';this.menuOpen=false;if(id==='crud')this.loadCrud();if(id==='usuarios')this.getUsers();if(id==='dashboard'||id==='historial')this.refresh();if(['colaboradores','asistencia','horarios','indicadores','novedades'].includes(id))this.cargarSprint2()}
  cargarSprint2(){
    this.estadoS2='';
    this.http.get<{colaboradores:any[]}>('/api/sprint2/colaboradores',{params:{q:this.filtroNombre}}).subscribe({next:r=>this.colaboradoresS2=r.colaboradores,error:()=>this.estadoS2='No se pudo consultar colaboradores'});
    this.http.get<{marcaciones:any[]}>('/api/sprint2/asistencia',{params:{empleado_id:this.filtroEmpleado}}).subscribe({next:r=>this.asistenciaS2=r.marcaciones,error:()=>this.estadoS2='No se pudo consultar marcaciones'});
    this.http.get<any>('/api/sprint2/indicadores').subscribe({next:r=>this.indicadoresS2=r});
    this.http.get<{colaboradores:any[]}>('/api/sprint2/no-identificadas').subscribe({next:r=>this.noIdentificadasS2=r.colaboradores});
    this.http.get<{horarios:any[]}>('/api/sprint2/horarios').subscribe({next:r=>this.horariosS2=r.horarios,error:()=>this.estadoS2='No se pudieron consultar horarios'});
    this.http.get<{colaboradores:any[]}>('/api/sprint2/colaboradores').subscribe({next:r=>this.colaboradoresParaHorario=r.colaboradores,error:()=>this.estadoS2='No se pudo cargar la lista de colaboradores'});
    this.http.get<any>('/api/sprint2/atrasos',{params:{empleado_id:this.filtroEmpleado}}).subscribe({next:r=>{this.atrasosS2=r.atrasos;this.resumenAtrasos=r},error:()=>this.estadoS2='No se pudieron calcular atrasos'});
    this.http.get<{permisos:any[]}>('/api/sprint2/permisos').subscribe({next:r=>this.permisosS2=r.permisos});
  }
  verFicha(empleado_id:string){
    this.fichaLaboral=null;
    this.http.get<any>('/api/sprint2/colaboradores/'+encodeURIComponent(empleado_id)+'/laboral').subscribe({
      next:r=>this.fichaLaboral=r,error:()=>this.estadoS2='No se pudo consultar la ficha laboral'
    });
  }
  nombreColaborador(id:string):string {
    const c=this.colaboradoresS2.find(c=>String(c.empleado_id)===String(id));
    return c?.nombre || 'Sin coincidencia';
  }
  guardarHorario(){
    this.estadoS2='';
    if(!this.horarioNuevo.empleado_id){this.estadoS2='Selecciona un colaborador';return;}
    this.http.post('/api/sprint2/horarios',this.horarioNuevo).subscribe({
      next:()=>{this.estadoS2='Horario guardado (pendiente de validación con RRHH)';this.cargarSprint2()},
      error:e=>this.estadoS2=e.error?.error||'No se pudo guardar horario'
    });
  }
  eliminarHorario(id:number){
    this.http.delete('/api/sprint2/horarios/'+id).subscribe({
      next:()=>this.cargarSprint2(),error:()=>this.estadoS2='No se pudo eliminar horario'
    });
  }
  refresh(){this.http.get<{importaciones:History[]}>('/api/importaciones').subscribe({next:r=>this.historialCompleto=r.importaciones,error:()=>{}});this.http.get<Summary>('/api/resumen').subscribe({next:r=>this.summary=r,error:()=>{}})}
  clearImportResult(){this.importResult=null;this.resultSource='';this.resultFileName='';this.notice='';this.error='';}
  chooseFile(e:Event,aux=false){const file=(e.target as HTMLInputElement).files?.[0]||null;if(aux)this.auxFile=file;else this.file=file;this.error='';this.notice='';this.importResult=null;this.resultSource='';this.resultFileName=''}
  upload(){if(!this.file)return;this.loading=true;this.error='';this.notice='';this.importResult=null;const form=new FormData();form.append('archivo',this.file);this.http.post<ImportResult>('/api/importar/marcaciones',form).subscribe({next:r=>{this.importResult=r;this.resultSource='marcaciones';this.resultFileName=this.file?.name||'Marcaciones';this.notice=r.mensaje;this.loading=false;this.refresh()},error:(e:HttpErrorResponse)=>{this.error=e.error?.error||'Error al importar';this.loading=false}})}
  uploadAux(){if(!this.auxFile)return;this.error='';this.notice='';this.importResult=null;this.resultSource='';const form=new FormData();form.append('archivo',this.auxFile);form.append('categoria',this.auxType);this.loading=true;this.http.post<ImportResult>(('/api/importar/' + this.auxType),form).subscribe({next:r=>{this.notice=r.mensaje;this.importResult=r;this.resultSource='auxiliar';this.resultFileName=this.auxFile?.name||'Archivo complementario';this.loading=false;this.cargarSprint2()},error:(e:HttpErrorResponse)=>{this.error=e.error?.error||'Error';this.loading=false}})}
  getUsers(){if(!this.isAdmin)return;this.http.get<{usuarios:User[]}>('/api/usuarios').subscribe({next:r=>this.users=r.usuarios,error:(e:HttpErrorResponse)=>this.error=e.error?.error||'Error al cargar usuarios'})}
  createUser(){this.error='';this.notice='';this.http.post('/api/usuarios',this.newUser).subscribe({next:()=>{this.notice='Usuario creado correctamente';this.newUser={nombre:'',usuario:'',password:'',rol:'Recursos Humanos'};this.getUsers()},error:(e:HttpErrorResponse)=>this.error=e.error?.error||'Error al crear usuario'})}
}

