import { Component, OnInit, ViewChild } from '@angular/core';
import { MatHorizontalStepper, MatStep } from '@angular/material';
import { FormBuilder, FormGroup, FormControl, Validators } from '@angular/forms';
import { Observable } from 'rxjs/Rx';

import { ScanService } from '../../services/scan.service';
import {UploadScansSelectorComponent} from "../../components/upload-scans-selector/upload-scans-selector.component";


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
  @ViewChild('uploadSingleScanSelector') uploadSingleScanSelector: UploadScansSelectorComponent;
  @ViewChild('uploadMultipleScansSelector') uploadMultipleScansSelector: UploadScansSelectorComponent;

  scans: object = {};
  numberOfScans: number = 0;
  totalNumberOfSlices: number = 0;

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
    this.scanService.getAvailableCategories().then((availableCategories) => {
      this.availableCategories = availableCategories;
    });
  }

  chooseFiles($event) {
    this.scans = $event.scans;
    this.numberOfScans = $event.numberOfScans;
    this.totalNumberOfSlices = $event.numberOfSlices;
  }
 
  updateProgressBar() {
    this.slicesSent += 1;
    this.progress = 100.0 * this.slicesSent / this.totalNumberOfSlices;
    if (this.slicesSent === this.totalNumberOfSlices) {
      this.stepper.next();
    }
  }

  uploadFiles() {
    this.slicesSent = 0;
    this.progress = 0.0;
    if (this.uploadMode === UploadMode.SINGLE_SCAN) {
      this.uploadSingleScan(this.scans['singleScan']).subscribe(_ => this.updateProgressBar());
    } else if (this.uploadMode === UploadMode.MULTIPLE_SCANS) {
      this.uploadMultipleScans().subscribe(_ => this.updateProgressBar());
    } else {
      console.error('Unsupported upload mode!');
    }
  }

  uploadSingleScan(slices) {
    let category = this.chooseCategoryFormGroup.get('category').value;
    let numberOfSlices = slices.length;

    return Observable.defer(
        () => this.scanService.createNewScan(category, numberOfSlices)
      )
      .flatMap((scanId: string) => {
        console.log('New Scan created with ID:', scanId, ', number of Slices:', numberOfSlices);
        return this.scanService.uploadSlices(scanId, slices);
      });
  }

  uploadMultipleScans() {
    let CONCURRENT_SCANS_UPLOAD = 1;

    return Observable.from(Object.keys(this.scans))
      .map((scan) => this.uploadSingleScan(this.scans[scan]))
      .mergeAll(CONCURRENT_SCANS_UPLOAD);
  }

  resetFormGroup(formGroup: FormGroup) {
    formGroup.reset();
    formGroup.markAsUntouched();
    Object.keys(formGroup.controls).forEach((name) => {
      let control = formGroup.controls[name];
      control.setErrors(null);
    });
  }

  restart() {
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

    this.scans = {};
    this.numberOfScans = 0;
    this.totalNumberOfSlices = 0;
    this.slicesSent = 0;

    this.chooseModeStep.completed = false;
    this.chooseFilesStep.completed = false;
    this.sendingFilesStep.completed = false;
    this.uploadCompletedStep.completed = false;
    this.stepper.selectedIndex = 0;
  }

  isGoogleChrome() {
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
