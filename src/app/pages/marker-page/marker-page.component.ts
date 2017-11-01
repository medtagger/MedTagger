import {Component, OnInit, ViewChild} from '@angular/core';
import {ActivatedRoute} from '@angular/router';

import {ScanService} from '../../services/scan.service';
import {MarkerComponent} from '../../components/marker/marker.component';
import {ScanMetadata} from '../../model/ScanMetadata';
import {MarkerSlice} from '../../model/MarkerSlice';
import {ROISelection3D} from '../../model/ROISelection3D';
import {Response} from '@angular/http';


@Component({
  selector: 'app-marker-page',
  templateUrl: './marker-page.component.html',
  providers: [ScanService],
  styleUrls: ['./marker-page.component.scss']
})
export class MarkerPageComponent implements OnInit {

  private static readonly SLICE_BATCH_SIZE = 10;

  @ViewChild(MarkerComponent) marker: MarkerComponent;

  scan: ScanMetadata;
  category: string;
  lastSliceID = 0;

  constructor(private scanService: ScanService, private route: ActivatedRoute) {
    console.log('MarkerPage constructor', this.marker);
  }

  ngOnInit() {
    console.log('MarkerPage init', this.marker);
    this.route.queryParamMap.subscribe(params => {
      this.category = params.get('category') || '';
      this.requestScan();
    });

    this.scanService.slicesObservable().subscribe((slice: MarkerSlice) => {
      console.log('MarkerPage | ngOnInit | slicesObservable: ', slice);
      if (slice.index > this.lastSliceID) {
        this.lastSliceID = slice.index;
      }
      this.marker.feedData(slice);
    });

    this.marker.hookUpSliceObserver(MarkerPageComponent.SLICE_BATCH_SIZE).then((isObserverHooked: boolean) => {
      if (isObserverHooked) {
        this.marker.observableSliceRequest.subscribe((sliceRequest: number) => {
          console.log('MarkerPage | observable sliceRequest: ', sliceRequest);
          let count = MarkerPageComponent.SLICE_BATCH_SIZE;
          if (sliceRequest + count > this.scan.numberOfSlices) {
            count = this.scan.numberOfSlices - sliceRequest;
          }
          if (sliceRequest < 0) {
            count = count + sliceRequest;
            sliceRequest = 0;
          }
          this.scanService.requestSlices(this.scan.scanId, sliceRequest, count);
        });
      }
    });
  }

  private requestScan(): void {
    this.scanService.getRandomScan(this.category).then((scan: ScanMetadata) => {
      this.scan = scan;
      this.marker.setScanMetadata(this.scan);

      const begin = Math.floor(Math.random() * (scan.numberOfSlices - MarkerPageComponent.SLICE_BATCH_SIZE));
      const count = MarkerPageComponent.SLICE_BATCH_SIZE;
      this.scanService.requestSlices(scan.scanId, begin, count);
    });
  }

  public skipScan(): void {
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

  public remove2dSelection(): void {
    this.marker.removeCurrentSelection();
  }
}
