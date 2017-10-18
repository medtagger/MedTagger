import { Component, OnInit } from '@angular/core';

import { ScanService, Slice } from '../../services/scan.service'


@Component({
  selector: 'app-marker-page',
  templateUrl: './marker-page.component.html',
  providers: [ScanService],
})
export class MarkerPageComponent implements OnInit {
  public currentImageNr: number;
  private slices: Slice[] = [];
  scanId: string = 'abc-123';
  example_slice_as_b64: string;

  constructor(private scanService: ScanService) {
    this.currentImageNr = 0;

    scanService.slicesObservable().subscribe(slice => {
      this.slices.push(slice);

      // Just for example purpose - can be removed!
      // TODO: Let's figure out a better way to show images on UI
      let bytes = new Uint8Array(slice.image);
      let binary = '';
      for (let i = 0; i < bytes.byteLength; i++) {
          binary += String.fromCharCode(bytes[i]);
      }
      this.example_slice_as_b64 = 'data:image/png;base64,' + btoa(binary);
    });
  }

  ngOnInit() {
    console.log('MarkerPage init');
  }

  requestExampleSliceButton() {
    this.scanService.requestSlices(this.scanId, 5, 5);
  }

}
