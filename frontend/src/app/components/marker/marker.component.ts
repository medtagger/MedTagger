import {Component, ElementRef, OnInit, ViewChild} from '@angular/core';
import {MarkerSlice} from '../../model/MarkerSlice';
import {MatSlider} from '@angular/material/slider';
import {Subject} from 'rxjs';
import {ScanViewerComponent} from '../scan-viewer/scan-viewer.component';
import {SliceSelection} from '../../model/SliceSelection';

@Component({
    selector: 'app-marker-component',
    templateUrl: './marker.component.html',
    styleUrls: ['./marker.component.scss']
})
export class MarkerComponent extends ScanViewerComponent implements OnInit {

    currentImage: HTMLImageElement;
    downloadingScanInProgress = false;
    downloadingSlicesInProgress = false;

    @ViewChild('image')
    set viewImage(viewElement: ElementRef) {
        this.currentImage = viewElement.nativeElement;
    }

    canvas: HTMLCanvasElement;

    @ViewChild('canvas')
    set viewCanvas(viewElement: ElementRef) {
        this.canvas = viewElement.nativeElement;
    }

    @ViewChild('slider') slider: MatSlider;

    public selectionState: {isValid: boolean, is2d: boolean, hasArchive: boolean} = { isValid: false, is2d: false, hasArchive: false};

    public observableSliceRequest: Subject<number>;

    constructor() {
        super();
    }

    get currentSlice() {
        return this._currentSlice;
    }

    public setDownloadScanInProgress(isInProgress: boolean) {
        this.downloadingScanInProgress = isInProgress;
    }

    public setDownloadSlicesInProgress(isInProgress: boolean) {
        this.downloadingSlicesInProgress = isInProgress;
    }

    public removeCurrentSelection(): void {
        this.selector.removeCurrentSelection();
        this.updateSelectionState();
    }

    private updateSelectionState(): void {
        this.selectionState.hasArchive = this.selector.hasArchivedSelections();
        this.selectionState.is2d = this.selector.hasSliceSelection();
        this.selectionState.isValid = this.selector.hasValidSelection();
    }

    public get3dSelection(): SliceSelection[] {
        this.selector.archiveSelections();
        this.updateSelectionState();

        this.selector.clearCanvasSelection();

        const coordinates: SliceSelection[] = this.selector.getSelections();
        this.selector.clearSelections();
        this.updateSelectionState();

        this.selector.drawPreviousSelections();

        return coordinates;
    }

    private hookUpStateChangeSubscription(): void {
        this.selector.getStateChangeEmitter().subscribe(() => {
            console.log('Marker | getStateChange event from selector!');
            this.updateSelectionState();
        });
    }

    public prepareForNewScan(): void {
        this.clearData();
        this.hookUpStateChangeSubscription();
    }

    ngOnInit() {
        console.log('Marker init');
        console.log('View elements: image ', this.currentImage, ', canvas ', this.canvas, ', slider ', this.slider);

        this.slices = new Map<number, MarkerSlice>();

        this.selector.clearData();

        this.hookUpStateChangeSubscription();

        this.initializeCanvas();

        this.setCanvasImage();

        this.slider.registerOnChange((sliderValue: number) => {
            console.log('Marker init | slider change: ', sliderValue);

            this.requestSlicesIfNeeded(sliderValue);
            this.changeMarkerImage(sliderValue);

            this.selector.clearCanvasSelection();

            this.selector.drawPreviousSelections();
            this.updateSelectionState();
        });

        this.initCanvasSelectionTool();

    }

    private initCanvasSelectionTool(): void {
        console.log('Marker | initCanvasSelectionTool');

        this.canvas.onmousedown = (mouseEvent: MouseEvent) => {
            console.log('Marker | initCanvasSelectionTool | onmousedown clientXY: ', mouseEvent.clientX, mouseEvent.clientY);
            this.selector.onMouseDown(mouseEvent);
        };

        this.canvas.onmouseup = (mouseEvent: MouseEvent) => {
            this.selector.onMouseUp(mouseEvent);
        };

        this.canvas.onmousemove = (mouseEvent: MouseEvent) => {
            this.selector.onMouseMove(mouseEvent);
        };
    }
}
