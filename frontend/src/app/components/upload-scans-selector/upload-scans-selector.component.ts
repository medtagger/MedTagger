import {Component, Output, EventEmitter, ViewChild, ElementRef, Input} from '@angular/core';

@Component({
    selector: 'upload-scans-selector',
    templateUrl: './upload-scans-selector.component.html'
})
export class UploadScansSelectorComponent {
    @Input() multipleScans: boolean;
    @Output() onFileSelect: EventEmitter<object> = new EventEmitter();

    @ViewChild('inputFile') nativeInputFile: ElementRef;

    private _files: File[];

    public numberOfSlices: number = 0;
    public numberOfScans: number = 0;
    public scans: object = {};  // TODO: Convert this dictionary (key: path, value: files) to list of stuctures

    prepareScans() {
        // User didn't select any files
        if (!this._files || this._files.length == 0) {
            this.numberOfScans = 0;
            this.numberOfSlices = 0;
            this.scans = {};
        }

        // User selected single scan upload
        if (!this.multipleScans) {
            this.scans = {
                "singleScan": []
            };
            for (let sliceFile of this._files) {
                // Skip all files that are not DICOMs
                if (sliceFile.type != "application/dicom") {
                    continue;
                }

                // Check for size limit (5 MB)
                if (sliceFile.size > 5 * 1024 * 1024) {
                    continue;
                }

                // File seems to be fine
                this.scans["singleScan"].push(sliceFile);
            }
            this.numberOfScans = 1;
            this.numberOfSlices = this.scans["singleScan"] && this.scans["singleScan"].length || 0;
            return;
        }

        // User selected multiple scans for upload, so let's group them into the Scans
        this.numberOfScans = 0;
        this.numberOfSlices = 0;
        var lastScanDirectory: String;
        for (let sliceFile of this._files) {
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
                // If we found Slice from new directory - we consider this as another Scan
                lastScanDirectory = currentScanDirectory;
                this.scans[currentScanDirectory] = [];
                this.numberOfScans++;
            }

            // Store given Slice to the Scan which is defined as current Scan Directory
            this.numberOfSlices++;
            this.scans[currentScanDirectory].push(sliceFile);
        }
    }

    onNativeInputFileSelect($event) {
        this._files = $event.target.files || $event.scrElement.files;
        this.prepareScans();
        this.onFileSelect.emit(this);
    }

    selectFile() {
        this.nativeInputFile.nativeElement.click();
    }

    public reinitialize(): void {
        this._files = [];

        this.numberOfSlices = 0;
        this.numberOfScans = 0;
        this.scans = {};
    }
}
