import {Component, ElementRef, OnInit, ViewChild} from '@angular/core';

import {ScanService} from '../../services/scan.service';
import {MarkerComponent} from '../../components/marker/marker.component';
import {ScanMetadata} from '../../model/ScanMetadata';
import {MarkerSlice} from '../../model/MarkerSlice';


@Component({
  selector: 'app-marker-page',
  templateUrl: './marker-page.component.html',
  providers: [ScanService],
  styleUrls: ['./marker-page.component.scss']
})
export class MarkerPageComponent implements OnInit {
  @ViewChild(MarkerComponent) marker: MarkerComponent;

  scan: ScanMetadata;

  constructor(private scanService: ScanService) {
    console.log('MarkerPage constructor', this.marker);
  }

  ngOnInit() {
    console.log('MarkerPage init', this.marker);
    this.requestScan();
    this.scanService.slicesObservable().subscribe((slice: MarkerSlice) => {
      console.log('MarkerPage | ngOnInit | slicesObservable: ', slice);
      this.marker.feedData(slice);
    });
  }

  private requestScan(): void {
    this.scanService.getRandomScan().then((scan: ScanMetadata) => {
      this.scan = scan;
      this.marker.setScanMetadata(this.scan);

      const begin = 0;
      const count = 10;
      this.scanService.requestSlices(scan.scanId, begin, count);
    });
  }

  private skipScan(): void {
    this.marker.clearData();
    this.requestScan();
  }

  public sendSelection() {
    return;
  }

  private remove2dSelection(): void {
    this.marker.removeCurrentSelection();
  }

  private formScanSelection() {

  }
}
