import {Component, OnInit} from '@angular/core';
import {Router} from '@angular/router';
import {UserInfo} from '../../model/UserInfo';
import {MatSnackBar} from "@angular/material";

@Component({
    selector: 'app-home-page',
    templateUrl: './home-page.component.html',
    styleUrls: ['./home-page.component.scss']
})
export class HomePageComponent implements OnInit {
    public user: UserInfo;

    constructor(private routerService: Router, private snackBar: MatSnackBar) {
        this.user = JSON.parse(sessionStorage.getItem('userInfo'));
    }

    ngOnInit() {
    }

    private indicateValidationPageIsUnavailable(): void {
      this.snackBar.open('Validation Page is temporarily unavailable.', '', {duration: 2000, });
  }
}
