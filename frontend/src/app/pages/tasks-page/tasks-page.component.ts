import {Component, OnInit} from '@angular/core';
import {MatSnackBar, MatIconRegistry} from '@angular/material';
import {DomSanitizer} from '@angular/platform-browser';

import {ScanService} from '../../services/scan.service';

@Component({
    selector: 'app-category-page',
    templateUrl: './tasks-page.component.html',
    providers: [ScanService],
    styleUrls: ['./tasks-page.component.scss']
})
export class TasksPageComponent implements OnInit {

    tasks = [];
    downloadingTasksInProgress = false;
    constructor(private iconRegistry: MatIconRegistry, private sanitizer: DomSanitizer, private scanService: ScanService,
                public snackBar: MatSnackBar) {
    }

    ngOnInit() {
      this.downloadingTasksInProgress = true;
        this.scanService.getTasks().then((tasks) => {
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
