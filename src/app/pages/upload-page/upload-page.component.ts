import { Component, OnInit, ViewChild } from '@angular/core';

import { ScanService, Slice } from '../../services/scan.service'


enum UploadMode {
  SINGLE_SCAN,
  MULTIPLE_SCANS
}


@Component({
  selector: 'app-upload-page',
  templateUrl: './upload-page.component.html',
  providers: [ScanService],
})
export class UploadPageComponent implements OnInit {
  @ViewChild('dicomUpload') dicomUploadForm;
  uploadMode: UploadMode = UploadMode.SINGLE_SCAN;
  UploadMode = UploadMode;

  constructor(private scanService: ScanService) {}

  ngOnInit() {
    console.log('Upload init');
  }

  uploadButton() {
    let fileBrowser = this.dicomUploadForm.nativeElement;
    if (fileBrowser.files && fileBrowser.files.length > 0) {
      this.uploadFiles(fileBrowser.files);
    } else {
      console.warn('No scans selected!');
    }
  }

  uploadFiles(files: ArrayBuffer[]) {
    if (this.uploadMode == UploadMode.SINGLE_SCAN) {
      this.uploadSingleScan(files);
    } else if (this.uploadMode == UploadMode.MULTIPLE_SCANS) {
      this.uploadMultipleScans(files);
    } else {
      console.error('Unsupported upload mode!');
    }
  }

  uploadSingleScan(files: ArrayBuffer[]) {
    this.scanService.createNewScan().then((scanId: string) => {
      console.log('New Scan created with given ID:', scanId);
      for (let slice of files) {
        console.log('Sending...', slice);
        this.scanService.uploadSlice(scanId, slice);
      }
    });
  }

  uploadMultipleScans(files: ArrayBuffer[]) {
    console.warn('Not supported yet!');
  }

}
