import {
    HttpInterceptor,
    HttpRequest,
    HttpHandler,
    HttpSentEvent,
    HttpHeaderResponse,
    HttpProgressEvent,
    HttpResponse,
    HttpUserEvent
} from '@angular/common/http';
import {Observable} from 'rxjs';
import {Injectable} from '@angular/core';

@Injectable()
export class HttpAuthenticationInterceptor implements HttpInterceptor {
    intercept(req: HttpRequest<any>, next: HttpHandler):
        Observable<HttpSentEvent | HttpHeaderResponse | HttpProgressEvent | HttpResponse<any> | HttpUserEvent<any>> {
        req = req.clone({
            setHeaders: {
                Authorization: 'Bearer ' + sessionStorage.getItem('authorizationToken')
            }
        });

        return next.handle(req);
    }

}
