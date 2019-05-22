import { Component, OnInit, ViewChild, NgZone, Renderer2, ElementRef } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { HOME } from '../../constants/routes';
import { TaskStatus, Operation } from '../../model/TaskStatus';

@Component({
    selector: 'app-nav-bar',
    templateUrl: './nav-bar.component.html',
    styleUrls: ['./nav-bar.component.scss']
})
export class NavBarComponent implements OnInit {

    @ViewChild('timer')
    public taskTimer: ElementRef;

    currentTime: string;
    taskStatus: TaskStatus;
    showPageTitle: boolean;
    activeRoute: string;
    homeRoute = HOME;

    constructor(private activatedRoute: ActivatedRoute, private router: Router, private zone: NgZone,
        private renderer: Renderer2) {
        this.activeRoute = activatedRoute.snapshot.data['title'];
        this.showPageTitle = !router.isActive(HOME, false);

        this.zone.runOutsideAngular(() => {
            setInterval(() => {
                const newTime = new Date(Date.now() - this.taskStatus.labellingTime);
                this.currentTime = `${newTime.getMinutes()}:${newTime.getSeconds()}`;
                this.renderer.setProperty(this.taskTimer.nativeElement, 'textContent', this.currentTime);
            }, 1000);
        });
    }

    ngOnInit() {}

    public changeStatusText(text: Operation) {
        this.taskStatus.changeStatusOperation(text);
    }

    public updateScanProgress() {
        this.taskStatus.updateProgress();
    }

    public trackTaskStatus(scansToLabel: number) {
        this.taskStatus = new TaskStatus(scansToLabel);
    }

    private showTaskStatus(): boolean {
        return !!this.taskStatus;
    }
}
