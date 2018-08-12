import {Injectable} from '@angular/core';
import {MatDialog, MatDialogRef} from '@angular/material';
import {InfoDialogComponent} from '../dialogs/info-dialog.component';
import {InputDialogComponent} from '../dialogs/input-dialog.component';

const DIALOG_BOX_WIDTH = '450px';

@Injectable()
export class DialogService {
    constructor(public dialog: MatDialog) {}

    public openInfoDialog(title: string, content: string, buttonText?: string): MatDialogRef<any> {
        const buttonLabel: string = buttonText ? buttonText : 'Ok';

        const infoDialogRef = this.dialog.open(InfoDialogComponent, {
            width: DIALOG_BOX_WIDTH,
            data: {title: title, content: content, buttonText: buttonLabel}
        });

        return infoDialogRef;
    }

    public openInputDialog(title: string, content: string, inputData: string, buttonText?: string): MatDialogRef<any> {
        const buttonLabel: string = buttonText ? buttonText : 'Submit';

        const inputDialogRef = this.dialog.open(InputDialogComponent, {
            width: DIALOG_BOX_WIDTH,
            data: {title: title, content: content, input: inputData, buttonText: buttonLabel}
        });

        return inputDialogRef;
    }
}
