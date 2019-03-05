import {Component, OnInit} from '@angular/core';
import {Router} from '@angular/router';
import {FormControl, FormGroup, Validators} from '@angular/forms';
import {passwordValidator} from '../validators/password-validator.directive';
import {AccountService} from '../../services/account.service';
import * as appRoutes from '../../constants/routes';
import {UserInfo} from '../../model/UserInfo';

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
    loginPageMode: LoginPageMode = LoginPageMode.LOG_IN;
    registerForm: FormGroup;
    loginForm: FormGroup;

    user: UserInfo;

    loggingInProgress: boolean;
    loggingInError: string;
    registrationInProgress: boolean;
    registrationError: string;
    loginPasswordVisible = false;
    registerPasswordVisible = false;

    constructor(private routerService: Router, private accountService: AccountService) {
    }

    ngOnInit() {
        if (this.accountService.isLoggedIn()) {
            this.routerService.navigate([appRoutes.HOME]);
        }
        this.registerForm = new FormGroup({
            firstName: new FormControl(null, [Validators.required]),
            lastName: new FormControl(null, [Validators.required]),
            email: new FormControl(null, [Validators.required, Validators.email]),
            password: new FormControl(null, [Validators.required, Validators.minLength(MIN_PASSWORD_LENGTH)]),
            confirmPassword: new FormControl(null, [Validators.required, passwordValidator()])
        });
        this.loginForm = new FormGroup({
            email: new FormControl(null, [Validators.required, Validators.email]),
            password: new FormControl(null, [Validators.required, Validators.minLength(MIN_PASSWORD_LENGTH)])
        });
    }

    resetLogin(): void {
        this.loginForm.reset();
        this.loggingInProgress = false;
        this.loggingInError = undefined;
    }

    public logIn(): void {
        if (this.loginForm.invalid) {
            return;
        }

        this.loggingInProgress = true;
        this.loggingInError = undefined;
        this.accountService.logIn(this.loginForm.value['email'], this.loginForm.value['password'])
            .then((token) => {
                sessionStorage.setItem('authorizationToken', token);
                return this.accountService.getCurrentUserInfo();
            }, (error) => {
                this.loggingInProgress = false;
                this.loggingInError = error.error.details;
            })
            .then((userInfo) => {
                this.loggingInProgress = false;
                console.log(userInfo);
                if (userInfo) {
                    sessionStorage.setItem('userInfo', JSON.stringify(userInfo));
                    this.user = JSON.parse(sessionStorage.getItem('userInfo'));
                    this.routerService.navigate([this.user.settings.skipTutorial ? appRoutes.HOME : appRoutes.TUTORIAL]);
                }
            }, (error) => {
                this.loggingInProgress = false;
                this.loggingInError = error.error.details;
            });
    }

    public changePageMode(loginPageMode: LoginPageMode): void {
        if (loginPageMode === this.loginPageMode) {
            return;
        }

        this.loginPasswordVisible = false;
        this.registerPasswordVisible = false;
        if (loginPageMode === LoginPageMode.LOG_IN) {
            this.resetLogin();
        } else if (loginPageMode === LoginPageMode.REGISTER) {
            this.resetRegistration();
        } else {
            console.error('Unsupported login page mode!');
            return;
        }
        this.loginPageMode = loginPageMode;
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
        return this.registerForm.get('firstName').hasError('required') ? 'Field required' : '';
    }

    getLastNameErrorMessage(): string {
        return this.registerForm.get('lastName').hasError('required') ? 'Field required' : '';
    }

    getEmailErrorMessage(): string {
        return this.registerForm.get('email').hasError('required') ? 'Field required' :
            this.registerForm.get('email').hasError('email') ? 'Invalid email.' :
                '';
    }

    getPasswordErrorMessage(): string {
        return this.registerForm.get('password').hasError('required') ? 'Field required' :
            this.registerForm.get('password').hasError('minlength') ? 'Password should be longer than ' + MIN_PASSWORD_LENGTH
                + ' characters.' : '';
    }

    getConfirmPasswordErrorMessage(): string {
        return this.registerForm.get('confirmPassword').hasError('required') ? 'Field required' :
            this.registerForm.get('confirmPassword').hasError('passwordValidator') ? 'Passwords do not match.' :
                '';
    }

    resetRegistration(): void {
        this.registerForm.reset();
        this.registrationInProgress = false;
        this.registrationError = undefined;
    }

    public register(): void {
        if (this.registerForm.invalid) {
            return;
        }
        this.registrationInProgress = true;
        this.registrationError = undefined;
        const formValue = this.registerForm.value;
        this.accountService.register(formValue['email'], formValue['password'], formValue['firstName'], formValue['lastName'])
            .then((userToken: string) => {
                sessionStorage.setItem('authorizationToken', userToken);
                return this.accountService.getCurrentUserInfo();
            }, (error) => {
                this.resetRegistration();
                this.registrationError = error.error.details;
            })
            .then((userInfo) => {
                this.registrationInProgress = false;
                console.log(userInfo);
                if (userInfo) {
                    sessionStorage.setItem('userInfo', JSON.stringify(userInfo));
                    this.user = JSON.parse(sessionStorage.getItem('userInfo'));
                    this.routerService.navigate([this.user.settings.skipTutorial ? appRoutes.HOME : appRoutes.TUTORIAL]);
                }
            }, (error) => {
                this.resetRegistration();
                this.registrationError = error.error.details;
            });
    }
}
