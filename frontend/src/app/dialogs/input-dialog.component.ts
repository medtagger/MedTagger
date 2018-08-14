import {Component, Inject} from '@angular/core';
import {MAT_DIALOG_DATA, MatDialogRef} from '@angular/material';
import {FormControl} from '@angular/forms';

@Component({
    selector: 'app-input-dialog',
    templateUrl: 'input-dialog.component.html',
    styleUrls: ['./all.dialog.scss']
})
export class InputDialogComponent {

    userInput = new FormControl('', []);

    constructor(private dialogRef: MatDialogRef<InputDialogComponent>,
                @Inject(MAT_DIALOG_DATA) public data: { title: string, content: string, input: string, buttonText: string }) {
    }

    closeDialog(): void {
        const input = this.userInput.value ? this.userInput.value.trim() : '';
        this.dialogRef.close(`${input}`);
    }
}
