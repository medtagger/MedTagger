import {Component, Inject} from '@angular/core';
import {MAT_DIALOG_DATA, MatDialogRef} from '@angular/material';

@Component({
    selector: 'app-info-dialog',
    templateUrl: 'info-dialog.component.html',
    styleUrls: ['./all.dialog.scss']
})
export class InfoDialogComponent {

    constructor(public dialogRef: MatDialogRef<InfoDialogComponent>,
                @Inject(MAT_DIALOG_DATA) public data: { title: string, content: string, buttonText: string }) {
    }

    closeDialog(): void {
        this.dialogRef.close();
    }
}
