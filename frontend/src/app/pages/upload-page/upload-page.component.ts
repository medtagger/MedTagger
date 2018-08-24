import {Component, OnInit, ViewChild} from '@angular/core';
import {MatHorizontalStepper, MatStep, MatSelectionList} from '@angular/material';
import {FormBuilder, FormGroup, FormControl, Validators} from '@angular/forms';
import {HttpErrorResponse} from '@angular/common/http';

import {ScanService} from '../../services/scan.service';
import {DatasetService} from '../../services/dataset.service';
import {ScanMetadata} from '../../model/ScanMetadata';
import {
    UploadScansSelectorComponent,
    SelectedScan,
    UserFiles,
    IncompatibleFile
} from '../../components/upload-scans-selector/upload-scans-selector.component';
import {Observable} from 'rxjs/internal/Observable';
import {interval} from 'rxjs/internal/observable/interval';
import {throwError} from 'rxjs/internal/observable/throwError';


enum UploadMode {
    SINGLE_SCAN,
    MULTIPLE_SCANS
}

enum UploadingScanStatus {
    QUEUED,
    UPLOADING,
    WAITING_FOR_PROCESSING,
    PROCESSING,
    AVAILABLE,
    ERROR
}

enum UploadStep {
    SELECT_DATASET,
    SELECT_UPLOAD_MODE,
    SELECT_SCAN,
    UPLOADING,
    SUMMARY
}

class UploadingScan {
    id = '';
    status: UploadingScanStatus = UploadingScanStatus.QUEUED;
    scan: SelectedScan;
    errorsDuringUpload = 0;

    constructor(scan: SelectedScan) {
        this.scan = scan;
    }

    public updateStatus(scanMetadata: ScanMetadata): void {
        switch (scanMetadata.status) {
            case 'STORED': {
                this.status = UploadingScanStatus.WAITING_FOR_PROCESSING;
                break;
            }
            case 'PROCESSING': {
                this.status = UploadingScanStatus.PROCESSING;
                break;
            }
            case 'AVAILABLE': {
                this.status = UploadingScanStatus.AVAILABLE;
                break;
            }
        }
    }

}


@Component({
    selector: 'app-upload-page',
    templateUrl: './upload-page.component.html',
    providers: [ScanService],
    styleUrls: ['./upload-page.component.scss']
})
export class UploadPageComponent implements OnInit {

    @ViewChild('scansForRetry') scansForRetry: MatSelectionList;
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

    incompatibleFiles: IncompatibleFile[] = [];

    slicesSent = 0;
    totalNumberOfSlices = 0;
    progress = 0.0;

    // Needed in template for comparison with Enum values
    UploadMode = UploadMode;
    UploadingScanStatus = UploadingScanStatus;

    uploadMode: UploadMode = UploadMode.SINGLE_SCAN;
    dataset: string;
    availableDatasets = [];

    chooseModeFormGroup: FormGroup;
    chooseFilesFormGroup: FormGroup;
    sendingFilesFormGroup: FormGroup;
    uploadCompletedFormGroup: FormGroup;
    chooseDatasetFormGroup: FormGroup;

    constructor(private scanService: ScanService, private datasetService: DatasetService, private formBuilder: FormBuilder) {
    }

    ngOnInit() {
        this.chooseModeFormGroup = this.formBuilder.group({
            'modeChosen': new FormControl(null, [Validators.required]),
        });
        this.chooseFilesFormGroup = this.formBuilder.group({
            'filesChosen': new FormControl(null, [Validators.required]),
        });
        this.sendingFilesFormGroup = this.formBuilder.group({
            'filesSent': new FormControl(null, [Validators.required]),
        });
        this.uploadCompletedFormGroup = this.formBuilder.group({});
        this.chooseDatasetFormGroup = this.formBuilder.group({
            'dataset': new FormControl(this.dataset, [Validators.required]),
        });
        this.datasetService.getAvailableDatasets().then((availableDatasets) => {
            this.availableDatasets = availableDatasets;
        });
    }

    public chooseFiles(userFiles: UserFiles): void {
        this.scans = userFiles.scans;
        this.totalNumberOfSlices = userFiles.numberOfSlices;
        this.incompatibleFiles = userFiles.incompatibleFiles;
    }

    private updateProgressBar(numberOfSlicesSent: number = 1): void {
        this.slicesSent += numberOfSlicesSent;
        this.progress = 100.0 * this.slicesSent / this.totalNumberOfSlices;
    }

