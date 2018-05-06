import {Component, Output, EventEmitter, ViewChild, ElementRef, Input} from '@angular/core';

const FILE_SIZE_LIMIT = 5;  // MB

export class SelectedScan {
    directory: string = '';
    files: File[] = [];
}

export class IncompatibleFile {
    file: File;
    reason: string;

    constructor(file: File, reason: string) {
        this.file = file;
        this.reason = reason;
    }
}

export class UserFiles {
    scans: SelectedScan[];
    numberOfSlices: number;
    incompatibleFiles: IncompatibleFile[];

    constructor(scans: SelectedScan[], numberOfSlices: number, incompatibleFiles: IncompatibleFile[]) {
        this.scans = scans;
        this.numberOfSlices = numberOfSlices;
        this.incompatibleFiles = incompatibleFiles;
    }
}

@Component({
    selector: 'upload-scans-selector',
    templateUrl: './upload-scans-selector.component.html'
})
export class UploadScansSelectorComponent {
    @Input() multipleScans: boolean;
    @Output() onFileSelect: EventEmitter<object> = new EventEmitter();

    @ViewChild('inputFile') nativeInputFile: ElementRef;
    private userSelectedFiles: File[] = [];

    public scans: SelectedScan[] = [];
    public totalNumberOfSlices: number = 0;
    public incompatibleFiles: IncompatibleFile[] = [];

    private isCompatibleSliceFile(sliceFile: File): boolean {
        // Skip all files that are not DICOMs
        if (sliceFile.type != "application/dicom") {
            let reason = 'Incompatible MIME Type! Should be "application/dicom" but File has type "' + sliceFile.type + '".';
            this.incompatibleFiles.push(new IncompatibleFile(sliceFile, reason));
            return false;
        }

        // Check for size limit (5 MB)
        if (sliceFile.size > FILE_SIZE_LIMIT * 1024 * 1024) {
            let fileSize = Math.round(sliceFile.size / 1024 / 1024);
            let reason = 'Too large File! This file has ' + fileSize + 'MB but the limit is ' + FILE_SIZE_LIMIT + 'MB.';
            this.incompatibleFiles.push(new IncompatibleFile(sliceFile, reason));
            return false;
        }

        return true;
    }

    private prepareScans(): void {
        // Always start with empty list and we will fill it by iterating over files
        this.scans = [];
        this.incompatibleFiles = [];

        // User didn't select any files
        if (!this.userSelectedFiles || this.userSelectedFiles.length == 0) {
            return;
        }

        // User selected single scan upload
        if (!this.multipleScans) {
            let singleScan = new SelectedScan();
            for (let sliceFile of this.userSelectedFiles) {
                // Check file compatibility and add it to the list of incompatible files
                if (!this.isCompatibleSliceFile(sliceFile)) {
                    continue;
                }

                this.totalNumberOfSlices += 1;
                singleScan.files.push(sliceFile);
            }

            // As we cannot fetch these files' directory, we've got to display something on the UI
            singleScan.directory = 'Single 3D Scan (' + this.totalNumberOfSlices + ' DICOMs)';
            this.scans.push(singleScan);
            return;
        }

        // User selected multiple scans for upload, so let's group them into the Scans
        let lastScanDirectory: String;
        let currentScan;
        for (let sliceFile of this.userSelectedFiles) {
            // Check file compatibility and add it to the list of incompatible files
            if (!this.isCompatibleSliceFile(sliceFile)) {
                continue;
            }

            // Slices that are in the same directory as others (previous ones) are considered as a single Scan
            let slicePath = sliceFile.webkitRelativePath;
            let currentScanDirectory = slicePath.split("/").slice(0, -1).join("/");
            if (currentScanDirectory != lastScanDirectory) {
                // If this is not the first iteration of the whole loop over files -> save current Scan
                if (!!lastScanDirectory) {
                    this.scans.push(currentScan);
                }

                // If we found Slice from new directory - we consider this as another Scan
                currentScan = new SelectedScan();
                currentScan.directory = currentScanDirectory;
                currentScan.files = [];
                lastScanDirectory = currentScanDirectory;
            }

            // Store given Slice to the Scan which is defined as current Scan Directory
            this.totalNumberOfSlices += 1;
            currentScan.files.push(sliceFile);
        }

        // Don't forget about current scan!
        if (!!currentScan) {
            this.scans.push(currentScan);
        }
    }

    public onNativeInputFileSelect($event): void {
        this.scans = [];
        this.incompatibleFiles = [];
        this.totalNumberOfSlices = 0;
        this.userSelectedFiles = $event.target.files || $event.scrElement.files;
        this.prepareScans();
        this.onFileSelect.emit(new UserFiles(this.scans, this.totalNumberOfSlices, this.incompatibleFiles));
    }

    public selectFile(): void {
        this.nativeInputFile.nativeElement.click();
    }

    public reinitialize(): void {
        this.userSelectedFiles = [];
        this.totalNumberOfSlices = 0;
        this.scans = [];
        this.incompatibleFiles = [];
    }
}
