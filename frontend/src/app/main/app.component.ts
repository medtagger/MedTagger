import {Component, OnInit} from '@angular/core';
import {Router, NavigationEnd, ActivatedRoute} from '@angular/router';
import {UserInfo} from '../model/UserInfo';
import {filter, map, mergeMap} from "rxjs/operators";

@Component({
    selector: 'app-root',
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {

    pageTitle = '';
    public currentUser: UserInfo;

    constructor(private router: Router, private activatedRoute: ActivatedRoute) {
        router.events.subscribe(() => {
            this.currentUser = JSON.parse(sessionStorage.getItem('userInfo'));
            console.log(this.currentUser);
        })

    };

    ngOnInit() {
        this.router.events.pipe(
            filter((event) => event instanceof NavigationEnd),
            map(() => this.activatedRoute),
            map((route) => {
                while (route.firstChild) route = route.firstChild;
                return route;
            }),
            filter((route) => route.outlet === 'primary'),
            mergeMap((route) => route.data),
            mergeMap((route) => route.data),
        ).subscribe((event) => this.pageTitle = event['title']);
    }

    get isLoginPage(): boolean {
        return this.router.url.startsWith('/login');
    }

    public logOut(): void {
        sessionStorage.removeItem('authorizationToken');
        sessionStorage.removeItem('userInfo');
        this.router.navigate(['login']);
    }
}
