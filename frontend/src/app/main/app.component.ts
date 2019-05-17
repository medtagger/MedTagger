import {Component, OnInit} from '@angular/core';
import {Router, NavigationEnd, ActivatedRoute} from '@angular/router';
import {UserInfo} from '../model/UserInfo';
import {MatSnackBar} from '@angular/material';
import {filter, map, mergeMap} from 'rxjs/operators';
import * as appRoutes from '../constants/routes';
import { TranslateService } from '@ngx-translate/core';

@Component({
    selector: 'app-root',
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {
    private static readonly DEFAULT_LANGUAGE: string = 'en';
    public pageTitle = '';
    public shouldShowFooter = true;
    public currentUser: UserInfo;

    constructor(private router: Router, private activatedRoute: ActivatedRoute,
        private snackBar: MatSnackBar, private translate: TranslateService) {

        translate.setDefaultLang(AppComponent.DEFAULT_LANGUAGE);

        translate.use(AppComponent.DEFAULT_LANGUAGE);

        router.events.subscribe(() => {
            this.currentUser = JSON.parse(sessionStorage.getItem('userInfo'));
            console.log(this.currentUser);
        });
    }

    ngOnInit() {
        this.router.events.pipe(
            filter((event) => event instanceof NavigationEnd),
            map(() => this.activatedRoute),
            map((route: ActivatedRoute) => {
                while (route.firstChild) {
                    route = route.firstChild;
                }
                return route;
            }),
            filter((route: ActivatedRoute) => route.outlet === 'primary'),
            mergeMap((route: ActivatedRoute) => route.data)
        ).subscribe((event) => {
            this.pageTitle = event['title'];
            this.shouldShowFooter = !event['disableFooter'];
        });
    }

    get isLoginPage(): boolean {
        return this.router.url.startsWith('/' + appRoutes.LOGIN);
    }

    public logOut(): void {
        sessionStorage.removeItem('authorizationToken');
        sessionStorage.removeItem('userInfo');
        this.router.navigate([appRoutes.LOGIN]);
    }

    private indicateValidationPageIsUnavailable(): void {
      this.snackBar.open('Validation Page is temporarily unavailable.', '', {duration: 2000, });
  }
}
