import {Component, OnInit, ViewChild} from '@angular/core';
import {ActivatedRoute} from '@angular/router';

import {ScanService} from '../../services/scan.service';
import {MarkerComponent} from '../../components/marker/marker.component';
import {ScanMetadata} from '../../model/ScanMetadata';
import {MarkerSlice} from '../../model/MarkerSlice';
import {ROISelection3D} from '../../model/ROISelection3D';
import {RectROISelector} from '../../components/selectors/RectROISelector';
import {ROISelection2D} from '../../model/ROISelection2D';
import {DialogService} from '../../services/dialog.service';
import {Location} from '@angular/common';
import {MatSnackBar} from '@angular/material';


class LabelTag {
    name: string;
    key: string;
    tools: Array<string>;
    hidden: boolean;

    constructor(name: string, key: string, tools: Array<string>) {
        this.name = name;
        this.key = key;
        this.tools = tools;
        this.hidden = false;
    }
}


class LabelListItem {
    sliceIndex: number;
    pinned: boolean;
    visible: boolean;
    tag: LabelTag;
    hovered: boolean;  // TODO: Can I do this in any better way?

    constructor(sliceIndex: number, tag: LabelTag) {
        this.sliceIndex = sliceIndex;
        this.tag = tag;
        this.visible = true;
        this.pinned = false;
        this.hovered = false;
    }
}


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
    startTime: Date;

    // Mock-up!
    tags: Array<LabelTag> = [
        new LabelTag("Left Kidney", "LEFT_KIDNEY", ["RECTANGLE"]),
        new LabelTag("Right Kidney", "RIGHT_KIDNEY", ["RECTANGLE"]),
    ];
    labels: Array<LabelListItem> = [
        new LabelListItem(25, this.tags[0]),
        new LabelListItem(26, this.tags[0]),
        new LabelListItem(27, this.tags[0]),
        new LabelListItem(22, this.tags[1]),
    ];

    constructor(private scanService: ScanService, private route: ActivatedRoute, private dialogService: DialogService,
                private location: Location, private snackBar: MatSnackBar) {
        console.log('MarkerPage constructor', this.marker);
    }

    ngOnInit() {
        // Mock-up!
        this.labels[0].visible = false;
        this.labels[1].pinned = true;

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
            if (this.marker.downloadingScanInProgress === true) {
                this.indicateNewScanAppeared();
            }
            this.marker.setDownloadSlicesInProgress(false);
            this.marker.setDownloadScanInProgress(false);
        });

        this.marker.hookUpSliceObserver(MarkerPageComponent.SLICE_BATCH_SIZE).then((isObserverHooked: boolean) => {
            if (isObserverHooked) {
                this.marker.observableSliceRequest.subscribe((sliceRequest: number) => {
                    console.log('MarkerPage | observable sliceRequest: ', sliceRequest);
                    this.marker.setDownloadSlicesInProgress(true);
                    let count = MarkerPageComponent.SLICE_BATCH_SIZE;
                    if (sliceRequest + count > this.scan.numberOfSlices) {
                        count = this.scan.numberOfSlices - sliceRequest;
                        this.marker.setDownloadSlicesInProgress(false);
                    }
                    if (sliceRequest < 0) {
                        count = count + sliceRequest;
                        sliceRequest = 0;
                        this.marker.setDownloadSlicesInProgress(false);
                    }
                    this.scanService.requestSlices(this.scan.scanId, sliceRequest, count);
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
                this.scanService.requestSlices(scan.scanId, begin, count);
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
                if (response.status === 200) {
                    console.log('MarkerPage | sendSelection | success!');
                }
            })
            .catch((errorResponse: Error) => {
                this.dialogService
                    .openInfoDialog('Error', 'Cannot send selection', 'Ok');
            });
        this.startMeasuringLabelingTime();
        this.indicateLabelHasBeenSend();
        return;
    }

    public remove2dSelection(): void {
        this.marker.removeCurrentSelection();
    }

    public getLabelsForTag(tag: LabelTag): Array<LabelListItem> {
        return this.labels.filter(label => label.tag.key == tag.key);
    }

    public deleteLabel(label: LabelListItem): void {
        let index = this.labels.indexOf(label);
        if (index > -1) {
            this.labels.splice(index, 1);
        }
    }

    private startMeasuringLabelingTime(): void {
      this.startTime = new Date();
    }

    private getLabelingTimeInSeconds(startTime: Date): number {
      const endTime = new Date();
      return (endTime.getTime() - startTime.getTime()) / 1000.0;
    }

    private indicateLabelHasBeenSend(): void {
      this.snackBar.open('Label has been send', '', {duration: 2000, });
    }

    private indicateNewScanAppeared(): void {
      this.snackBar.open('New scan has been loaded', '', {duration: 2000, });
    }
}
