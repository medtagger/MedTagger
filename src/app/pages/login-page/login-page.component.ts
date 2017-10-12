import {Component, OnInit} from '@angular/core';
import {Router} from '@angular/router';

@Component({
  selector: 'app-login-page',
  templateUrl: './login-page.component.html'
})
export class LoginPageComponent implements OnInit {

  constructor(private routerService: Router) {
  }

  ngOnInit() {
  }

  public logIn(): void {
    this.routerService.navigate(['marker']);
  }

}
