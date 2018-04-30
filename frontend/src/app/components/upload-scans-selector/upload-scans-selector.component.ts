import {Component, Output, EventEmitter, ViewChild, ElementRef, Input} from '@angular/core';

export class SelectedScan {
    directory: string = '';
    files: File[] = [];
}

@Component({
    selector: 'upload-scans-selector',
    templateUrl: './upload-scans-selector.component.html'
})
export class UploadScansSelectorComponent {
    @Input() multipleScans: boolean;
    @Output() onFileSelect: EventEmitter<object> = new EventEmitter();

    @ViewChild('inputFile') nativeInputFile: ElementRef;
    private userSelectedFiles: File[];

    public scans: Array<SelectedScan> = [];
    public totalNumberOfSlices: number = 0;

    prepareScans() {
        // User didn't select any files
        if (!this.userSelectedFiles || this.userSelectedFiles.length == 0) {
            this.scans = [];
        }

        // User selected single scan upload
        if (!this.multipleScans) {
            var singleScan = new SelectedScan();
            for (let sliceFile of this.userSelectedFiles) {
                // Skip all files that are not DICOMs
                if (sliceFile.type != "application/dicom") {
                    continue;
                }

                // Check for size limit (5 MB)
                if (sliceFile.size > 5 * 1024 * 1024) {
                    continue;
                }

                // File seems to be fine
                this.totalNumberOfSlices += 1;
                singleScan.files.push(sliceFile);
            }

            // As we cannot fetch these files' directory, we've got to display something on the UI
            singleScan.directory = 'Single 3D Scan (' + this.totalNumberOfSlices + ' DICOMs)';
            this.scans.push(singleScan);
            return;
        }

        // User selected multiple scans for upload, so let's group them into the Scans
        var lastScanDirectory: String;
        var currentScan;
        for (let sliceFile of this.userSelectedFiles) {
            // Skip all files that are not DICOMs
            if (sliceFile.type != "application/dicom") {
                continue;
            }

            // Check for size limit (5 MB)
            if (sliceFile.size > 5 * 1024 * 1024) {
                continue;
            }

            // Slices that are in the same directory as others (previous ones) are considered as a single Scan
            var slicePath = sliceFile.webkitRelativePath;
            var currentScanDirectory = slicePath.split("/").slice(0, -1).join("/");
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
        this.scans.push(currentScan);
    }

    onNativeInputFileSelect($event) {
        this.scans = [];
        this.totalNumberOfSlices = 0;
        this.userSelectedFiles = $event.target.files || $event.scrElement.files;
        this.prepareScans();
        this.onFileSelect.emit(this);
    }

    selectFile() {
        this.nativeInputFile.nativeElement.click();
    }

    public reinitialize(): void {
        this.userSelectedFiles = [];
        this.totalNumberOfSlices = 0;
        this.scans = [];
    }
}
