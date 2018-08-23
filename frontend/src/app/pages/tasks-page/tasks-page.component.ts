import {Component, OnInit} from '@angular/core';
import {MatSnackBar, MatIconRegistry} from '@angular/material';
import {DomSanitizer} from '@angular/platform-browser';

import {TaskService} from '../../services/task.service';

@Component({
    selector: 'app-tasks-page',
    templateUrl: './tasks-page.component.html',
    styleUrls: ['./tasks-page.component.scss']
})
export class TasksPageComponent implements OnInit {

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
