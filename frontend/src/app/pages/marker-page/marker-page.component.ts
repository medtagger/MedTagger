import {Component, OnInit, ViewChild} from '@angular/core';
import {ActivatedRoute} from '@angular/router';

import {ScanService} from '../../services/scan.service';
import {MarkerComponent} from '../../components/marker/marker.component';
import {ScanMetadata} from '../../model/ScanMetadata';
import {MarkerSlice} from '../../model/MarkerSlice';
import {ROISelection3D} from '../../model/ROISelection3D';
import {RectROISelector} from '../../components/selectors/RectROISelector';
import {ROISelection2D} from '../../model/ROISelection2D';
import {SliceRequest} from '../../model/SliceRequest';
import {DialogService} from '../../services/dialog.service';
import {Location} from '@angular/common';
import {MatSnackBar} from '@angular/material';
import {LabelTag} from '../../model/LabelTag';
import {LabelExplorerComponent} from '../../components/label-explorer/label-explorer.component';


@Component({
    selector: 'app-marker-page',
    templateUrl: './marker-page.component.html',
    providers: [ScanService],
    styleUrls: ['./marker-page.component.scss']
})
export class MarkerPageComponent implements OnInit {

    private static readonly SLICE_BATCH_SIZE = 10;

    @ViewChild(MarkerComponent) marker: MarkerComponent;

    @ViewChild(LabelExplorerComponent) labelExplorer: LabelExplorerComponent;

    // TODO: get labelling context from categry
    tags: Array<LabelTag> = [
        new LabelTag('All', 'ALL', ['RECTANGLE'])
    ];

    scan: ScanMetadata;
    category: string;
    lastSliceID = 0;
    startTime: Date;

    constructor(private scanService: ScanService, private route: ActivatedRoute, private dialogService: DialogService,
                private location: Location, private snackBar: MatSnackBar) {
        console.log('MarkerPage constructor', this.marker);
    }

    ngOnInit() {
        console.log('MarkerPage init', this.marker);

        this.marker.setSelector(new RectROISelector(this.marker.getCanvas()));
        this.marker.setLabelExplorer(this.labelExplorer);

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
            if (this.marker.downloadingScanInProgress === true) {
                this.indicateNewScanAppeared();
            }
            if (slice.isLastInBatch()) {
                this.marker.setDownloadSlicesInProgress(false);
            }
            this.marker.setDownloadScanInProgress(false);
        });

        this.marker.hookUpSliceObserver(MarkerPageComponent.SLICE_BATCH_SIZE).then((isObserverHooked: boolean) => {
            if (isObserverHooked) {
                this.marker.observableSliceRequest.subscribe((request: SliceRequest) => {
                    let sliceRequest = request.slice;
                    let reversed = request.reversed;
                    console.log('MarkerPage | observable sliceRequest: ', sliceRequest, ' reversed: ', reversed);
                    let count = MarkerPageComponent.SLICE_BATCH_SIZE;
                    if (reversed === false && sliceRequest + count > this.scan.numberOfSlices) {
                        count = this.scan.numberOfSlices - sliceRequest;
                    }
                    if (reversed === true) {
                        sliceRequest -= count;
                        if (sliceRequest < 0) {
                            count += sliceRequest;
                            sliceRequest = 0;
                        }
                    }
                    if (count <= 0) {
                        return;
                    }
                    if (this.marker.downloadingSlicesInProgress === false) {
                        this.scanService.requestSlices(this.scan.scanId, sliceRequest, count, reversed);
                        this.marker.setDownloadSlicesInProgress(true);
                    }
                });
            }
        });
    }

    private requestScan(): void {
        this.marker.setDownloadScanInProgress(true);
        this.scanService.getRandomScan(this.category).then(
            (scan: ScanMetadata) => {
                this.scan = scan;
                this.marker.setScanMetadata(this.scan);

                const begin = Math.floor(Math.random() * (scan.numberOfSlices - MarkerPageComponent.SLICE_BATCH_SIZE));
                const count = MarkerPageComponent.SLICE_BATCH_SIZE;
                this.startMeasuringLabelingTime();
                this.scanService.requestSlices(scan.scanId, begin, count, false);
            },
            (errorResponse: Error) => {
                console.log(errorResponse);
                this.marker.setDownloadScanInProgress(false);
                this.marker.setDownloadSlicesInProgress(false);
                this.dialogService
                    .openInfoDialog('Nothing to do here!', 'No more Scans available for you in this category!', 'Go back')
                    .afterClosed()
                    .subscribe(() => {
                        this.location.back();
                    });
            });
    }

    public skipScan(): void {
        this.marker.setDownloadScanInProgress(true);
        this.marker.prepareForNewScan();
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
                console.log('MarkerPage | sendSelection | success!');
                this.indicateLabelHasBeenSend();
                this.labelExplorer.reinitializeExplorer();
                this.skipScan();
                this.startMeasuringLabelingTime();
            })
            .catch((errorResponse: Error) => {
                this.dialogService.openInfoDialog('Error', 'Cannot send selection', 'Ok');
            });
    }

    public remove2dSelection(): void {
        this.marker.removeCurrentSelection();
    }

    private startMeasuringLabelingTime(): void {
        this.startTime = new Date();
    }

    private getLabelingTimeInSeconds(startTime: Date): number {
        const endTime = new Date();
        return (endTime.getTime() - startTime.getTime()) / 1000.0;
    }

    private indicateLabelHasBeenSend(): void {
        this.snackBar.open('Label has been sent!', '', {duration: 2000});
    }

    private indicateNewScanAppeared(): void {
        this.snackBar.open('New scan has been loaded!', '', {duration: 2000});
    }
}
