import { HttpInterceptorFn } from '@angular/common/http';

export const authInterceptor: HttpInterceptorFn = (req, next) => {
    const token = localStorage.getItem('token');
    console.log('AuthInterceptor - Intercepting:', req.url);
    console.log('AuthInterceptor - Token found:', !!token);

    if (token) {
        const clonedReq = req.clone({
            setHeaders: {
                Authorization: `Token ${token}`
            }
        });
        return next(clonedReq);
    }

    return next(req);
};
