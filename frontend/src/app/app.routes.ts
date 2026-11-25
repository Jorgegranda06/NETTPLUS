import { Routes } from '@angular/router';
import { Component } from '@angular/core';
import { DepartamentosPage } from './paginas/departamentos/departamentos.page';
import { ColaboradoresPage } from './paginas/colaboradores/colaboradores.page';
import { MarcacionesPage } from './paginas/marcaciones/marcaciones.page';
import { HorariosPage } from './paginas/horarios/horarios.page';
import { PermisosPage } from './paginas/permisos/permisos.page';
import { UsuariosPage } from './paginas/usuarios/usuarios.page';
@Component({standalone:true,template:''})
export class EmptyPage {}
export const routes: Routes = [{path:'',component:EmptyPage,pathMatch:'full'},{path:'gestion/departamentos',component:DepartamentosPage,data:{entidad:'departamentos'}},{path:'gestion/colaboradores',component:ColaboradoresPage,data:{entidad:'colaboradores'}},{path:'gestion/marcaciones',component:MarcacionesPage,data:{entidad:'marcaciones'}},{path:'gestion/horarios',component:HorariosPage,data:{entidad:'horarios'}},{path:'gestion/permisos',component:PermisosPage,data:{entidad:'permisos'}},{path:'gestion/cuentas',component:UsuariosPage,data:{entidad:'cuentas'}}];