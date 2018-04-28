import {Component, HostListener, OnInit, ViewChild, ElementRef} from '@angular/core';
import {MarkerSlice} from '../../model/MarkerSlice';
import {Subject} from 'rxjs';
import {ScanMetadata} from '../../model/ScanMetadata';
import {MatSlider} from '@angular/material';
import {Selector} from '../selectors/Selector';
import {SliceSelection} from '../../model/SliceSelection';

@Component({
    selector: 'app-scan-viewer',
    templateUrl: './scan-viewer.component.html',
    styleUrls: ['./scan-viewer.component.scss']
})
export class ScanViewerComponent implements OnInit {

    currentImage: HTMLImageElement;

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

    public scanMetadata: ScanMetadata;
    public slices: Map<number, MarkerSlice>;
    protected _currentSlice;

    public observableSliceRequest: Subject<number>;
    protected sliceBatchSize: number;

    protected selector: Selector<SliceSelection>;

    constructor() {
    }

	@HostListener('window:resize', ['$event'])
	onResize(event) {
		this.updateCanvasSize();
	}

	protected updateCanvasSize(): void {
		//this.setCanvasWidth(event.target.innerWidth - 300 - 48 - 20);
		//this.setCanvasHeight(event.target.innerHeight - 64);
		this.setCanvasWidth(this.currentImage.width);
		this.setCanvasHeight(this.currentImage.height);
	}

    ngAfterViewInit() {
        console.log('ScanViewer | ngAfterViewInit');
        this.sliderFocus();
    }

    public sliderFocus() {
        this.slider._elementRef.nativeElement.focus();
    }

    public setSelector(newSelector: Selector<SliceSelection>) {
        this.selector = newSelector;
    }

    public setArchivedSelections(selections: Array<SliceSelection>): void {
        console.log('ScanViewer | setArchivedSelections: ', selections);
        const normalizedSelections: Array<SliceSelection> = this.selector.formArchivedSelections(selections);
        this.selector.archiveSelections(normalizedSelections);
    }

    public getCanvas(): HTMLCanvasElement {
        return this.canvas;
    }

    public setCanvasWidth(newWidth: number): void {
        this.canvas.width = newWidth;
        this.selector.updateCanvasWidth(this.canvas.width);
    }

    public setCanvasHeight(newHeight: number): void {
        this.canvas.height = newHeight;
        this.selector.updateCanvasHeight(this.canvas.height);
    }

    get currentSlice() {
        return this._currentSlice;
    }

    public clearData(): void {
        this.slices = new Map<number, MarkerSlice>();
        this._currentSlice = undefined;
        this.selector.clearData();
    }

    public feedData(newSlice: MarkerSlice): void {
        console.log('ScanViewer | feedData: ', newSlice);
        if (!this._currentSlice) {
            this._currentSlice = newSlice.index;
            this.selector.updateCurrentSlice(this._currentSlice);
        }
        this.addSlice(newSlice);
        this.updateSliderRange();
    }

    protected updateSliderRange(): void {
        const sortedKeys: number[] = Array.from(this.slices.keys()).sort((a: number, b: number) => {
            return a - b;
        });
        console.log('ScanViewer | updateSliderRange | sortedKeys: ', sortedKeys);

        this.slider.min = sortedKeys[0];
        this.slider.max = sortedKeys[sortedKeys.length - 1];
    }

    protected addSlice(newSlice: MarkerSlice) {
        this.slices.set(newSlice.index, newSlice);
        if (this.slices.size === 1) {
            this.setCanvasImage();
        }
    }

    public setScanMetadata(scanMetadata: ScanMetadata): void {
        this.scanMetadata = scanMetadata;
    }

    public hookUpSliceObserver(sliceBatchSize: number): Promise<boolean> {
        this.sliceBatchSize = sliceBatchSize;
        return new Promise((resolve) => {
            this.observableSliceRequest = new Subject<number>();
            resolve(true);
        });
    }

    ngAfterViewChecked() {}

    ngOnInit() {
        console.log('ScanViewer | ngOnInit');
        console.log('View elements: image ', this.currentImage, ', canvas ', this.canvas, ', slider ', this.slider);

        this.slices = new Map<number, MarkerSlice>();

        this.initializeCanvas();

        this.initializeImage( ()=> {
			this.selector.drawPreviousSelections();
		});

        this.setCanvasImage();

        this.slider.registerOnChange((sliderValue: number) => {
            console.log('ScanViewer init | slider change: ', sliderValue);

            this.selector.updateCurrentSlice(sliderValue);
            this.requestSlicesIfNeeded(sliderValue);

            this.changeMarkerImage(sliderValue);
        });
    }

    protected requestSlicesIfNeeded(sliderValue: number): void {
        console.log('ScanViewer | requestSlicesIfNeeded sliderValue: ', sliderValue);
        let requestSliceIndex;
        if (this.slider.max === sliderValue) {
            requestSliceIndex = sliderValue + 1;
            console.log('ScanViewer | requestSlicesIfNeeded more (higher indexes): ', requestSliceIndex);
            this.observableSliceRequest.next(requestSliceIndex);
        }
        if (this.slider.min === sliderValue) {
            requestSliceIndex = sliderValue - this.sliceBatchSize;
            console.log('ScanViewer | requestSlicesIfNeeded more (lower indexes): ', requestSliceIndex);
            this.observableSliceRequest.next(requestSliceIndex);
        }
    }

    protected initializeCanvas(): void {
        this.selector.updateCanvasPosition(this.canvas.getBoundingClientRect());
    }

    protected initializeImage( afterImageLoad?:()=> void): void {
		this.currentImage.onload = (event: Event) => {
			this.updateCanvasSize();
			if (afterImageLoad) {
				afterImageLoad();
			}
		};
	}

    @HostListener('window:resize', [])
    protected updateCanvasPositionOnWindowResize(): void {
        this.selector.updateCanvasPosition(this.canvas.getBoundingClientRect());
    }

    protected changeMarkerImage(sliceID: number): void {
        this.selector.addCurrentSelection();

        this._currentSlice = sliceID;
        this.selector.updateCurrentSlice(this._currentSlice);

        this.selector.clearCanvasSelection();
        this.setCanvasImage();
    }

    protected setCanvasImage(): void {
        if (this.slices.has(this._currentSlice)) {
            this.currentImage.src = this.slices.get(this._currentSlice).source;
        }
    }
}
