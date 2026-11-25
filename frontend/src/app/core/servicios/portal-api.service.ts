import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
@Injectable({providedIn:'root'})
export class PortalApiService {
 private http=inject(HttpClient);
 download(url:string,params:Record<string,string>){return this.http.get(url,{params,responseType:'blob'});}
 get<T>(url:string, options?:any){return this.http.get<T>(url,options as {params?:Record<string,string>});}
 post<T=any>(url:string,data:any){return this.http.post<T>(url,data);}
 put<T=any>(url:string,data:any){return this.http.put<T>(url,data);}
 delete<T=any>(url:string){return this.http.delete<T>(url);}
}