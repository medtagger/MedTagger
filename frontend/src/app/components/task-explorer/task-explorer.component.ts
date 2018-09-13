import { Component, OnInit } from '@angular/core';
import {MatIconRegistry, MatSnackBar} from '@angular/material';
import {DomSanitizer} from '@angular/platform-browser';
import {TaskService} from '../../services/task.service';
import {LABELLING, LABELLING_TUTORIAL} from '../../constants/routes';
import {UserInfo} from '../../model/UserInfo';
import {Router} from '@angular/router';
import {Task} from '../../model/Task';

@Component({
  selector: 'app-task-explorer',
  templateUrl: './task-explorer.component.html',
  styleUrls: ['./task-explorer.component.scss']
})
export class TaskExplorerComponent implements OnInit {
    private user: UserInfo;
    tasks = [];
    downloadingTasksInProgress = false;
    constructor(private iconRegistry: MatIconRegistry, private sanitizer: DomSanitizer, private taskService: TaskService,
                public snackBar: MatSnackBar, private router: Router) {
        this.user = JSON.parse(sessionStorage.getItem('userInfo'));
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

    private getTaskUrl(): Array<string> {
        return [this.user.settings.skipTutorial ? '/' + LABELLING : '/' + LABELLING_TUTORIAL];
    }

    goToLabelingPage(task: Task): void {
        this.router.navigate(this.getTaskUrl(), {queryParams: {task: task.key}});
    }
}
