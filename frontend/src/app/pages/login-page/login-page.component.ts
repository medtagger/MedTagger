import {Component, OnInit} from '@angular/core';
import {Router} from '@angular/router';
import {FormControl, FormGroup, Validators} from '@angular/forms';
import {passwordValidator} from '../validators/password-validator.directive';
import {AccountService} from '../../services/account.service';

enum LoginPageMode {
    LOG_IN,
    REGISTER
}

const MIN_PASSWORD_LENGTH = 8;

@Component({
    selector: 'app-login-page',
    templateUrl: './login-page.component.html',
    styleUrls: ['./login-page.component.scss'],
    providers: [AccountService]
})

export class LoginPageComponent implements OnInit {
    LoginPageMode = LoginPageMode;  // Needed in template for comparison with Enum values
    loginPageMode: LoginPageMode = LoginPageMode.REGISTER;
    userForm: FormGroup;

    loggingInProgress: boolean;
    loggingInError: boolean;
    registrationInProgress: boolean;
    loginPasswordVisible = false;
    registerPasswordVisible = false;

    constructor(private routerService: Router, private accountService: AccountService) {
    }

    ngOnInit() {
        if (this.accountService.isLoggedIn()) {
            this.routerService.navigate(['home']);
        }
        this.userForm = new FormGroup({
            firstName: new FormControl(null, [Validators.required]),
            lastName: new FormControl(null, [Validators.required]),
            email: new FormControl(null, [Validators.required, Validators.email]),
            password: new FormControl(null, [Validators.required, Validators.minLength(MIN_PASSWORD_LENGTH)]),
            confirmPassword: new FormControl(null, [Validators.required, passwordValidator()])
        });
    }

    resetLogin(): void {
        this.loggingInProgress = false;
        this.loggingInError = false;
    }

    public logIn(): void {
        this.loggingInProgress = true;
        this.loggingInError = false;
        this.accountService.logIn(this.userForm.value['email'], this.userForm.value['password'])
            .then((token) => {
                sessionStorage.setItem('authorizationToken', token);
                return this.accountService.getCurrentUserInfo();
            }, (error) => {
                this.loggingInProgress = false;
                this.loggingInError = true;
            })
            .then((userInfo) => {
                this.loggingInProgress = false;
                if (userInfo) {
                    sessionStorage.setItem('userInfo', JSON.stringify(userInfo));
                    this.routerService.navigate(['home']);
                } else {
                    this.loggingInError = true;
                }
            }, () => {
                this.loggingInProgress = false;
                this.loggingInError = true;
            });
    }

    public changePageMode(): void {
        this.userForm.reset();
        this.loginPasswordVisible = false;
        this.registerPasswordVisible = false;
        if (this.loginPageMode === LoginPageMode.LOG_IN) {
            this.loginPageMode = LoginPageMode.REGISTER;
            this.resetLogin();
        } else if (this.loginPageMode === LoginPageMode.REGISTER) {
            this.loginPageMode = LoginPageMode.LOG_IN;
            this.resetRegistration();
        } else {
            console.error('Unsupported login page mode!');
        }
    }

    public changeVisibility(): void {
        if (this.loginPageMode === LoginPageMode.LOG_IN) {
            this.loginPasswordVisible = !this.loginPasswordVisible;
        } else if (this.loginPageMode === LoginPageMode.REGISTER) {
            this.registerPasswordVisible = !this.registerPasswordVisible;
        } else {
            console.error('Unsupported login page mode!');
        }
    }

    getFirstNameErrorMessage(): string {
        return this.userForm.get('firstName').hasError('required') ? 'Field required' : '';
    }

    getLastNameErrorMessage(): string {
        return this.userForm.get('lastName').hasError('required') ? 'Field required' : '';
    }

    getEmailErrorMessage(): string {
        return this.userForm.get('email').hasError('required') ? 'Field required' :
            this.userForm.get('email').hasError('email') ? 'Invalid email.' :
                '';
    }

    getPasswordErrorMessage(): string {
        return this.userForm.get('password').hasError('required') ? 'Field required' :
            this.userForm.get('password').hasError('minlength') ? 'Password should be longer than ' + MIN_PASSWORD_LENGTH + ' characters.' :
                '';
    }

    getConfirmPasswordErrorMessage(): string {
        return this.userForm.get('confirmPassword').hasError('required') ? 'Field required' :
            this.userForm.get('confirmPassword').hasError('passwordValidator') ? 'Passwords does not match.' :
                '';
    }

    resetRegistration(): void {
        this.registrationInProgress = false;
    }

    public register(): void {
        this.registrationInProgress = true;
        const formValue = this.userForm.value;
        this.accountService.register(formValue['email'], formValue['password'], formValue['firstName'], formValue['lastName'])
            .then(() => {
                this.registrationInProgress = false;
                this.changePageMode();
            }, () => {
                this.resetRegistration();
            });
    }
}
