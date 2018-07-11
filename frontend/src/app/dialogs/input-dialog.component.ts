import { AfterViewChecked, Component, Inject } from "@angular/core";
import {MAT_DIALOG_DATA, MatDialogRef} from "@angular/material";
import {FormBuilder, FormGroup} from "@angular/forms";

@Component({
    selector: 'app-input-dialog',
    templateUrl: 'input-dialog.component.html',
    styleUrls: ['./all.dialog.scss']
})
export class InputDialogComponent implements AfterViewChecked {

    form: FormGroup;

    constructor(private formBuilder: FormBuilder,
                private dialogRef: MatDialogRef<InputDialogComponent>,
                @Inject(MAT_DIALOG_DATA) public data: { title: string, content: string, buttonText: string }) {
    }

    ngOnInit() {
        this.form = this.formBuilder.group({
            userInput: ''
        });
    }

    ngAfterViewChecked() {
        setTimeout(() => {
            document.getElementById('userInput').focus();
        }, 500);
    }

    closeDialog(form): void {
        let input = form.value.userInput ? form.value.userInput : '';
        input = input.trim();
        this.dialogRef.close(`${input}`);
    }
}
