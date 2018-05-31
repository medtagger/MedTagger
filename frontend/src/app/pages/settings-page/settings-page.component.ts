import {Component, OnInit} from '@angular/core';
import {MatSnackBar} from '@angular/material';
import {FormControl, Validators} from '@angular/forms';
import {UserInfo} from '../../model/UserInfo';
import {UsersService} from '../../services/users.service';


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
    protected allUsers: Array<UserInfo>;

    constructor(public snackBar: MatSnackBar, private usersService: UsersService) {
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
          this.snackBar.open('User data has not been updated due to a validation failure.', 'Dismiss', {
            duration: 3000,
          });
          return;
        }
        this.usersService.setUserDetails(this.currentUser.id, this.userFirstName.value, this.userLastName.value)
            .then(() => {
              this.currentUser.firstName = this.userFirstName.value;
              this.currentUser.lastName = this.userLastName.value;
              sessionStorage.setItem('userInfo', JSON.stringify(this.currentUser));
              this.snackBar.open('User data has been updated.', 'Dismiss', {
                duration: 3000,
              });
            });
    }

    validateUserInput() {
      return !(this.userFirstName.value === '' ||
          this.userLastName.value === '' ||
          this.userEmail.value === '' ||
          (this.userFirstName.value === this.currentUser.firstName && this.userLastName.value === this.currentUser.lastName));
    }

    showInvalidFormMessage() {
        this.snackBar.open('Incorrect form data!', 'Dismiss', {
            duration: 5000,
        });
    }

    getUserFirstNameErrorMessage() {
        return this.userFirstName.hasError('required') ? 'First name is required!' : '';
    }

    getUserLastNameErrorMessage() {
        return this.userLastName.hasError('required') ? 'Last name is required!' : '';
    }

    getUserEmailErrorMessage() {
        return this.userEmail.hasError('required') ? 'E-mail address is required!' :
            this.userEmail.hasError('email') ? 'Incorrect e-mail address' : '';
    }

    getUserPasswordErrorMessage() {
        return this.userPassword.hasError('required') ? 'Password is required!' : '';
    }

    getUserPasswordConfirmationErrorMessage() {
        return this.userPasswordConfirmation.hasError('required') ? 'Password confirmation is required!' : '';
    }

}
