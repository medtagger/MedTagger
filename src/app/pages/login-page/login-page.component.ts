import {Component, OnInit} from '@angular/core';
import {Router} from '@angular/router';
import {MockService} from '../../services/mock.service';

@Component({
  selector: 'app-login-page',
  templateUrl: './login-page.component.html',
  // styleUrls: ['./login-page.component.scss']
})
export class LoginPageComponent implements OnInit {

  constructor(private routerService: Router, private mockService: MockService) {
    this.mockService.getMockSlices().then((res) => {
      console.log('LoginPageComponent | mockResult: ', res);
    });
  }

  ngOnInit() {
  }

  public logIn(): void {
    this.routerService.navigate(['marker']);
  }

}
