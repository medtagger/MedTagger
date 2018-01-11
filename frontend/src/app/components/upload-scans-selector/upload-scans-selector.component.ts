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
  public scans: object = {};

  prepareScans() {
    if (!this.multipleScans) {
      this.numberOfScans = 1;
      this.numberOfSlices = this._files && this._files.length || 0;
      this.scans = {
        "singleScan": this._files
      };
      return;
    }
    
    if (!this._files || this._files.length == 0) {
      this.numberOfScans = 0;
      this.scans = {};
    }

    this.numberOfScans = 0;
    this.numberOfSlices = 0;
    var lastSliceDirectory: String;
    for (let sliceFile of this._files) {
      if (sliceFile.type != "application/dicom" || !sliceFile.webkitRelativePath.endsWith(".dcm")) {
        continue;
      }
      var currentSlicePath = sliceFile.webkitRelativePath;
      var currentSliceDirectory = currentSlicePath.split("/").slice(0, -1).join("/");
      if (currentSliceDirectory != lastSliceDirectory) {
        lastSliceDirectory = currentSliceDirectory;
        this.scans[currentSliceDirectory] = [];
        this.numberOfScans++;
      }
      this.numberOfSlices++;
      this.scans[currentSliceDirectory].push(sliceFile);
    }
  }

  onNativeInputFileSelect($event) {
    this._files = $event.srcElement.files;
    this.prepareScans();
    this.onFileSelect.emit(this);
  }

  selectFile() {
    this.nativeInputFile.nativeElement.click();
  }
}
