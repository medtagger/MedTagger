import {Component, OnInit} from '@angular/core';
import {Router} from '@angular/router';
import {FormControl, FormGroup, Validators} from '@angular/forms';
import {passwordValidator} from '../validators/password-validator.directive';

enum LoginPageMode {
  LOG_IN,
  REGISTER
}

@Component({
  selector: 'app-login-page',
  templateUrl: './login-page.component.html',
  styleUrls: ['./login-page.component.scss'],
})
export class LoginPageComponent implements OnInit {
  LoginPageMode = LoginPageMode;  // Needed in template for comparison with Enum values
  loginPageMode: LoginPageMode = LoginPageMode.LOG_IN;
  firstName = '';
  lastName = '';
  email = '';
  password = '';
  confirmPassword = '';
  userForm: FormGroup;


  constructor(private routerService: Router) {
  }

  ngOnInit() {
    this.userForm = new FormGroup({
      'firstName': new FormControl(this.firstName, [
        Validators.required]),
      'lastName': new FormControl(this.lastName, [
        Validators.required]),
      'email': new FormControl(this.email, [
        Validators.required, Validators.email]),
      'password': new FormControl(this.password, [
        Validators.required]),
      'confirmPassword': new FormControl(this.confirmPassword, [
        Validators.required, passwordValidator()])
    });
  }

  public logIn(): void {
    this.routerService.navigate(['home']);
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

  public userRegistration(): void {
    // TODO: registration
  }
}
