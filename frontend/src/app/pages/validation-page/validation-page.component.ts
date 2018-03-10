import {Component, OnInit, ViewChild} from '@angular/core';
import {LabelService} from '../../services/label.service';
import {Label} from '../../model/Label';
import {ScanService} from '../../services/scan.service';
import {MarkerSlice} from '../../model/MarkerSlice';
import {ScanMetadata} from "../../model/ScanMetadata";
import {ScanViewerComponent} from '../../components/scan-viewer/scan-viewer.component';
import {RectROISelector} from '../../components/selectors/RectROISelector';
import {ROISelection2D} from '../../model/ROISelection2D';
import {DialogService} from "../../services/dialog.service";
import {Location} from "@angular/common";


@Component({
    selector: 'app-validation-page',
    templateUrl: './validation-page.component.html',
    providers: [LabelService, ScanService],
    styleUrls: ['./validation-page.component.scss']
})
export class ValidationPageComponent implements OnInit {

    private static readonly SLICE_BATCH_SIZE = 10;
    @ViewChild(ScanViewerComponent) scanViewer: ScanViewerComponent;
    label: Label;
    scan: ScanMetadata;


    constructor(private labelService: LabelService, private scanService: ScanService,
                private dialogService: DialogService, private location: Location) {
    }

    ngOnInit() {
        console.log('ValidationPage init', this.scanViewer);

        this.scanViewer.setSelector(new RectROISelector(this.scanViewer.getCanvas()));

        this.requestSlicesWithLabel();
        this.scanService.slicesObservable().subscribe((slice: MarkerSlice) => {
            this.scanViewer.feedData(slice);

            this.scanViewer.hookUpSliceObserver(ValidationPageComponent.SLICE_BATCH_SIZE).then((isObserverHooked: boolean) => {
                if (isObserverHooked) {
                    this.scanViewer.observableSliceRequest.subscribe((sliceRequest: number) => {
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

    private rect2DROIConverter(selections: any): Array<ROISelection2D> {
        const roiSelections: Array<ROISelection2D> = [];
        selections.forEach((selection: any) => {
            roiSelections.push(new ROISelection2D(selection.x, selection.y, selection.slice_index, selection.width, selection.height));
        });
        return roiSelections;
    }

    private requestSlicesWithLabel(): void {
        this.labelService.getRandomLabel(this.rect2DROIConverter).then((label: Label) => {
            this.label = label;
            this.scanViewer.setArchivedSelections(this.label.labelSelections);

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
        }).catch((error: Error) => {
            this.dialogService
                .openInfoDialog("Error", "Cannot find any selections to validate", "Go back")
                .afterClosed()
                .subscribe(() => {
                    this.location.back();
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
        this.scanViewer.clearData();
        this.requestSlicesWithLabel();
    }
}
