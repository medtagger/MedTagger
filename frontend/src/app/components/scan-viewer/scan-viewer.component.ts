import {Component, HostListener, OnInit, ViewChild, ElementRef, AfterViewInit} from '@angular/core';
import {MarkerSlice} from '../../model/MarkerSlice';
import {Subject, from} from 'rxjs';
import {groupBy, toArray} from 'rxjs/operators';
import {ScanMetadata} from '../../model/ScanMetadata';
import {MatSlider} from '@angular/material';
import {Selector} from '../selectors/Selector';
import {SliceRequest} from '../../model/SliceRequest';
import {SliceSelection} from '../../model/selections/SliceSelection';
import {LabelTag} from '../../model/labels/LabelTag';

@Component({
    selector: 'app-scan-viewer',
    templateUrl: './scan-viewer.component.html',
    styleUrls: ['./scan-viewer.component.scss']
})
export class ScanViewerComponent implements OnInit, AfterViewInit {

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


    canvasWorkspace: HTMLDivElement;

    @ViewChild('canvasWorkspace')
    set viewWorkspace(viewElement: ElementRef) {
        this.canvasWorkspace = viewElement.nativeElement;
    }

    public scanMetadata: ScanMetadata;
    public slices: Map<number, MarkerSlice>;
    protected _currentSlice;

    public observableSliceRequest: Subject<SliceRequest>;
    protected sliceBatchSize: number;

    protected selectors: Array<Selector<SliceSelection>>;
    protected _currentTag;

    constructor() {
    }

    @HostListener('window:resize', ['$event'])
    onResize() {
        this.resizeImageToCurrentWorkspace();
        this.updateCanvasSize();
    }

    protected updateCanvasSize(): void {
        console.log('ScanViewer | updateCanvasSize');
        this.setCanvasWidth(this.currentImage.width);
        this.setCanvasHeight(this.currentImage.height);
        this.drawSelections();
    }

    ngAfterViewInit() {
        console.log('ScanViewer | ngAfterViewInit');
        this.sliderFocus();
    }

    public sliderFocus() {
        this.slider._elementRef.nativeElement.focus();
    }

    public setSelectors(newSelectors: Array<Selector<SliceSelection>>) {
        this.clearCanvasSelections();
        this.selectors = newSelectors.slice();
        this.selectors.forEach((selector) => {
            selector.updateCanvasPosition(this.canvas.getBoundingClientRect());
            selector.updateCurrentSlice(this._currentSlice);
            selector.updateCanvasWidth(this.canvas.width);
            selector.updateCanvasHeight(this.canvas.height);
            selector.drawSelections();
        });
    }

    public setCurrentTagForSelector(selector: Selector<SliceSelection>, tag: LabelTag) {
        selector.updateCurrentTag(tag);
    }

    public setCurrentTag(tag: LabelTag) {
        this._currentTag = tag;
    }

    public setArchivedSelections(selections: Array<SliceSelection>): void {
        console.log('ScanViewer | setArchivedSelections: ', selections);
        from(selections).pipe(groupBy((selection) => selection.label_tool)).subscribe(selectionGroup => {
            const selector = this.selectors.find((s) => s.getSelectorName() === selectionGroup.key);
            if (selector !== undefined) {
                selectionGroup.pipe(toArray()).subscribe((s) => selector.archiveSelections(selector.formArchivedSelections(s)));
            } else {
                console.warn(`ScanViewer | setArchivedSelections | '${selectionGroup.key}' tool doesn't exist`);
            }
        });

    }

    public getCanvas(): HTMLCanvasElement {
        return this.canvas;
    }

    public setCanvasWidth(newWidth: number): void {
        this.canvas.width = newWidth;
        this.selectors.forEach((selector) => selector.updateCanvasWidth(this.canvas.width));
    }

    public setCanvasHeight(newHeight: number): void {
        this.canvas.height = newHeight;
        this.selectors.forEach((selector) => selector.updateCanvasHeight(this.canvas.height));
    }

    get currentSlice() {
        return this._currentSlice;
    }

    public clearData(): void {
        this.slices = new Map<number, MarkerSlice>();
        this._currentSlice = undefined;
        this.selectors.forEach((selector) => selector.clearData());
        SliceSelection.resetIdCounter();
    }

