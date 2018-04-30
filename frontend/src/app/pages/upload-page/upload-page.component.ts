import {Component, OnInit, ViewChild} from '@angular/core';
import {MatHorizontalStepper, MatStep} from '@angular/material';
import {FormBuilder, FormGroup, FormControl, Validators} from '@angular/forms';
import {Observable} from 'rxjs/Rx';

import {ScanService} from '../../services/scan.service';
import {ScanMetadata} from '../../model/ScanMetadata';
import {UploadScansSelectorComponent, SelectedScan} from "../../components/upload-scans-selector/upload-scans-selector.component";


enum UploadMode {
    SINGLE_SCAN,
    MULTIPLE_SCANS
}

enum UploadingScanStatus {
    QUEUED,
    UPLOADING,
    PROCESSING,
    AVAILABLE,
    ERROR
}

class UploadingScan {
    id: string = '';
    status: UploadingScanStatus = UploadingScanStatus.QUEUED;
    scan: SelectedScan;

    constructor(scan: SelectedScan) {
        this.scan = scan;
    }
}


@Component({
    selector: 'app-upload-page',
    templateUrl: './upload-page.component.html',
    providers: [ScanService],
    styleUrls: ['./upload-page.component.scss']
})
export class UploadPageComponent implements OnInit {

    @ViewChild('stepper') stepper: MatHorizontalStepper;
    @ViewChild('chooseModeStep') chooseModeStep: MatStep;
    @ViewChild('chooseFilesStep') chooseFilesStep: MatStep;
    @ViewChild('sendingFilesStep') sendingFilesStep: MatStep;
    @ViewChild('uploadCompletedStep') uploadCompletedStep: MatStep;
    @ViewChild('uploadSingleScanSelector') uploadSingleScanSelector: UploadScansSelectorComponent;
    @ViewChild('uploadMultipleScansSelector') uploadMultipleScansSelector: UploadScansSelectorComponent;

    scans: Array<SelectedScan> = [];
    queuedScans: Array<UploadingScan> = [];
    uploadingAndProcessingScans: Array<UploadingScan> = [];
    availableScans: Array<UploadingScan> = [];
    errorScans: Array<UploadingScan> = [];
    
    slicesSent: number = 0;
    totalNumberOfSlices: number = 0;
    progress: number = 0.0;
    
    // Needed in template for comparison with Enum values
    UploadMode = UploadMode;
    UploadingScanStatus = UploadingScanStatus;

    uploadMode: UploadMode = UploadMode.SINGLE_SCAN;
    category: string;
    availableCategories = [];

    chooseModeFormGroup: FormGroup;
    chooseFilesFormGroup: FormGroup;
    sendingFilesFormGroup: FormGroup;
    uploadCompletedFormGroup: FormGroup;
    chooseCategoryFormGroup: FormGroup;

    constructor(private scanService: ScanService, private formBuilder: FormBuilder) {}

    ngOnInit() {
        this.chooseModeFormGroup = this.formBuilder.group({});
        this.chooseFilesFormGroup = this.formBuilder.group({});
        this.sendingFilesFormGroup = this.formBuilder.group({});
        this.uploadCompletedFormGroup = this.formBuilder.group({});
        this.chooseCategoryFormGroup = this.formBuilder.group({
            'category': new FormControl(this.category, [Validators.required]),
        });
        this.scanService.getAvailableCategories().then((availableCategories) => {
            this.availableCategories = availableCategories;
        });
    }

    public chooseFiles($event): void {
        this.scans = $event.scans;
        this.totalNumberOfSlices = $event.totalNumberOfSlices;
    }

    private updateProgressBar(numberOfSlicesSent: number = 1): void {
        this.slicesSent += numberOfSlicesSent;
        this.progress = 100.0 * this.slicesSent / this.totalNumberOfSlices;
    }

    private pollScanUploadStatus() {
        let TIME_INTERVAL = 5000; // 5 seconds
        var subscription = Observable.interval(TIME_INTERVAL).subscribe(_ => {
            // Iteration in reverse order makes it safe to remove elements from this array
            for (let i = this.uploadingAndProcessingScans.length - 1; i >= 0; i--) {
                let scanToMonitor = this.uploadingAndProcessingScans[i];

                // Skip all Scans that were not fully created yet
                if (!scanToMonitor.id) {
                    continue;
                }

                // Check Scan status and move it to appropiate state if needed
                this.scanService.getScanForScanId(scanToMonitor.id).then((metadata: ScanMetadata) => {
                    console.log(metadata);
                    if (metadata.status == 'STORED' || metadata.status == 'PROCESSING') {
                        scanToMonitor.status = UploadingScanStatus.PROCESSING;
                    }
                    if (metadata.status == 'AVAILABLE') {
                        scanToMonitor.status = UploadingScanStatus.AVAILABLE;
                    }
                }, _ => {
                    // Scan was removed from MedTagger due to all files corrupted
                    scanToMonitor.status = UploadingScanStatus.ERROR;
                });

                // Move all errored and available Scans to uploaded array, so we won't monitor them again
                if (scanToMonitor.status === UploadingScanStatus.ERROR) {
                    this.uploadingAndProcessingScans.splice(i, 1);
                    this.errorScans.push(scanToMonitor);
                }
                if (scanToMonitor.status === UploadingScanStatus.AVAILABLE) {
                    this.uploadingAndProcessingScans.splice(i, 1);
                    this.availableScans.push(scanToMonitor);
                }
            }

            // End polling once we've uploaded all Scans
            if (this.errorScans.length + this.availableScans.length === this.scans.length) {
                console.log('We\'ve uploaded all Scans, let\'s move on!');
                subscription.unsubscribe();
                this.stepper.next();
            }
        });
    }
    
