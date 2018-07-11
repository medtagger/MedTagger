import {Injectable} from '@angular/core';
import {MatDialog, MatDialogRef} from '@angular/material';
import {InfoDialogComponent} from '../dialogs/info-dialog.component';
import {InputDialogComponent} from '../dialogs/input-dialog.component';

@Injectable()
export class DialogService {
    constructor(public dialog: MatDialog) {}

    public openInfoDialog(title: string, content: string, buttonText?: string): MatDialogRef<any> {
        const buttonLabel: string = buttonText ? buttonText : 'Ok';

        const infoDialogRef = this.dialog.open(InfoDialogComponent, {
            width: '450px',
            data: {title: title, content: content, buttonText: buttonLabel}
        });

        return infoDialogRef;
    }

    public openInputDialog(title: string, content: string, buttonText?: string): MatDialogRef<any> {
        const buttonLabel: string = buttonText ? buttonText : 'Submit';

        const inputDialogRef = this.dialog.open(InputDialogComponent, {
            width: '450px',
            data: {title: title, content: content, buttonText: buttonLabel}
        });

        return inputDialogRef;
    }
}
