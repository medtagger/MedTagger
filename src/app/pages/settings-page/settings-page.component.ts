import { Component, OnInit } from '@angular/core';
import { MatSnackBar } from '@angular/material';
import { FormControl, Validators } from '@angular/forms';


@Component({
  selector: 'app-settings-page',
  templateUrl: './settings-page.component.html',
  styleUrls: ['./settings-page.component.scss']
})
export class SettingsPageComponent implements OnInit {

  userName = new FormControl('', [Validators.required]);
  userSurname = new FormControl('', [Validators.required]);
  userEmail = new FormControl('', [Validators.required, Validators.email]);
  userPassword = new FormControl('', [Validators.required]);
  userPasswordConfirmation = new FormControl('', [Validators.required]);

  constructor(public snackBar: MatSnackBar) {
  }

  ngOnInit() {
    this.userName.setValue('Jan');
    this.userSurname.setValue('Kowalski');
    this.userEmail.setValue('jan.kowalski@gmail.com');
  }

  //
  // Functions related to data saving
  //

  saveBasicData() {
    if (!this.userName.valid || !this.userSurname.valid || !this.userEmail.valid) {
      this.showInvalidFormMessage();
      return;
    }
    this.snackBar.open("Zapisano!", "Zamknij", {
        duration: 5000,
      });
  }

  savePasswords() {
    if (!this.userPassword.valid || !this.userPasswordConfirmation.valid) {
      this.showInvalidFormMessage();
      return;
    }
    this.snackBar.open("Zapisano!", "Zamknij", {
      duration: 5000,
    });
  }

  //
  // Functions related to error handling
  //
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
