import {Component, Inject} from "@angular/core";
import {MAT_DIALOG_DATA, MatDialogRef} from "@angular/material";

@Component({
  selector: 'app-info-dialog',
  templateUrl: 'info.dialog.html',
  styleUrls: ['./all.dialog.scss']
})
export class InfoDialog {

  constructor(
    public dialogRef: MatDialogRef<InfoDialog>,
    @Inject(MAT_DIALOG_DATA) public data: {title: string, content: string, buttonText: string}) { }

  closeDialog(): void {
    this.dialogRef.close();
  }
}