    public async uploadFiles(): Promise<void> {
        this.slicesSent = 0;
        this.progress = 0.0;

        // Queue all Scans
        this.queuedScans = [];
        this.uploadingAndProcessingScans = [];
        this.availableScans = [];
        this.errorScans= [];
        for (let scan of this.scans) {
            this.queuedScans.push(new UploadingScan(scan));
        }

        // Run polling of Scans upload progress in parallel to the uploading Scans
        this.pollScanUploadStatus();

        // Upload all queued Scans one by one
        while (this.queuedScans.length > 0) {
            let queuedScan = this.queuedScans.pop();
            queuedScan.status = UploadingScanStatus.UPLOADING;
            this.uploadingAndProcessingScans.push(queuedScan);
            try {
                await this.asyncUploadSingleScan(queuedScan);
            } catch (error) {
                queuedScan.status = UploadingScanStatus.ERROR;
            }
        }
    }

    private asyncUploadSingleScan(uploadingScan: UploadingScan): Promise<void> {
        let numberOfAllSlices = uploadingScan.scan.files.length;
        var numberOfSlicesSent = 0;
        return new Promise<void>((resolve, reject) => {
            this.uploadSingleScan(uploadingScan).subscribe(
                _ => {
                    this.updateProgressBar();
                    numberOfSlicesSent += 1;
                },
                _ => {
                    this.updateProgressBar(numberOfAllSlices - numberOfSlicesSent);
                    reject();
                },
                () => resolve(),
            );
        });
    }

    private uploadSingleScan(uploadingScan: UploadingScan): Observable<any> {
        let category = this.chooseCategoryFormGroup.get('category').value;
        let numberOfSlices = uploadingScan.scan.files.length;

        return Observable.defer(
            () => this.scanService.createNewScan(category, numberOfSlices)
        ).flatMap((scanId: string) => {
            console.log('New Scan created with ID:', scanId, ', number of Slices:', numberOfSlices);
            uploadingScan.id = scanId;
            return this.scanService.uploadSlices(scanId, uploadingScan.scan.files);
        });
    }

    private resetFormGroup(formGroup: FormGroup): void {
        formGroup.reset();
        formGroup.markAsUntouched();
        Object.keys(formGroup.controls).forEach((name) => {
            let control = formGroup.controls[name];
            control.setErrors(null);
        });
    }

    public restart() {
        this.resetFormGroup(this.chooseCategoryFormGroup);
        this.resetFormGroup(this.chooseModeFormGroup);
        this.resetFormGroup(this.chooseFilesFormGroup);
        this.resetFormGroup(this.sendingFilesFormGroup);
        this.resetFormGroup(this.uploadCompletedFormGroup);

        if (this.uploadSingleScanSelector) {
            this.uploadSingleScanSelector.reinitialize();
        }

        if (this.uploadMultipleScansSelector) {
            this.uploadMultipleScansSelector.reinitialize();
        }

        this.scans = [];
        this.queuedScans = [];
        this.uploadingAndProcessingScans = [];
        this.availableScans = [];
        this.errorScans= [];
        this.totalNumberOfSlices = 0;
        this.slicesSent = 0;

        this.chooseModeStep.completed = false;
        this.chooseFilesStep.completed = false;
        this.sendingFilesStep.completed = false;
        this.uploadCompletedStep.completed = false;
        this.stepper.selectedIndex = 0;
    }

    public isGoogleChrome(): boolean {
        // TODO: It would be nice to check if there is some lib that does it for us
        // For now, this ugly method was taken (nearly) as-is from: https://stackoverflow.com/a/13348618
        var isChromium = (window as any).chrome,
            winNav = window.navigator,
            vendorName = winNav.vendor,
            isOpera = winNav.userAgent.indexOf("OPR") > -1,
            isIEedge = winNav.userAgent.indexOf("Edge") > -1,
            isIOSChrome = winNav.userAgent.match("CriOS");

        if (isIOSChrome) {
            return false; // We don't want to support mobile devices
        } else if (
            isChromium !== null &&
            typeof isChromium !== "undefined" &&
            vendorName === "Google Inc." &&
            isOpera === false &&
            isIEedge === false
        ) {
            return true;
        } else {
            return false;
        }
    }
}
