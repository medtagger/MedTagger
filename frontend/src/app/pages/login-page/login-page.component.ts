import {Component, OnInit} from '@angular/core';
import {Router} from '@angular/router';
import {FormControl, FormGroup, Validators} from '@angular/forms';
import {passwordValidator} from '../validators/password-validator.directive';
import {AccountService} from '../../services/account.service';
import * as ERRORS from "./login-errors";

enum LoginPageMode {
    LOG_IN,
    REGISTER
}

const MIN_PASSWORD_LENGTH: number = 8;

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

    loggingInProgress: boolean;
    loggingInError: boolean;

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
            }, (error) => {
                this.loggingInProgress = false;
                this.loggingInError = true;
            });
    }

    public changePageMode(): void {
        this.userForm.reset();
        if (this.loginPageMode === LoginPageMode.LOG_IN) {
            this.loginPageMode = LoginPageMode.REGISTER;
        } else if (this.loginPageMode === LoginPageMode.REGISTER) {
            this.loginPageMode = LoginPageMode.LOG_IN;
        } else {
            console.error('Unsupported login page mode!');
        }
    }

    getFirstNameErrorMessage(): string {
        return this.userForm.get('firstName').hasError('required') ? ERRORS.REQUIREMENT : '';
    }

    getLastNameErrorMessage(): string {
        return this.userForm.get('lastName').hasError('required') ? ERRORS.REQUIREMENT : '';
    }

    getEmailErrorMessage(): string {
        return this.userForm.get('email').hasError('required') ? ERRORS.REQUIREMENT :
            this.userForm.get('email').hasError('email') ? ERRORS.INVALID_MAIL :
                '';
    }

    getPasswordErrorMessage(): string {
        return this.userForm.get('password').hasError('required') ? ERRORS.REQUIREMENT :
            this.userForm.get('password').hasError('minlength') ? ERRORS.PASSWORD_LENGTH :
                '';
    }

    getConfirmPasswordErrorMessage(): string {
        return this.userForm.get('confirmPassword').hasError('required') ? ERRORS.REQUIREMENT :
            this.userForm.get('confirmPassword').hasError('passwordValidator') ? ERRORS.PASSWORD_MATCH :
                '';
    }

    public register(): void {
        let formValue = this.userForm.value;
        this.accountService.register(formValue['email'], formValue['password'], formValue['firstName'], formValue['lastName'])
            .then(() => this.changePageMode());
    }
}
