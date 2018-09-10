import { Component, OnInit } from '@angular/core';
import {MatIconRegistry, MatSnackBar} from "@angular/material";
import {DomSanitizer} from "@angular/platform-browser";
import {TaskService} from "../../services/task.service";

@Component({
  selector: 'app-task-explorer',
  templateUrl: './task-explorer.component.html',
  styleUrls: ['./task-explorer.component.scss']
})
export class TaskExplorerComponent implements OnInit {

    tasks = [];
    downloadingTasksInProgress = false;
    constructor(private iconRegistry: MatIconRegistry, private sanitizer: DomSanitizer, private taskService: TaskService,
                public snackBar: MatSnackBar) {
    }

    ngOnInit() {
        this.downloadingTasksInProgress = true;
        this.taskService.getTasks().then((tasks) => {
            this.tasks = tasks;
            for (const task of tasks) {
                this.iconRegistry.addSvgIcon(task.key, this.sanitizer.bypassSecurityTrustResourceUrl(task.imagePath));
            }
            this.downloadingTasksInProgress = false;
        }, () => {
            this.downloadingTasksInProgress = false;
            this.snackBar.open('There was an error while downloading tasks', 'Close', {
                duration: 5000,
            });
        });
    }
}
