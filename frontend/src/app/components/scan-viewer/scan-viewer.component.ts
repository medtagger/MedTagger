import {AfterViewInit, Component, ElementRef, HostListener, OnInit, ViewChild} from '@angular/core';
import {MarkerSlice} from '../../model/MarkerSlice';
import {from, Subject} from 'rxjs';
import {groupBy, toArray} from 'rxjs/operators';
import {ScanMetadata} from '../../model/ScanMetadata';
import {MatSlider} from '@angular/material';
import {Tool} from '../tools/Tool';
import {SliceRequest} from '../../model/SliceRequest';
import {SliceSelection} from '../../model/selections/SliceSelection';
import {LabelTag} from '../../model/labels/LabelTag';

@Component({
    selector: 'app-scan-viewer',
    templateUrl: './scan-viewer.component.html',
    styleUrls: ['./scan-viewer.component.scss']
})
export class ScanViewerComponent implements OnInit, AfterViewInit {

    downloadingScanInProgress = false;
    downloadingSlicesInProgress = false;

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

    imageContainer: HTMLDivElement;

    @ViewChild('imageContainer')
    set viewImageContainer(viewElement: ElementRef) {
        this.imageContainer = viewElement.nativeElement;
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

    protected tools: Array<Tool<SliceSelection>>;
    protected _currentTag;

    public focusable = true;

    protected _scale = 1.0;

    set scale(scale: number) {
        this._scale = scale;
        this.resizeImageToCurrentWorkspace();
        this.updateCanvasSize();
    }

    get scale(): number {
        return this._scale;
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
        SliceSelection.resetIdCounter();
    }

    public sliderFocus() {
        if (this.focusable) {
            // setTimeout() fixes slider focus issues in IE/Firefox
            window.setTimeout(() => {
                this.slider._elementRef.nativeElement.focus();
            }, 10);
        }
    }

    public setFocusable(focusable: boolean) {
        this.focusable = focusable;
        if (!this.focusable) {
            this.slider._elementRef.nativeElement.focus();
        } else {
            this.slider._elementRef.nativeElement.blur();
        }
    }

    public setTools(newTools: Array<Tool<SliceSelection>>) {
        this.clearCanvasSelections();
        this.tools = newTools.slice();
        this.tools.forEach((tool) => {
            tool.updateCanvasPosition(this.canvas.getBoundingClientRect());
            tool.updateCurrentSlice(this._currentSlice);
            tool.updateCanvasWidth(this.canvas.width);
            tool.updateCanvasHeight(this.canvas.height);
            tool.drawSelections();
        });
    }

    public setCurrentTagForTool(tool: Tool<SliceSelection>, tag: LabelTag) {
        console.log('Updating tag for tool: ', tool);
        tool.updateCurrentTag(tag);
    }

    public setCurrentTag(tag: LabelTag) {
        this._currentTag = tag;
    }

    public setArchivedSelections(selections: Array<SliceSelection>): void {
        console.log('ScanViewer | setArchivedSelections: ', selections);
        from(selections).pipe(groupBy((selection) => selection.label_tool)).subscribe(selectionGroup => {
            const tool = this.tools.find((s) => s.getToolName() === selectionGroup.key);
            if (tool !== undefined) {
                selectionGroup.pipe(toArray()).subscribe((s) => tool.archiveSelections(tool.formArchivedSelections(s)));
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
        this.tools.forEach((tool) => tool.updateCanvasWidth(this.canvas.width));
    }

    public setCanvasHeight(newHeight: number): void {
        this.canvas.height = newHeight;
        this.tools.forEach((tool) => tool.updateCanvasHeight(this.canvas.height));
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

    public clearData(): void {
        this.slices = new Map<number, MarkerSlice>();
        this._currentSlice = undefined;
        this.tools.forEach((tool) => tool.clearData());
        SliceSelection.resetIdCounter();
    }

    public feedData(newSlice: MarkerSlice): void {
        console.log('ScanViewer | feedData: ', newSlice);
        if (!this._currentSlice) {
            this._currentSlice = newSlice.index;
            this.tools.forEach((tool) => tool.updateCurrentSlice(this._currentSlice));
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

    public updateCanvasPositionInTools(): void {
        this.tools.forEach((selector) => selector.updateCanvasPosition(this.canvas.getBoundingClientRect()));
    }

    public selectMiddleSlice(): void {
        const slicesCount = this.slider.max - this.slider.min + 1;
        const middleSliceNumber = this.slider.min + Math.floor(slicesCount / 2);
        this.slider.value = middleSliceNumber;
        this.changeMarkerImage(middleSliceNumber);
        this.drawSelections();
    }

    ngOnInit() {
        console.log('ScanViewer | ngOnInit');
        console.log('View elements: image ', this.currentImage, ', canvas ', this.canvas, ', slider ', this.slider);

        this.slices = new Map<number, MarkerSlice>();

        this.updateCanvasPositionInTools();

        this.initializeImage(this.drawSelections);

        this.setCanvasImage();

        this.slider.registerOnChange((sliderValue: number) => {
            console.log('ScanViewer init | slider change: ', sliderValue);

            this.tools.forEach((tool) => tool.updateCurrentSlice(sliderValue));
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
        this.canvas.oncontextmenu = (e) => e.preventDefault();
        this.tools.forEach((tool) => tool.updateCanvasPosition(this.canvas.getBoundingClientRect()));
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
        this.tools.forEach((tool) => tool.updateCurrentSlice(this._currentSlice));

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
        const ratioScalar = minCanvasSize * this.scale / maxImageSize;

        console.log('ScanViewer | resizeImageToCurrentWorkspace | ratioScalar: ', ratioScalar);

        const imageSize = {
            width: this.scanMetadata.width * ratioScalar,
            height: this.scanMetadata.height * ratioScalar
        };

        this.currentImage.style.maxWidth = imageSize.width + 'px';
        this.currentImage.style.maxHeight = imageSize.height + 'px';

        this.currentImage.width = imageSize.width;
        this.currentImage.height = imageSize.height;

        if (imageSize.width < this.canvasWorkspace.clientWidth) {
            const left = ((this.canvasWorkspace.clientWidth / 2) - (this.currentImage.width / 2)) + 'px';
            this.currentImage.style.left = left;
            this.canvas.style.left = left;
        }
        if (imageSize.height < this.canvasWorkspace.clientHeight) {
            const top = ((this.canvasWorkspace.clientHeight / 2) - (this.currentImage.height / 2)) + 'px';
            this.currentImage.style.top = top;
            this.canvas.style.top = top;
        }

        this.updateCanvasPositionInTools();
    }

    protected drawSelections(): void {
        this.tools.forEach((tool) => tool.drawSelections());
    }

    protected clearCanvasSelections(): void {
        this.canvas.getContext('2d').clearRect(0, 0, this.canvas.width, this.canvas.height);
    }

    protected redrawSelections(): void {
        this.clearCanvasSelections();
        this.drawSelections();
    }
}
