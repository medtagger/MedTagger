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

    userName = new FormControl('', [Validators.required]);
    userSurname = new FormControl('', [Validators.required]);
    userEmail = new FormControl('', [Validators.required, Validators.email]);
    userPassword = new FormControl('', [Validators.required]);
    userPasswordConfirmation = new FormControl('', [Validators.required]);

    public currentUser: UserInfo;
    private allUsers: Array<UserInfo>;

    constructor(public snackBar: MatSnackBar, private usersService: UsersService) {
        this.currentUser = JSON.parse(sessionStorage.getItem('userInfo'));
        if (this.currentUser.role === 'admin') {
            this.usersService.getAllUsers().then(users => this.allUsers = users);
        }
    }

    ngOnInit() {
        this.userName.setValue(this.currentUser.firstName);
        this.userSurname.setValue(this.currentUser.lastName);
        this.userEmail.setValue(this.currentUser.email);
    }

    private promoteToDoctor(user: UserInfo): void {
        this.usersService.setRole(user.id, 'doctor')
            .then(() => {
                user.role = 'doctor';
            })
    }

    showInvalidFormMessage() {
        this.snackBar.open("Nieprawidłowe dane formularza!", "Zamknij", {
            duration: 5000,
        });
    }

    getUserNameErrorMessage() {
        return this.userName.hasError('required') ? 'Imię jest wymagane!' : '';
    }

    getUserSurnameErrorMessage() {
        return this.userSurname.hasError('required') ? 'Nazwisko jest wymagane!' : '';
    }

    getUserEmailErrorMessage() {
        return this.userEmail.hasError('required') ? 'Adres e-mail jest wymagany!' :
            this.userEmail.hasError('email') ? 'Nieprawidłowy adres e-mail' : '';
    }

    getUserPasswordErrorMessage() {
        return this.userPassword.hasError('required') ? 'Hasło jest wymagane!' : '';
    }

    getUserPasswordConfirmationErrorMessage() {
        return this.userPasswordConfirmation.hasError('required') ? 'Potwierdzenie hasła jest wymagane!' : '';
    }
}
