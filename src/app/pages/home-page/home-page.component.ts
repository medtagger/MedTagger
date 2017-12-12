import {Component, OnInit} from '@angular/core';
import {Router} from '@angular/router';
import { UserInfo } from '../../model/UserInfo';

@Component({
  selector: 'app-home-page',
  templateUrl: './home-page.component.html',
  styleUrls: ['./home-page.component.scss']
})
export class HomePageComponent implements OnInit {
  private user: UserInfo;

  constructor(private routerService: Router) {
    this.user = JSON.parse(sessionStorage.getItem('userInfo'));
  }

  ngOnInit() {
    if (!sessionStorage.getItem('authenticationToken')) {
      this.routerService.navigate(['login']);
    }
  }
}
