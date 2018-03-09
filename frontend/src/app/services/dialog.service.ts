import {Injectable} from "@angular/core";
import {MatDialog, MatDialogRef} from "@angular/material";
import {InfoDialog} from "../dialogs/info.dialog";

@Injectable()
export class DialogService {
  constructor(public dialog: MatDialog) {}

  public openInfoDialog(title: string, content: string, buttonText?: string): MatDialogRef<any> {
    let buttonLabel: string = buttonText ? buttonText : "Ok";

    let infoDialogRef = this.dialog.open(InfoDialog, {
      width: '250px',
      data: { title: title, content: content, buttonText: buttonLabel}
    });

    return infoDialogRef;
  }
}
