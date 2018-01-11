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

  scans: object = {};
  numberOfScans: number = 0;
  numberOfSlices: number = 0;

  slicesSent = 0;
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
      this.slicesSent += 1;
      this.progress = 100.0 * this.slicesSent / this.numberOfSlices;
      if (this.slicesSent === this.numberOfSlices) {
        this.stepper.next();
      }
    });
    this.scanService.getAvailableCategories().then((availableCategories) => {
      this.availableCategories = availableCategories;
    });
  }

  chooseFiles($event) {
    this.scans = $event.scans;
    this.numberOfScans = $event.numberOfScans;
    this.numberOfSlices = $event.numberOfSlices;
  }

  uploadFiles() {
    this.slicesSent = 0;
    this.progress = 0.0;
    if (this.uploadMode === UploadMode.SINGLE_SCAN) {
      this.uploadSingleScan();
    } else if (this.uploadMode === UploadMode.MULTIPLE_SCANS) {
      this.uploadMultipleScans();
    } else {
      console.error('Unsupported upload mode!');
    }
  }

  uploadSingleScan() {
    let category = this.chooseCategoryFormGroup.get('category').value;
    this.scanService.createNewScan(category, this.numberOfSlices).then((scanId: string) => {
      console.log('New Scan created with ID:', scanId);
      var files = this.scans['singleScan'];
      this.scanService.uploadSlices(scanId, files);
    });
  }

  uploadMultipleScans() {
    let category = this.chooseCategoryFormGroup.get('category').value;
    for (var scan in this.scans) {
      this.scanService.createNewScan(category, this.numberOfSlices).then((scanId: string) => {
        console.log('New Scan created with ID:', scanId);
        var files = this.scans[scan];
        this.scanService.uploadSlices(scanId, files);
      });
    }
  }

  restart() {
    this.chooseCategoryFormGroup.reset();
    this.scans = {};
    this.numberOfScans = 0;
    this.numberOfSlices = 0;

    this.stepper.selectedIndex = 0;
    this.chooseModeStep.completed = false;
    this.chooseFilesStep.completed = false;
    this.sendingFilesStep.completed = false;
    this.uploadCompletedStep.completed = false;
  }

}
