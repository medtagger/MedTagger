import {Component, OnInit} from '@angular/core';
import {UserInfo} from '../../model/UserInfo';
import {Router} from '@angular/router';
import {UPLOAD, SETTINGS, LOGIN} from '../../constants/routes';
import {
    trigger,
    style,
    animate,
    transition
} from '@angular/animations';

@Component({
    selector: 'app-home-page',
    templateUrl: './home-page.component.html',
    styleUrls: ['./home-page.component.scss'],
    animations: [
        trigger('displayDropdown', [
            transition('void => *', [
                style({transform: 'translateY(-10%)', opacity: 1}),
                animate(200)
            ]),
            transition('* => void', [
                animate(200, style({transform: 'translateY(10%)'}))
            ])
        ])
    ]
})
export class HomePageComponent implements OnInit {
    public user: UserInfo;
    public isDropdownActive = false;
    public settingsPage: string = '/' + SETTINGS;
    public loginPage: string = '/' + LOGIN;

    constructor(private router: Router) {
        this.user = JSON.parse(sessionStorage.getItem('userInfo'));
    }

    ngOnInit() {
    }

    goToUploadPage(): void {
        this.router.navigateByUrl('/' + UPLOAD);
    }

    toggleDropdown(): void {
        this.isDropdownActive = !this.isDropdownActive;
        // TODO: find how to close dropdown when button above loses focus
        setTimeout(() => this.isDropdownActive = false, 2000);
    }

    public logOut(): void {
        sessionStorage.removeItem('authorizationToken');
        sessionStorage.removeItem('userInfo');
        this.router.navigate([LOGIN]);
    }

}
