import {Component, OnInit, ViewChild} from '@angular/core';
import {LabelService} from '../../services/label.service';
import {Label} from '../../model/Label';
import {MarkerComponent} from '../../components/marker/marker.component';
import {ScanService} from '../../services/scan.service';
import {MarkerSlice} from '../../model/MarkerSlice';
import {ScanMetadata} from "../../model/ScanMetadata";


@Component({
  selector: 'app-validation-page',
  templateUrl: './validation-page.component.html',
  providers: [LabelService, ScanService],
  styleUrls: ['./validation-page.component.scss']
})
export class ValidationPageComponent implements OnInit {

  private static readonly SLICE_BATCH_SIZE = 10;
  @ViewChild(MarkerComponent) marker: MarkerComponent;
  label: Label;
  scan: ScanMetadata;


  constructor(private labelService: LabelService, private scanService: ScanService) {
  }

  ngOnInit() {
    console.log('ValidationPage init', this.marker);
    this.requestSlicesWithLabel();
    this.scanService.slicesObservable().subscribe((slice: MarkerSlice) => {
      this.marker.feedData(slice);

      this.marker.hookUpSliceObserver(ValidationPageComponent.SLICE_BATCH_SIZE).then((isObserverHooked: boolean) => {
        if (isObserverHooked) {
          this.marker.observableSliceRequest.subscribe((sliceRequest: number) => {
            console.log('ValidationPage | observable sliceRequest: ', sliceRequest);
            let count = ValidationPageComponent.SLICE_BATCH_SIZE;
            if (sliceRequest + count > this.scan.numberOfSlices) {
              count = this.scan.numberOfSlices - sliceRequest;
            }
            if (sliceRequest < 0) {
              count = count + sliceRequest;
              sliceRequest = 0;
            }
            this.scanService.requestSlices(this.label.scanId, sliceRequest, count);
          });
        }
      });
    });
  }

  private requestSlicesWithLabel(): void {
    this.labelService.getRandomLabel().then((label: Label) => {
      this.label = label;

      this.scanService.getScanForScanId(this.label.scanId).then((scan: ScanMetadata) => {
        this.scan = scan;

        const indexes: number[] = [];
        for (let i = 0; i < label.labelSelections.length; i++) {
          indexes.push(label.labelSelections[i].sliceIndex);
        }
        const begin = indexes[Math.floor((Math.random() * indexes.length))];
        let count = ValidationPageComponent.SLICE_BATCH_SIZE;
        if (begin + ValidationPageComponent.SLICE_BATCH_SIZE > this.scan.numberOfSlices) {
          count = this.scan.numberOfSlices - begin;
        }
        this.scanService.requestSlices(this.label.scanId, begin, count);
      });
    });
  }

  public markAsValid(): void {
    this.labelService.changeStatus(this.label.labelId, 'VALID').then(() => {
      this.skipScan();
    });
  }

  public markAsInvalid(): void {
    this.labelService.changeStatus(this.label.labelId, 'INVALID').then(() => {
      this.skipScan();
    });
  }

  public skipScan(): void {
    this.marker.clearData();
    this.requestSlicesWithLabel();
  }
}