    private pollScanUploadStatus() {
        const TIME_INTERVAL = 5000; // 5 seconds
        const subscription = interval(TIME_INTERVAL).subscribe(_ => {
            // Iteration in reverse order makes it safe to remove elements from this array
            for (let i = this.uploadingAndProcessingScans.length - 1; i >= 0; i--) {
                const scanToMonitor = this.uploadingAndProcessingScans[i];

                // Skip all Scans that were not fully created yet
                if (!scanToMonitor.id) {
                    continue;
                }

                // Check Scan status and move it to appropiate state if needed
                this.scanService.getScanForScanId(scanToMonitor.id).then((metadata: ScanMetadata) => {
                    scanToMonitor.updateStatus(metadata);
                }, (error: HttpErrorResponse) => {
                    // Scan was removed from MedTagger due to all files corrupted
                    if (error.status === 404) {
                        scanToMonitor.status = UploadingScanStatus.ERROR;
                    }
                });

                // Move all errored and available Scans to uploaded array, so we won't monitor them again
                switch (scanToMonitor.status) {
                    case UploadingScanStatus.ERROR: {
                        this.uploadingAndProcessingScans.splice(i, 1);
                        this.errorScans.push(scanToMonitor);
                        break;
                    }
                    case UploadingScanStatus.AVAILABLE: {
                        this.uploadingAndProcessingScans.splice(i, 1);
                        this.availableScans.push(scanToMonitor);
                        break;
                    }
                }
            }

            // End polling once we've uploaded all Scans
            if (this.errorScans.length + this.availableScans.length === this.scans.length) {
                console.log('We\'ve uploaded all Scans, let\'s move on!');
                subscription.unsubscribe();
                this.sendingFilesFormGroup.controls['filesSent'].setValue('true');
                this.stepper.next();
            }
        });
    }

    public async uploadFiles(): Promise<void> {
        this.chooseFilesFormGroup.controls['filesChosen'].setValue('true');
        this.stepper.next();

        this.slicesSent = 0;
        this.progress = 0.0;

        // Queue all Scans
        this.queuedScans = [];
        this.uploadingAndProcessingScans = [];
        this.availableScans = [];
        this.errorScans = [];
        for (const scan of this.scans) {
            this.queuedScans.push(new UploadingScan(scan));
        }

        // Run polling of Scans upload progress in parallel to the uploading Scans
        this.pollScanUploadStatus();

        // Upload all queued Scans one by one
        while (this.queuedScans.length > 0) {
            const queuedScan = this.queuedScans.pop();
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
        const numberOfAllSlices = uploadingScan.scan.files.length;
        let numberOfSlicesSent = 0;
        return new Promise<void>((resolve, reject) => {
            this.uploadSingleScan(uploadingScan).then((newScan) => {
                console.log('Upload has started!');
                newScan.subscribe(
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
            }, (error: HttpErrorResponse) => {
                console.log('Could not create new Scan.');
                reject();
            });
        });
    }

    private uploadSingleScan(uploadingScan: UploadingScan): Promise<Observable<any | never>> {
        const dataset = this.chooseDatasetFormGroup.get('dataset').value;
        const numberOfSlices = uploadingScan.scan.files.length;

        return this.scanService.createNewScan(dataset, numberOfSlices).then((scanId: string) => {
                console.log('New Scan created with ID:', scanId, ', number of Slices:', numberOfSlices);
                uploadingScan.id = scanId;
                return this.scanService.uploadSlices(scanId, uploadingScan.scan.files);
            },
            () => {
                return throwError({error: 'Could not create Scan.'});
            });
    }

    private resetFormGroup(formGroup: FormGroup): void {
        formGroup.reset();
    }

    public restart(): void {
        this.resetFormGroup(this.chooseDatasetFormGroup);
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
        this.errorScans = [];
        this.incompatibleFiles = [];
        this.totalNumberOfSlices = 0;
        this.slicesSent = 0;

        if (!!this.scansForRetry && !!this.scansForRetry.selectedOptions) {
            this.scansForRetry.selectedOptions.clear();
        }
        this.stepper.reset();
    }

    public uploadAgain(): void {
        this.scans = [];
        this.incompatibleFiles = [];
        this.totalNumberOfSlices = 0;
        for (const listElement of this.scansForRetry.selectedOptions.selected) {
            this.totalNumberOfSlices += listElement.value.scan.files.length;
            this.scans.push(listElement.value.scan);
        }

        // Clear Upload and Summary page and go to the Uploading view triggering upload
        this.resetFormGroup(this.sendingFilesFormGroup);
        this.resetFormGroup(this.uploadCompletedFormGroup);
        this.sendingFilesStep.completed = false;
        this.uploadCompletedStep.completed = false;
        this.scansForRetry.selectedOptions.clear();
        this.stepper.selectedIndex = UploadStep.UPLOADING;
        this.uploadFiles();
    }

    public isGoogleChrome(): boolean {
        // TODO: It would be nice to check if there is some lib that does it for us
        // For now, this ugly method was taken (nearly) as-is from: https://stackoverflow.com/a/13348618
        const isChromium = (window as any).chrome,
            winNav = window.navigator,
            vendorName = winNav.vendor,
            isOpera = winNav.userAgent.indexOf('OPR') > -1,
            isIEedge = winNav.userAgent.indexOf('Edge') > -1,
            isIOSChrome = winNav.userAgent.match('CriOS');

        if (isIOSChrome) {
            return false; // We don't want to support mobile devices
        } else if (
            isChromium !== null &&
            typeof isChromium !== 'undefined' &&
            vendorName === 'Google Inc.' &&
            isOpera === false &&
            isIEedge === false
        ) {
            return true;
        } else {
            return false;
        }
    }

    public selectUploadMode(uploadMode: UploadMode): void {
        this.uploadMode = uploadMode;
        this.chooseModeFormGroup.controls['modeChosen'].setValue('true');
        this.stepper.next();
    }
}
