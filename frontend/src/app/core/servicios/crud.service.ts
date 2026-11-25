import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
@Injectable({providedIn:'root'})
export class CrudService {
 private http=inject(HttpClient);
 profile(emp:string){return this.http.get<any>('/api/sprint2/colaboradores/'+encodeURIComponent(emp)+'/laboral');}
 list(e:string){return this.http.get<any[]>('/api/'+e+'/');}
 detail(e:string,id:number){return this.http.get<any>('/api/'+e+'/'+id+'/');}
 save(e:string,id:number|null,data:any){return id===null?this.http.post('/api/'+e+'/',data):this.http.patch('/api/'+e+'/'+id+'/',data);}
 remove(e:string,id:number){return this.http.delete('/api/'+e+'/'+id+'/');}
}
