import { Injectable } from '@angular/core';
import { MatDialog, MatDialogRef } from '@angular/material';
import { InfoDialogComponent } from '../dialogs/info-dialog.component';
import { InputDialogComponent } from '../dialogs/input-dialog.component';
import { TranslateService } from '@ngx-translate/core';

const DIALOG_BOX_WIDTH = '450px';

@Injectable()
export class DialogService {
    constructor(public dialog: MatDialog, private translateService: TranslateService) {}

    public openInfoDialog(title: string, content: string, buttonText?: string): MatDialogRef<any> {
        const buttonLabel: string = buttonText ? buttonText : this.translateService.instant('SERVICE.DIALOG.OK');

        const infoDialogRef = this.dialog.open(InfoDialogComponent, {
            width: DIALOG_BOX_WIDTH,
            data: {title: title, content: content, buttonText: buttonLabel}
        });

        return infoDialogRef;
    }

    public openInputDialog(title: string, content: string, inputData: string, buttonText?: string): MatDialogRef<any> {
        const buttonLabel: string = buttonText ? buttonText : this.translateService.instant('SERVICE.DIALOG.SUBMIT');

        const inputDialogRef = this.dialog.open(InputDialogComponent, {
            width: DIALOG_BOX_WIDTH,
            data: {title: title, content: content, input: inputData, buttonText: buttonLabel}
        });

        return inputDialogRef;
    }
}
