import {Component, ViewChild, OnInit} from '@angular/core';
import {MatHorizontalStepper} from '@angular/material';
import {FormBuilder, FormControl, FormGroup} from '@angular/forms';
import {Router} from '@angular/router';
import {UsersService} from '../../services/users.service';
import {UserInfo} from '../../model/UserInfo';
import {UserSettings} from '../../model/UserSettings';


@Component({
    selector: 'app-marker-tutorial-page',
    templateUrl: './marker-tutorial-page.component.html',
    styleUrls: ['./marker-tutorial-page.component.scss'],
    providers: [UsersService]
})
export class MarkerTutorialPageComponent implements OnInit {

    @ViewChild('firstStepVideo') firstStepVideo;
    @ViewChild('secondStepVideo') secondStepVideo;
    @ViewChild('thirdStepVideo') thirdStepVideo;
    @ViewChild('fourthStepVideo') fourthStepVideo;

    formGroup: FormGroup;
    @ViewChild('stepper') stepper: MatHorizontalStepper;

    doNotShowAgain = new FormControl(true);

    private readonly user: UserInfo;

    constructor(private _formBuilder: FormBuilder, private router: Router, private usersService: UsersService) {
        this.user = JSON.parse(sessionStorage.getItem('userInfo'));
    }

    ngOnInit() {
        this.formGroup = this._formBuilder.group({});
        this.playFirstStepVideo();

        this.stepper.selectionChange.subscribe((event) => {
            switch (event.selectedIndex) {
                case 0: {
                    this.playFirstStepVideo();
                    break;
                }
                case 1: {
                    this.playSecondStepVideo();
                    break;
                }
                case 2: {
                    this.playThirdStepVideo();
                    break;
                }
                case 3: {
                    this.playFourthStepVideo();
                    break;
                }
            }
        });
    }

    playFirstStepVideo() {
        this.firstStepVideo.nativeElement.play();
        this.secondStepVideo.nativeElement.pause();
        this.thirdStepVideo.nativeElement.pause();
        this.fourthStepVideo.nativeElement.pause();
    }

    playSecondStepVideo() {
        this.firstStepVideo.nativeElement.pause();
        this.secondStepVideo.nativeElement.play();
        this.thirdStepVideo.nativeElement.pause();
        this.fourthStepVideo.nativeElement.pause();
    }

    playThirdStepVideo() {
        this.firstStepVideo.nativeElement.pause();
        this.secondStepVideo.nativeElement.pause();
        this.thirdStepVideo.nativeElement.play();
        this.fourthStepVideo.nativeElement.pause();
    }

    playFourthStepVideo() {
        this.firstStepVideo.nativeElement.pause();
        this.secondStepVideo.nativeElement.pause();
        this.thirdStepVideo.nativeElement.pause();
        this.fourthStepVideo.nativeElement.play();
    }

    public endTutorial(): void {
        if (this.doNotShowAgain.value) {
            const settings = new UserSettings();
            settings.skipTutorial = true;
            this.usersService.setUserSettings(this.user.id, settings).then(() => {
                this.user.settings.skipTutorial = true;
                sessionStorage.setItem('userInfo', JSON.stringify(this.user));
                this.router.navigateByUrl('/labelling/choose-task');
            });
        } else {
            this.router.navigateByUrl('/labelling/choose-task');
        }
    }
}
