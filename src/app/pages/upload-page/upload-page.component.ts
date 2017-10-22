import { Component, OnInit, ViewChild } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';

import { ScanService } from '../../services/scan.service'


enum UploadMode {
  SINGLE_SCAN,
  MULTIPLE_SCANS
}


@Component({
  selector: 'app-upload-page',
  templateUrl: './upload-page.component.html',
  providers: [ScanService],
  styleUrls: ['./upload-page.component.scss']
})
export class UploadPageComponent implements OnInit {

  @ViewChild('stepper') stepper;

  files: File[] = [];
  filesSent = 0;
  numberOfFiles = 0;
  progress = 0.0;

  UploadMode = UploadMode;  // Needed in template for comparison with Enum values
  uploadMode: UploadMode = UploadMode.SINGLE_SCAN;
  chooseModeFormGroup: FormGroup;
  chooseFilesFormGroup: FormGroup;
  sendingFilesFormGroup: FormGroup;
  uploadCompletedFormGroup: FormGroup;

  constructor(private scanService: ScanService, private formBuilder: FormBuilder) {}

  ngOnInit() {
    this.chooseModeFormGroup = this.formBuilder.group({});
    this.chooseFilesFormGroup = this.formBuilder.group({});
    this.sendingFilesFormGroup = this.formBuilder.group({});
    this.uploadCompletedFormGroup = this.formBuilder.group({});
    this.scanService.acknowledgeObservable().subscribe(() => {
      this.filesSent += 1;
      this.progress = 100.0 * this.filesSent / this.numberOfFiles;
      if (this.filesSent == this.numberOfFiles) {
        this.stepper.next();
      }
    });
  }

  chooseFiles(files: File[]) {
    this.files = files;
  }

  uploadFiles() {
    this.filesSent = 0;
    this.progress = 0.0;
    if (this.uploadMode == UploadMode.SINGLE_SCAN) {
      this.uploadSingleScan(this.files);
    } else if (this.uploadMode == UploadMode.MULTIPLE_SCANS) {
      this.uploadMultipleScans(this.files);
    } else {
      console.error('Unsupported upload mode!');
    }
  }

  uploadSingleScan(files: File[]) {
    this.numberOfFiles = this.files.length;
    this.scanService.createNewScan().then((scanId: string) => {
      console.log('New Scan created with ID:', scanId);
      this.scanService.uploadSlices(scanId, files);
    });
  }

  uploadMultipleScans(files: File[]) {
    console.warn('Not supported yet!');
    this.numberOfFiles = this.files.length;  // TODO: Change the way we track number of files in multiple scans upload mode!
  }

}
