import { HttpInterceptorFn } from '@angular/common/http';
export const API_ANDROID = 'http://10.0.2.2:8000';
export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const native = (window as any).Capacitor?.isNativePlatform?.();
  if(native && req.url.startsWith('/api/')) req=req.clone({url:API_ANDROID+req.url});
  const token = sessionStorage.getItem('nettplus_token');
  return next(token ? req.clone({setHeaders:{Authorization:`Bearer ${token}`}}) : req);
};