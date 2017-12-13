import 'rxjs/add/operator/filter';
import 'rxjs/add/operator/map';
import 'rxjs/add/operator/mergeMap';

import { Component, OnInit } from '@angular/core';
import { Router, NavigationEnd, ActivatedRoute } from '@angular/router';
import { UserInfo } from '../model/UserInfo';

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
    })

  };

  ngOnInit() {
    this.router.events
      .filter((event) => event instanceof NavigationEnd)
      .map(() => this.activatedRoute)
      .map((route) => {
        while (route.firstChild) route = route.firstChild;
        return route;
      })
      .filter((route) => route.outlet === 'primary')
      .mergeMap((route) => route.data)
      .subscribe((event) => this.pageTitle = event['title']);
  }

  get isLoginPage() : boolean {
    return this.router.url === '/login';
  }

  public logOut(): void {
    sessionStorage.removeItem('authenticationToken');
    sessionStorage.removeItem('userInfo');
    this.router.navigate(['login']);
  }
}
