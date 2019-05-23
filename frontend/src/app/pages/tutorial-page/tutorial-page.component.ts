import { Component, OnInit } from '@angular/core';
import { FormControl } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { UsersService } from '../../services/users.service';
import { UserInfo } from '../../model/UserInfo';
import { UserSettings } from '../../model/UserSettings';
import * as appRoutes from '../../constants/routes';

@Component({
    selector: 'app-tutorial-page',
    templateUrl: './tutorial-page.component.html',
    styleUrls: ['./tutorial-page.component.scss'],
    providers: [UsersService]
})
export class TutorialPageComponent implements OnInit {

    doNotShowAgain = new FormControl(true);

    private readonly user: UserInfo;

    constructor(private route: ActivatedRoute,
                private router: Router,
                private usersService: UsersService) {
        this.user = JSON.parse(sessionStorage.getItem('userInfo'));
    }

    ngOnInit() {
    }

    public endTutorial(): void {
        if (this.doNotShowAgain.value) {
            const settings = new UserSettings();
            settings.skipTutorial = true;
            this.usersService.setUserSettings(this.user.id, settings).then(() => {
                this.user.settings.skipTutorial = true;
                sessionStorage.setItem('userInfo', JSON.stringify(this.user));
            });
        }
        this.router.navigate(['/' + appRoutes.HOME]);
    }
}
