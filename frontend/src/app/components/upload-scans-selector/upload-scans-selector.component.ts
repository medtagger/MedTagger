import {Component, Output, EventEmitter, ViewChild, ElementRef, Input} from '@angular/core';

@Component({
  selector: 'upload-scans-selector',
  templateUrl: './upload-scans-selector.component.html'
})
export class UploadScansSelectorComponent {
  @Input() multipleScans: boolean;
  @Output() onFileSelect: EventEmitter<File[]> = new EventEmitter();

  @ViewChild('inputFile') nativeInputFile: ElementRef;

  private _files: File[];

  get fileCount(): number {
    // TODO: Fix file count for multiple scans!
    return this._files && this._files.length || 0;
  }

  onNativeInputFileSelect($event) {
    this._files = $event.srcElement.files;
    this.onFileSelect.emit(this._files);
  }

  selectFile() {
    this.nativeInputFile.nativeElement.click();
  }
}
