import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { HOME } from '../../constants/routes';

@Component({
    selector: 'app-nav-bar',
    templateUrl: './nav-bar.component.html',
    styleUrls: ['./nav-bar.component.scss']
})
export class NavBarComponent implements OnInit {

    showPageTitle: boolean;
    activeRoute: string;
    homeRoute = HOME;

    constructor(private activatedRoute: ActivatedRoute, private router: Router) {
        this.activeRoute = activatedRoute.snapshot.data['title'];
        this.showPageTitle = !router.isActive(HOME, false);
    }

    ngOnInit() {}
}
