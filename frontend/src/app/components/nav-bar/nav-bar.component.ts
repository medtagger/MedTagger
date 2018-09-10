import {Component, OnInit} from '@angular/core';
import {ActivatedRoute} from "@angular/router";
import {HOME} from '../../constants/routes';

@Component({
    selector: 'app-nav-bar',
    inputs: ['showPageTitle'],
    templateUrl: './nav-bar.component.html',
    styleUrls: ['./nav-bar.component.scss']
})
export class NavBarComponent implements OnInit {

    showPageTitle: boolean;
    activeRoute: string;
    homeRoute = HOME;
    constructor(private activatedRoute: ActivatedRoute) {
        this.activeRoute = activatedRoute.snapshot.data['title'];
    }

    ngOnInit() {
    }

}
