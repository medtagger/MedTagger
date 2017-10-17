import { Component, OnInit } from '@angular/core';

import {Scan, ScanService, Slice} from '../../services/scan.service'


@Component({
  selector: 'app-marker-page',
  templateUrl: './marker-page.component.html',
  providers: [ScanService],
  styleUrls: ['./marker-page.component.scss']
})
export class MarkerPageComponent implements OnInit {
  scan: Scan;
  slices: Slice[] = [];
  example_slice_as_b64: string;

  constructor(private scanService: ScanService) {
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

  requestExampleScanButton() {
    this.scanService.getRandomScan().then((scan: Scan) => {
      this.scan = scan;

      let begin = 0;
      let count = 1;
      this.scanService.requestSlices(scan.scanId, begin, count);
    });
  }

}
