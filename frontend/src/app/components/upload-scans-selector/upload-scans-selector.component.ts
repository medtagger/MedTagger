import {Component, Output, EventEmitter, ViewChild, ElementRef, Input} from '@angular/core';

const FILE_SIZE_LIMIT = 5;  // MB

export class SelectedScan {
    directory = '';
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
    selector: 'app-upload-scans-selector',
    templateUrl: './upload-scans-selector.component.html'
})
export class UploadScansSelectorComponent {
    @Input() multipleScans: boolean;
    @Output() onFileSelect: EventEmitter<object> = new EventEmitter();

    @ViewChild('inputFile') nativeInputFile: ElementRef;
    private userSelectedFiles: File[] = [];

    public scans: SelectedScan[] = [];
    public totalNumberOfSlices = 0;
    public incompatibleFiles: IncompatibleFile[] = [];

    // https://en.wikipedia.org/wiki/List_of_file_signatures -> dicom format
    private DICOM_BYTE_SIGNATURE = '4449434D';
    private DICOM_BYTE_SIGNATURE_OFFSET = 128;

    private async isCompatibleSliceFile(sliceFile: File): Promise<boolean> {
        let isCompatible = null;

        // Skip all files that are not DICOMs
        await this.isFileDicom(sliceFile).then(() => {
            // Check for size limit (5 MB)
            if (sliceFile.size > FILE_SIZE_LIMIT * 1024 * 1024) {
                const fileSize = Math.round(sliceFile.size / 1024 / 1024);
                const reason = 'Too large File! This file has ' + fileSize + 'MB but the limit is ' + FILE_SIZE_LIMIT + 'MB.';
                this.incompatibleFiles.push(new IncompatibleFile(sliceFile, reason));
                isCompatible = false;
            }

            isCompatible = true;
        }, (error: Error) => {
            const reason = 'Incompatible MIME Type! Should be "application/dicom" but File has type "' + sliceFile.type + '".';
            console.log(reason, error);
            this.incompatibleFiles.push(new IncompatibleFile(sliceFile, reason));
            isCompatible = false;
        });

        return isCompatible;
    }

    private async isFileDicom(sliceFile: File): Promise<any> {
        return new Promise(((resolve, reject) => {
            if (sliceFile.type === 'application/dicom') {
                resolve();
            } else {
                const fileReader: FileReader = new FileReader();

                fileReader.onloadend = (e: ProgressEvent) => {
                    const fileHeaderBytes = new Uint8Array(fileReader.result);

                    const singatureBytesValues: string[] = [];

                    fileHeaderBytes.forEach((byte) => {
                        singatureBytesValues.push(byte.toString(16));
                    });

                    const fileSignature: string = singatureBytesValues.join('').toUpperCase();

                    if (fileSignature === this.DICOM_BYTE_SIGNATURE) {
                        resolve();
                    } else {
                        reject(new Error('Non dicom file!'));
                    }
                };
                const blob = sliceFile.slice(this.DICOM_BYTE_SIGNATURE_OFFSET, this.DICOM_BYTE_SIGNATURE_OFFSET + 4);
                fileReader.readAsArrayBuffer(blob);
            }
        }));
    }

    private prepareScans(): Promise<void> {
        // Always start with empty list and we will fill it by iterating over files
        this.scans = [];
        this.incompatibleFiles = [];

        // User didn't select any files
        if (!this.userSelectedFiles || this.userSelectedFiles.length === 0) {
            return Promise.resolve();
        }

        // User selected single scan upload
        if (!this.multipleScans) {
            return this.prepareSingleScan();
        }

        return this.prepareMultipleScans();
    }

    private prepareSingleScan(): Promise<void> {
        const slicePromises: Array<Promise<any>> = [];
        const singleScan = new SelectedScan();
        for (const sliceFile of this.userSelectedFiles) {
            // Check file compatibility and add it to the list of incompatible files
            slicePromises.push(this.isCompatibleSliceFile(sliceFile).then((isCompatible: boolean) => {
                if (isCompatible) {
                    this.totalNumberOfSlices += 1;
                    singleScan.files.push(sliceFile);
                }
            }));
        }

        // As we cannot fetch these files' directory, we've got to display something on the UI
        return Promise.all(slicePromises)
            .then(() => {
                singleScan.directory = 'Single 3D Scan (' + this.totalNumberOfSlices + ' DICOMs)';
                this.scans.push(singleScan);
            });
    }

    private prepareMultipleScans(): Promise<void> {
        const slicePromises: Array<Promise<any>> = [];
        let lastScanDirectory: String;

        // User selected multiple scans for upload, so let's group them into the Scans
        let currentScan;

        for (const sliceFile of this.userSelectedFiles) {
            // Check file compatibility and add it to the list of incompatible files
            slicePromises.push(this.isCompatibleSliceFile(sliceFile).then((isCompatible: boolean) => {
                if (isCompatible) {
                    // Slices that are in the same directory as others (previous ones) are considered as a single Scan
                    const slicePath = sliceFile.webkitRelativePath;
                    const currentScanDirectory = slicePath.split('/').slice(0, -1).join('/');
                    if (currentScanDirectory !== lastScanDirectory) {
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
            }));
        }

        return Promise.all(slicePromises)
            .then(() => {
                // Don't forget about current scan!
                if (!!currentScan) {
                    this.scans.push(currentScan);
                }
            });
    }

    public onNativeInputFileSelect($event): void {
        this.scans = [];
        this.incompatibleFiles = [];
        this.totalNumberOfSlices = 0;
        this.userSelectedFiles = $event.target.files || $event.scrElement.files;
        this.prepareScans().then(() => {
            this.onFileSelect.emit(new UserFiles(this.scans, this.totalNumberOfSlices, this.incompatibleFiles));
        });
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
