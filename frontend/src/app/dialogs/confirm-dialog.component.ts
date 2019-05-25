import { Component, Inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material';

@Component({
    selector: 'app-info-dialog',
    templateUrl: 'confirm-dialog.component.html'
})
export class ConfirmDialogComponent {

    constructor(public dialogRef: MatDialogRef<ConfirmDialogComponent>,
        @Inject(MAT_DIALOG_DATA) public data:
            {
                title: string,
                content: string,
                buttonConfirm: string,
                buttonCancel: string
            }
    ) {}

    confirmDialog(): void {
        this.dialogRef.close({confirmed: true});
    }

    closeDialog(): void {
        this.dialogRef.close({confirmed: false});
    }
}