    public feedData(newSlice: MarkerSlice): void {
        console.log('ScanViewer | feedData: ', newSlice);
        if (!this._currentSlice) {
            this._currentSlice = newSlice.index;
            this.selectors.forEach((selector) => selector.updateCurrentSlice(this._currentSlice));
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
            this.observableSliceRequest = new Subject<SliceRequest>();
            resolve(true);
        });
    }

    ngOnInit() {
        console.log('ScanViewer | ngOnInit');
        console.log('View elements: image ', this.currentImage, ', canvas ', this.canvas, ', slider ', this.slider);

        this.slices = new Map<number, MarkerSlice>();

        this.initializeCanvas();

        this.initializeImage(this.drawSelections);

        this.setCanvasImage();

        this.slider.registerOnChange((sliderValue: number) => {
            console.log('ScanViewer init | slider change: ', sliderValue);

            this.selectors.forEach((selector) => selector.updateCurrentSlice(sliderValue));
            this.requestSlicesIfNeeded(sliderValue);

            this.changeMarkerImage(sliderValue);

            this.drawSelections();
        });
    }

    protected requestSlicesIfNeeded(sliderValue: number): void {
        console.log('ScanViewer | requestSlicesIfNeeded sliderValue: ', sliderValue);
        let requestSliceIndex;
        if (this.slider.max === sliderValue) {
            requestSliceIndex = sliderValue + 1;
            console.log('ScanViewer | requestSlicesIfNeeded more (higher indexes): ', requestSliceIndex);
            this.observableSliceRequest.next(new SliceRequest(requestSliceIndex));
        }
        if (this.slider.min === sliderValue) {
            requestSliceIndex = sliderValue - 1;
            console.log('ScanViewer | requestSlicesIfNeeded more (lower indexes): ', requestSliceIndex);
            this.observableSliceRequest.next(new SliceRequest(requestSliceIndex, true));
        }
    }

    protected initializeCanvas(): void {
        this.selectors.forEach((selector) => selector.updateCanvasPosition(this.canvas.getBoundingClientRect()));
    }

    protected initializeImage(afterImageLoad?: () => void): void {
        this.currentImage.onload = (event: Event) => {
            if (afterImageLoad) {
                afterImageLoad();
            }
            this.updateCanvasSize();
        };
    }

    protected changeMarkerImage(sliceID: number): void {
        this._currentSlice = sliceID;
        this.selectors.forEach((selector) => selector.updateCurrentSlice(this._currentSlice));

        this.clearCanvasSelections();
        this.setCanvasImage();
    }

    protected setCanvasImage(): void {
        if (this.slices.has(this._currentSlice)) {
            this.currentImage.src = this.slices.get(this._currentSlice).source;
            this.resizeImageToCurrentWorkspace();
        }
    }

    protected resizeImageToCurrentWorkspace(): void {
        console.log('ScanViewer | resizeImageToCurrentWorkspace | scanMetadata (width, height): ',
            this.scanMetadata.width, this.scanMetadata.height);
        console.log('ScanViewer | resizeImageToCurrentWorkspace | canvasWorkspace (client rect): ',
            this.canvasWorkspace.getClientRects());

        const maxImageSize = Math.max(this.scanMetadata.width, this.scanMetadata.height);
        const minCanvasSize = Math.min(this.canvasWorkspace.clientWidth, this.canvasWorkspace.clientHeight);
        const ratioScalar = (minCanvasSize / maxImageSize);

        console.log('ScanViewer | resizeImageToCurrentWorkspace | ratioScalar: ', ratioScalar);

        this.currentImage.style.maxWidth = (this.scanMetadata.width * ratioScalar) + 'px';
        this.currentImage.style.maxHeight = (this.scanMetadata.height * ratioScalar) + 'px';

        this.currentImage.width = this.scanMetadata.width * ratioScalar;
        this.currentImage.height = this.scanMetadata.height * ratioScalar;

        this.centerImageAndCanvas();
    }

    protected centerImageAndCanvas(): void {
        console.log('ScanViewer | centerImageAndCanvas');
        const centerX = (this.canvasWorkspace.clientWidth / 2) - (this.currentImage.width / 2);
        const centerY = (this.canvasWorkspace.clientHeight / 2) - (this.currentImage.height / 2);

        console.log('ScanViewer | centerImageAndCanvas | centerX - centerY: ', centerX, centerY);

        this.currentImage.style.left = centerX + 'px';
        this.currentImage.style.top = centerY + 'px';

        this.canvas.style.left = centerX + 'px';
        this.canvas.style.top = centerY + 'px';

        this.selectors.forEach((selector) => selector.updateCanvasPosition(this.canvas.getBoundingClientRect()));
    }

    protected drawSelections(): void {
        this.selectors.forEach((selector) => selector.drawSelections());
    }

    protected clearCanvasSelections(): void {
        this.canvas.getContext('2d').clearRect(0, 0, this.canvas.width, this.canvas.height);
    }

    protected redrawSelections(): void {
        console.log('ScanViewer | Redrawing selections (clean and draw)');
        this.clearCanvasSelections();
        this.drawSelections();
    }
}
