import { Component, OnInit } from '@angular/core';
import { MatSnackBar } from '@angular/material';
import { FormControl, Validators } from '@angular/forms';
import { UserInfo } from '../../model/UserInfo';
import { UsersService } from '../../services/users.service';
import { TranslateService } from '@ngx-translate/core';


@Component({
    selector: 'app-settings-page',
    templateUrl: './settings-page.component.html',
    styleUrls: ['./settings-page.component.scss'],
    providers: [UsersService]
})
export class SettingsPageComponent implements OnInit {

    userFirstName = new FormControl('', [Validators.required]);
    userLastName = new FormControl('', [Validators.required]);
    userEmail = new FormControl('', [Validators.required, Validators.email]);
    userPassword = new FormControl('', [Validators.required]);
    userPasswordConfirmation = new FormControl('', [Validators.required]);

    public currentUser: UserInfo;
    public allUsers: Array<UserInfo>;

    constructor(public snackBar: MatSnackBar, private usersService: UsersService,
        private translateService: TranslateService) {
        this.currentUser = JSON.parse(sessionStorage.getItem('userInfo'));
        if (this.currentUser.role === 'admin') {
            this.usersService.getAllUsers().then(users => this.allUsers = users);
        }
    }

    ngOnInit() {
        this.userFirstName.setValue(this.currentUser.firstName);
        this.userLastName.setValue(this.currentUser.lastName);
        this.userEmail.setValue(this.currentUser.email);
    }

    private promoteToDoctor(user: UserInfo): void {
        this.usersService.setRole(user.id, 'doctor')
            .then(() => {
                user.role = 'doctor';
            });
    }

    updateUserDetails() {
        if (!this.validateUserInput()) {
            this.snackBar.open(
                this.translateService.instant('SETTINGS.INFO.USER_VALIDATION_FAILED'),
                this.translateService.instant('SETTINGS.INFO.DISMISS'),
                { duration: 3000 }
            );
            return;
        }
        this.usersService.setUserDetails(this.currentUser.id, this.userFirstName.value, this.userLastName.value)
            .then(() => {
                this.currentUser.firstName = this.userFirstName.value;
                this.currentUser.lastName = this.userLastName.value;
                sessionStorage.setItem('userInfo', JSON.stringify(this.currentUser));
                this.snackBar.open(
                    this.translateService.instant('SETTINGS.INFO.USER_DATA_UPDATED'),
                    this.translateService.instant('SETTINGS.INFO.DISMISS'),
                    { duration: 3000 }
                );
            });
    }

    validateUserInput() {
      return !(this.userFirstName.value === '' ||
          this.userLastName.value === '' ||
          this.userEmail.value === '' ||
          (this.userFirstName.value === this.currentUser.firstName && this.userLastName.value === this.currentUser.lastName));
    }

    showInvalidFormMessage() {
        this.snackBar.open(
            this.translateService.instant('SETTINGS.INFO.INCORRECT_DATA'),
            this.translateService.instant('SETTINGS.INFO.DISMISS'),
            { duration: 5000 }
        );
    }

    getUserFirstNameErrorMessage() {
        return this.userFirstName.hasError('required')
            ? this.translateService.instant('SETTINGS.VALIDATION.FIRST_NAME') : '';
    }

    getUserLastNameErrorMessage() {
        return this.userLastName.hasError('required')
            ? this.translateService.instant('SETTINGS.VALIDATION.LAST_NAME') : '';
    }

    getUserEmailErrorMessage() {
        return this.userEmail.hasError('required')
            ? this.translateService.instant('SETTINGS.VALIDATION.EMAIL_REQUIRED') :
            this.userEmail.hasError('email')
                ? this.translateService.instant('SETTINGS.VALIDATION.INCORRECt_EMAIL') : '';
    }

    getUserPasswordErrorMessage() {
        return this.userPassword.hasError('required')
            ? this.translateService.instant('SETTINGS.VALIDATION.PASSWORD') : '';
    }

    getUserPasswordConfirmationErrorMessage() {
        return this.userPasswordConfirmation.hasError('required')
            ? this.translateService.instant('SETTINGS.VALIDATION.PASSWORD_CONFIRM') : '';
    }

}
