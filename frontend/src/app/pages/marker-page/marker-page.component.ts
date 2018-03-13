import {Component, OnInit, ViewChild} from '@angular/core';
import {ActivatedRoute} from '@angular/router';

import {ScanService} from '../../services/scan.service';
import {MarkerComponent} from '../../components/marker/marker.component';
import {ScanMetadata} from '../../model/ScanMetadata';
import {MarkerSlice} from '../../model/MarkerSlice';
import {ROISelection3D} from '../../model/ROISelection3D';
import {Response} from '@angular/http';
import {RectROISelector} from '../../components/selectors/RectROISelector';
import {ROISelection2D} from '../../model/ROISelection2D';
import {DialogService} from "../../services/dialog.service";
import {Location} from '@angular/common';


@Component({
    selector: 'app-marker-page',
    templateUrl: './marker-page.component.html',
    providers: [ScanService],
    styleUrls: ['./marker-page.component.scss']
})
export class MarkerPageComponent implements OnInit {

    private static readonly SLICE_BATCH_SIZE = 25;

    @ViewChild(MarkerComponent) marker: MarkerComponent;

    scan: ScanMetadata;
    category: string;
    lastSliceID = 0;
    startTime: Date;

    constructor(private scanService: ScanService, private route: ActivatedRoute, private dialogService: DialogService,
                private location: Location) {
        console.log('MarkerPage constructor', this.marker);
    }

    ngOnInit() {
        console.log('MarkerPage init', this.marker);

        this.marker.setSelector(new RectROISelector(this.marker.getCanvas()));

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

    public updateSelectionState() {

    }

    private requestScan(): void {
        this.scanService.getRandomScan(this.category).then(
            (scan: ScanMetadata) => {
                this.scan = scan;
                this.marker.setScanMetadata(this.scan);

                const begin = Math.floor(Math.random() * (scan.numberOfSlices - MarkerPageComponent.SLICE_BATCH_SIZE));
                const count = MarkerPageComponent.SLICE_BATCH_SIZE;
                this.startMeasuringLabelingTime();
                this.scanService.requestSlices(scan.scanId, begin, count);
            },
            (errorResponse: Error) => {
                console.log(errorResponse);
                this.dialogService
                    .openInfoDialog("Nothing to do here!", "No more Scans available for you in this category!", "Go back")
                    .afterClosed()
                    .subscribe(() => {
                        this.location.back();
                    });
            });
    }

    public skipScan(): void {
        this.marker.clearData();
        this.requestScan();
    }

    public sendCompleteLabel(): void {
        this.sendSelection(new ROISelection3D(<ROISelection2D[]>this.marker.get3dSelection()));
    }

    public sendEmptyLabel(): void {
        this.sendSelection(new ROISelection3D());
        this.skipScan();
    }

    private sendSelection(roiSelection: ROISelection3D) {
        const labelingTime = this.getLabelingTimeInSeconds(this.startTime);

        this.scanService.sendSelection(this.scan.scanId, roiSelection, labelingTime)
            .then((response: Response) => {
                if (response.status === 200) {
                    console.log('MarkerPage | sendSelection | success!');
                }
            })
            .catch((errorResponse: Error) => {
                this.dialogService
                    .openInfoDialog("Error", "Cannot send selection", "Ok");
            });
        this.startMeasuringLabelingTime();
        return;
    }

    public remove2dSelection(): void {
        this.marker.removeCurrentSelection();
    }

    private startMeasuringLabelingTime(): void {
      this.startTime = new Date();
    }

    private getLabelingTimeInSeconds(startTime: Date): number {
      const endTime = new Date();
      return (endTime.getTime() - startTime.getTime())/1000.0;
    }
}
