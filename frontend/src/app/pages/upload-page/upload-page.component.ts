import { Component, OnInit, ViewChild } from '@angular/core';
import { MatHorizontalStepper, MatStep } from '@angular/material';
import { FormBuilder, FormGroup, FormControl, Validators } from '@angular/forms';

import { ScanService } from '../../services/scan.service';


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

  @ViewChild('stepper') stepper: MatHorizontalStepper;
  @ViewChild('chooseModeStep') chooseModeStep: MatStep;
  @ViewChild('chooseFilesStep') chooseFilesStep: MatStep;
  @ViewChild('sendingFilesStep') sendingFilesStep: MatStep;
  @ViewChild('uploadCompletedStep') uploadCompletedStep: MatStep;

  files: File[] = [];
  filesSent = 0;
  numberOfFiles = 0;
  progress = 0.0;

  UploadMode = UploadMode;  // Needed in template for comparison with Enum values
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
    this.scanService.acknowledgeObservable().subscribe(() => {
      this.filesSent += 1;
      this.progress = 100.0 * this.filesSent / this.numberOfFiles;
      if (this.filesSent === this.numberOfFiles) {
        this.stepper.next();
      }
    });
    this.scanService.getAvailableCategories().then((availableCategories) => {
      this.availableCategories = availableCategories;
    });
  }

  chooseFiles(files: File[]) {
    this.files = files;
  }

  uploadFiles() {
    this.filesSent = 0;
    this.progress = 0.0;
    if (this.uploadMode === UploadMode.SINGLE_SCAN) {
      this.uploadSingleScan(this.files);
    } else if (this.uploadMode === UploadMode.MULTIPLE_SCANS) {
      this.uploadMultipleScans(this.files);
    } else {
      console.error('Unsupported upload mode!');
    }
  }

  uploadSingleScan(files: File[]) {
    let category = this.chooseCategoryFormGroup.get('category').value;
    this.numberOfFiles = this.files.length;
    this.scanService.createNewScan(category, this.numberOfFiles).then((scanId: string) => {
      console.log('New Scan created with ID:', scanId);
      this.scanService.uploadSlices(scanId, files);
    });
  }

  uploadMultipleScans(files: File[]) {
    console.warn('Not supported yet!');
    this.numberOfFiles = this.files.length;  // TODO: Change the way we track number of files in multiple scans upload mode!
  }

  restart() {
    this.stepper.selectedIndex = 0;
    this.chooseModeStep.completed = false;
    this.chooseFilesStep.completed = false;
    this.sendingFilesStep.completed = false;
    this.uploadCompletedStep.completed = false;
  }

}
