import {AfterViewChecked, Component, ElementRef, Inject, OnInit, ViewChild} from '@angular/core';
import {MAT_DIALOG_DATA, MatDialogRef} from '@angular/material';
import {FormBuilder, FormControl, FormGroup} from '@angular/forms';

@Component({
    selector: 'app-input-dialog',
    templateUrl: 'input-dialog.component.html',
    styleUrls: ['./all.dialog.scss']
})
export class InputDialogComponent {

    userInput = new FormControl('', []);

    constructor(private dialogRef: MatDialogRef<InputDialogComponent>,
                @Inject(MAT_DIALOG_DATA) public data: { title: string, content: string, buttonText: string }) {
    }

    closeDialog(): void {
        let input = this.userInput.value ? this.userInput.value.trim() : '';
        this.dialogRef.close(`${input}`);
    }
}
