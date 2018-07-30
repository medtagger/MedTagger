import {Component, OnInit, ViewChild} from '@angular/core';
import {ActivatedRoute} from '@angular/router';

import {ScanService} from '../../services/scan.service';
import {MarkerComponent} from '../../components/marker/marker.component';
import {ScanCategory, ScanMetadata} from '../../model/ScanMetadata';
import {MarkerSlice} from '../../model/MarkerSlice';
import {Selection3D} from '../../model/selections/Selection3D';
import {RectROISelector} from '../../components/selectors/RectROISelector';
import {SliceRequest} from '../../model/SliceRequest';
import {DialogService} from '../../services/dialog.service';
import {Location} from '@angular/common';
import {MatSnackBar} from '@angular/material';
import {LabelTag} from '../../model/labels/LabelTag';
import {LabelExplorerComponent} from '../../components/label-explorer/label-explorer.component';
import {Selector} from '../../components/selectors/Selector';
import {PointSelector} from '../../components/selectors/PointSelector';
import {SliceSelection} from '../../model/selections/SliceSelection';
import {BrushSelector} from '../../components/selectors/BrushSelector';
import {CategoryService} from '../../services/category.service';
import {FormControl, Validators} from '@angular/forms';
import {isUndefined} from 'util';
import {ChainSelector} from '../../components/selectors/ChainSelector';
import {SelectorAction} from '../../model/SelectorAction';


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

    scan: ScanMetadata;
    category: ScanCategory;
    lastSliceID = 0;
    startTime: Date;
    selectors: Map<string, Selector<any>>;
    categoryTags: FormControl;
    selectorActions: Array<SelectorAction> = [];

    constructor(private scanService: ScanService, private route: ActivatedRoute, private dialogService: DialogService,
                private categoryService: CategoryService, private location: Location, private snackBar: MatSnackBar) {
        console.log('MarkerPage constructor', this.marker);
    }

    ngOnInit() {
        console.log('MarkerPage init', this.marker);

        this.category = this.categoryService.getCurrentCategory();

        if (!this.category) {
            this.dialogService
                .openInfoDialog('You did not choose category properly!', 'Please choose it again!', 'Go back')
                .afterClosed()
                .subscribe(() => {
                    this.location.back();
                });
        } else if (this.category.tags.length === 0) {
            this.dialogService
                .openInfoDialog('There are no tags assigned to this category!', 'Please try another category!', 'Go back')
                .afterClosed()
                .subscribe(() => {
                    this.location.back();
                });
        }

        this.categoryTags = new FormControl('', [Validators.required]);

        this.selectors = new Map<string, Selector<any>>([
            ['RECTANGLE', new RectROISelector(this.marker.getCanvas())],
            ['POINT', new PointSelector(this.marker.getCanvas())],
            ['CHAIN', new ChainSelector(this.marker.getCanvas())],
            ['BRUSH', new BrushSelector(this.marker.getCanvas())]
        ]);

        this.marker.setSelectors(Array.from(this.selectors.values()));

        this.marker.setLabelExplorer(this.labelExplorer);

        this.requestScan();

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
                    const reversed = request.reversed;
                    let sliceRequest = request.slice;
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
        this.scanService.getRandomScan(this.category.key).then(
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
        this.scanService.skipScan(this.scan.scanId).then();
        this.nextScan();
    }

    public nextScan(): void {
        this.marker.setDownloadScanInProgress(true);
        this.marker.prepareForNewScan();
        this.requestScan();
    }

    public sendCompleteLabel(): void {
        this.sendSelection(new Selection3D(<SliceSelection[]>this.marker.get3dSelection()));
    }

    public sendEmptyLabel(): void {
        this.sendSelection(new Selection3D());
        this.nextScan();
    }

    private sendSelection(selection3D: Selection3D) {
        const labelingTime = this.getLabelingTimeInSeconds(this.startTime);

        this.scanService.sendSelection(this.scan.scanId, selection3D, labelingTime)
            .then((response: Response) => {
                console.log('MarkerPage | sendSelection | success!');
                this.indicateLabelHasBeenSend();
                this.labelExplorer.reinitializeExplorer();
                this.nextScan();
                this.startMeasuringLabelingTime();
            })
            .catch((errorResponse: Error) => {
                this.dialogService.openInfoDialog('Error', 'Cannot send selection', 'Ok');
            });
    }

    public remove2dSelection(): void {
        this.marker.removeAllSelectionsOnCurrentSlice();
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

    public isToolSupportedByCurrentTag(tool: string) {
        const tag = this.marker.getCurrentTag();
        if (isUndefined(tag)) {
            return false;
        }
        return tag.tools.includes(tool);
    }

    public setSelector(selectorName: string) {
        const selector = this.selectors.get(selectorName);
        if (selector) {
            this.marker.setCurrentSelector(selector);
            this.selectorActions = selector.getActions();
        } else {
            console.warn(`MarkerPage | setSelector | Selector "${selectorName}" doesn't exist`);
        }
    }

    public setTag(tag: LabelTag) {
        this.marker.setCurrentTag(tag);
    }

    public getToolIconName(iconName: string): string {
        return LabelExplorerComponent.toolIconNames.get(iconName);
    }
}
