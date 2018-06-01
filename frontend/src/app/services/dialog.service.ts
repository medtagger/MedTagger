import {Injectable} from '@angular/core';
import {MatDialog, MatDialogRef} from '@angular/material';
import {InfoDialogComponent} from '../dialogs/info-dialog.component';

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
}
