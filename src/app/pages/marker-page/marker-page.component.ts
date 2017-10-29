import {Component, ElementRef, OnInit, ViewChild} from '@angular/core';

import {ScanService} from '../../services/scan.service';
import {MarkerComponent} from '../../components/marker/marker.component';
import {ScanMetadata} from '../../model/ScanMetadata';
import {MarkerSlice} from '../../model/MarkerSlice';
import {ROISelection3D} from '../../model/ROISelection3D';
import {Response} from '@angular/http';
import {count} from 'rxjs/operator/count';


@Component({
  selector: 'app-marker-page',
  templateUrl: './marker-page.component.html',
  providers: [ScanService],
  styleUrls: ['./marker-page.component.scss']
})
export class MarkerPageComponent implements OnInit {
  @ViewChild(MarkerComponent) marker: MarkerComponent;

  scan: ScanMetadata;
  lastSliceID = 0;

  constructor(private scanService: ScanService) {
    console.log('MarkerPage constructor', this.marker);
  }

  ngOnInit() {
    console.log('MarkerPage init', this.marker);
    this.requestScan();
    this.scanService.slicesObservable().subscribe((slice: MarkerSlice) => {
      console.log('MarkerPage | ngOnInit | slicesObservable: ', slice);
      if (slice.index > this.lastSliceID) {
        this.lastSliceID = slice.index;
      }
      this.marker.feedData(slice);
    });
  }

  private requestScan(): void {
    this.scanService.getRandomScan().then((scan: ScanMetadata) => {
      this.scan = scan;
      this.marker.setScanMetadata(this.scan);

      //TODO: ogarnięcie randomowego startu

      const begin = Math.floor(Math.random() * scan.numberOfSlices);
      const count = 10;
      this.scanService.requestSlices(scan.scanId, begin, count);
    });
  }

  private skipScan(): void {
    this.marker.clearData();
    this.requestScan();
  }

  public sendSelection() {
    const roiSelection: ROISelection3D = this.marker.get3dSelection();
    this.scanService.send3dSelection(this.scan.scanId, roiSelection).then((response: Response) => {
      if (response.status === 200) {
        console.log('MarkerPage | sendSelection | success!');
      }
    });
    return;
  }

  private remove2dSelection(): void {
    this.marker.removeCurrentSelection();
  }

  public moreSlices(previous?: boolean) {
    if (previous) {
      // this.currentSliceIds.sort()
    }
    this.scanService.requestSlices(this.scan.scanId, this.lastSliceID, 10);
  }

}
