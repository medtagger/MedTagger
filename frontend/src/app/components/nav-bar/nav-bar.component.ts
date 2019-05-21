import { Component, OnInit, ViewChild } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { HOME } from '../../constants/routes';
import { TaskStatus } from '../../model/TaskStatus';
import { simpleTimer } from '../../utils/SimpleTimer';

@Component({
    selector: 'app-nav-bar',
    templateUrl: './nav-bar.component.html',
    styleUrls: ['./nav-bar.component.scss']
})
export class NavBarComponent implements OnInit {

    taskStatus: TaskStatus;
    showPageTitle: boolean;
    activeRoute: string;
    homeRoute = HOME;

    constructor(private activatedRoute: ActivatedRoute, private router: Router) {
        this.activeRoute = activatedRoute.snapshot.data['title'];
        this.showPageTitle = !router.isActive(HOME, false);
    }

    ngOnInit() {}

    public trackTaskStatus(scansToLabel: number) {
        this.taskStatus = new TaskStatus(scansToLabel);
    }

    private showTaskStatus(): boolean {
        return !!this.taskStatus;
    }

}
