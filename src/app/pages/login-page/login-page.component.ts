import {Component, OnInit} from '@angular/core';
import {Router} from '@angular/router';
import {FormControl, FormGroup, Validators} from '@angular/forms';
import {passwordValidator} from '../validators/password-validator.directive';
import { AccountService } from '../../services/account.service';

enum LoginPageMode {
  LOG_IN,
  REGISTER
}

@Component({
  selector: 'app-login-page',
  templateUrl: './login-page.component.html',
  styleUrls: ['./login-page.component.scss'],
  providers: [AccountService]
})

export class LoginPageComponent implements OnInit {
  LoginPageMode = LoginPageMode;  // Needed in template for comparison with Enum values
  loginPageMode: LoginPageMode = LoginPageMode.LOG_IN;
  userForm: FormGroup;

  constructor(private routerService: Router, private accountService: AccountService) {
  }

  ngOnInit() {
    this.userForm = new FormGroup({
      firstName: new FormControl(null, [Validators.required]),
      lastName: new FormControl(null, [Validators.required]),
      email: new FormControl(null, [Validators.required, Validators.email]),
      password: new FormControl(null, [Validators.required]),
      confirmPassword: new FormControl(null, [Validators.required, passwordValidator()])
    });
  }

  public logIn(): void {
    this.accountService.logIn(this.userForm.value['email'], this.userForm.value['password'])
      .then(token => {
        sessionStorage.setItem('authenticationToken', token);
        return this.accountService.getCurrentUserInfo();
      })
      .then(userInfo => {
        sessionStorage.setItem('userInfo', JSON.stringify(userInfo));
        this.routerService.navigate(['home']);
      });
  }

  public changePageMode(): void {
    if (this.loginPageMode === LoginPageMode.LOG_IN) {
      this.loginPageMode = LoginPageMode.REGISTER;
    } else if (this.loginPageMode === LoginPageMode.REGISTER) {
      this.userForm.reset();
      this.loginPageMode = LoginPageMode.LOG_IN;
    } else {
      console.error('Unsupported login page mode!');
    }
  }

  getFirstNameErrorMessage() {
    if (this.userForm.get('firstName').hasError('required')) {
      return 'Pole obowiązkowe.';
    }
  }

  getLastNameErrorMessage() {
    if (this.userForm.get('lastName').hasError('required')) {
      return 'Pole obowiązkowe.';
    }
  }

  getEmailErrorMessage() {
    return this.userForm.get('email').hasError('required') ? 'Pole obowiązkowe.' :
      this.userForm.get('email').hasError('email') ? 'E-mail jest niepoprawny.' :
        '';
  }

  getPasswordErrorMessage() {
    if (this.userForm.get('password').hasError('required')) {
      return 'Pole obowiązkowe.';
    }
  }

  getConfirmPasswordErrorMessage() {
    return this.userForm.get('confirmPassword').hasError('required') ? 'Pole obowiązkowe.' :
      this.userForm.get('confirmPassword').hasError('passwordValidator') ? 'Podane hasła nie są zgodne.' :
        '';
  }

  public register(): void {
    let formValue = this.userForm.value;
    this.accountService.register(formValue['email'], formValue['password'], formValue['firstName'], formValue['lastName'])
      .then(() => this.changePageMode());
  }
}
