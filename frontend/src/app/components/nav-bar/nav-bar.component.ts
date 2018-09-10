import {Component, OnInit} from '@angular/core';

@Component({
    selector: 'app-nav-bar',
    inputs: ['activePage'],
    templateUrl: './nav-bar.component.html',
    styleUrls: ['./nav-bar.component.scss']
})
export class NavBarComponent implements OnInit {

    activePage: string;
    constructor() {
    }

    ngOnInit() {
    }

}
