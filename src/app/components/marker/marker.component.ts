import {Component, ElementRef, OnInit, ViewChild, HostListener} from '@angular/core';
import {MarkerSlice} from '../../model/MarkerSlice';
import {MatSlider} from '@angular/material/slider';
import {ROISelection2D} from '../../model/ROISelection2D';
import {ScanMetadata} from '../../model/ScanMetadata';
import {ROISelection3D} from '../../model/ROISelection3D';
import {Subject} from 'rxjs/Subject';
import {MatSliderChange} from '@angular/material/slider';

@Component({
  selector: 'app-marker-component',
  templateUrl: './marker.component.html',
  styleUrls: ['./marker.component.scss']
})
export class MarkerComponent implements OnInit {

  private static readonly STYLE = {
    SELECTION_FONT_SIZE: 14,
    SELECTION_LINE_DENSITY: [6],
    CURRENT_SELECTION_COLOR: '#ff0000',
    OTHER_SELECTION_COLOR: '#256fde',
    ARCHIVED_SELECTION_COLOR: '#5f27e5'
  };

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

  private canvasCtx: CanvasRenderingContext2D;
  private canvasPosition: ClientRect;

  public scanMetadata: ScanMetadata;
  public slices: Map<number, MarkerSlice>;
  private _currentSlice;

  private selectedArea: ROISelection2D;
  private selections: Map<number, ROISelection2D>;
  private mouseDrag = false;

  public has3dSelection: boolean;
  public has2dSelection: boolean;
  public hasArchivedSelections: boolean;

  private archivedSelections: Array<ROISelection2D>;

  public observableSliceRequest: Subject<number>;
  private sliceBatchSize: number;

  constructor() {}

  get currentSlice() {
    return this._currentSlice;
  }

  public clearData(): void {
    this.slices = new Map<number, MarkerSlice>();
    this._currentSlice = undefined;
    this.selectedArea = undefined;
    this.selections = new Map<number, ROISelection2D>();
    this.archivedSelections = [];
    this.clearCanvasSelection();
  }

  public removeCurrentSelection(): void {
    if (this.has2dSelection) {
      this.selections.delete(this._currentSlice);
      this.selectedArea = undefined;
      this.updateSelectionState();

      this.clearCanvasSelection();
    }
  }

  private updateSelectionState(): void {
    this.hasArchivedSelections = this.archivedSelections.length > 0;
    this.has2dSelection = !!this.selections.get(this._currentSlice) || !!this.selectedArea;
    this.has3dSelection = this.selections.size >= 2 || (this.selections.size === 1 && !!this.selectedArea);
  }

  public get3dSelection(): ROISelection3D {
    if (this.selectedArea) {
      this.selections.set(this._currentSlice, this.selectedArea);
      this.selectedArea = undefined;
    }
    this.archiveSelections(this.selections);

    this.clearCanvasSelection();

    const coordinates: ROISelection2D[] = Array.from(this.selections.values());
    this.selections.clear();
    this.updateSelectionState();

    this.drawPreviousSelections();

    return new ROISelection3D(coordinates);
  }

  private archiveSelections(selectionMap: Map<number, ROISelection2D>) {
    selectionMap.forEach((value: ROISelection2D) => {
      this.archivedSelections.push(value);
    });
    this.updateSelectionState();
  }

  public feedData(newSlice: MarkerSlice): void {
    console.log('Marker | feedData: ', newSlice);
    if (!this._currentSlice) {
      this._currentSlice = newSlice.index;
    }
    this.addSlice(newSlice);
    this.updateSliderRange();
  }

  private updateSliderRange(): void {
    const sortedKeys: number[] = Array.from(this.slices.keys()).sort((a: number, b: number) => {
      return a - b;
    });
    console.log('MarkerComponent | updateSliderRange | sortedKeys: ', sortedKeys);

    this.slider.min = sortedKeys[0];
    this.slider.max = sortedKeys[sortedKeys.length - 1];
  }

  private addSlice(newSlice: MarkerSlice) {
    this.slices.set(newSlice.index, newSlice);
    if (this.slices.size === 1) {
      this.setCanvasImage();
    }
  }

  public setScanMetadata(scanMetadata: ScanMetadata): void {
    this.scanMetadata = scanMetadata;
    // this.slider.max = scanMetadata.numberOfSlices;
  }

  public hookUpSliceObserver(sliceBatchSize: number): Promise<boolean> {
    this.sliceBatchSize = sliceBatchSize;
    return new Promise((resolve) => {
      this.observableSliceRequest = new Subject<number>();
      resolve(true);
    });
  }

  ngOnInit() {
    console.log('Marker init');
    console.log('View elements: image ', this.currentImage, ', canvas ', this.canvas, ', slider ', this.slider);

    this.selections = new Map<number, ROISelection2D>();
    this.slices = new Map<number, MarkerSlice>();
    this.archivedSelections = [];

    this.initializeCanvas();

    this.currentImage.onload = () => {
      this.initCanvasSelectionTool();
    };

    this.setCanvasImage();

    this.slider.registerOnChange((sliderValue: number) => {
      console.log('Marker init | slider change: ', sliderValue);

      this.requestSlicesIfNeeded(sliderValue);

      this.changeMarkerImage(sliderValue);
      this.drawPreviousSelections();

      this.updateSelectionState();
    });
  }

  private requestSlicesIfNeeded(sliderValue: number): void {
    console.log('Marker | requestSlicesIfNeeded sliderValue: ', sliderValue);
    let requestSliceIndex;
    if (this.slider.max === sliderValue) {
      requestSliceIndex = sliderValue + 1;
      console.log('Marker | requestSlicesIfNeeded more (higher indexes): ', requestSliceIndex);
      this.observableSliceRequest.next(requestSliceIndex);
    }
    if (this.slider.min === sliderValue) {
      requestSliceIndex = sliderValue - this.sliceBatchSize;
      console.log('Marker | requestSlicesIfNeeded more (lower indexes): ', requestSliceIndex);
      this.observableSliceRequest.next(requestSliceIndex);
    }
  }

  private initializeCanvas(): void {
    this.canvasCtx = this.canvas.getContext('2d');
    this.canvasPosition = this.canvas.getBoundingClientRect();
  }

  @HostListener('window:resize', [])
  private updateCanvasPositionOnWindowResize(): void {
    this.canvasPosition = this.canvas.getBoundingClientRect();
  }

  private changeMarkerImage(sliceID: number): void {
    if (this.selectedArea) {
      this.selections.set(this._currentSlice, this.selectedArea);
      this.selectedArea = undefined;
    }
    this._currentSlice = sliceID;
    this.clearCanvasSelection();
    this.setCanvasImage();
  }

  private clearCanvasSelection(): void {
    this.canvasCtx.clearRect(0, 0, this.canvas.width, this.canvas.height);
    this.drawPreviousSelections();
  }

  private setCanvasImage(): void {
    if (this.slices.has(this._currentSlice)) {
      this.currentImage.src = this.slices.get(this._currentSlice).source;
    }
  }

  private drawPreviousSelections(): void {
    console.log('Marker | drawPreviousSelections | selection: ', this.selections);
    this.selections.forEach((selection: ROISelection2D) => {
      let color: string;
      if (selection.depth === this._currentSlice) {
        color = MarkerComponent.STYLE.CURRENT_SELECTION_COLOR;
      } else {
        color = MarkerComponent.STYLE.OTHER_SELECTION_COLOR;
      }
      this.drawSelection(selection, color);
    });
    console.log('Marker | drawPreviousSelections | archived: ', this.archivedSelections);
    this.archivedSelections.forEach((selection: ROISelection2D) => {
      this.drawSelection(selection, MarkerComponent.STYLE.ARCHIVED_SELECTION_COLOR);
    });
  }

  private drawSelection(selection: ROISelection2D, color: string): void {
    console.log('Marker | drawSelection | selection: ', selection);
    this.canvasCtx.strokeStyle = color;
    this.canvasCtx.setLineDash(MarkerComponent.STYLE.SELECTION_LINE_DENSITY);
    this.canvasCtx.strokeRect(selection.positionX, selection.positionY,
      selection.width, selection.height);

    const fontSize = MarkerComponent.STYLE.SELECTION_FONT_SIZE;
    this.canvasCtx.font = `${fontSize}px Arial`;
    this.canvasCtx.fillStyle = color;
    this.canvasCtx.fillText(selection.depth.toString(), selection.positionX + (fontSize / 4), selection.positionY + fontSize);
  }

  private initCanvasSelectionTool(): void {
    const canvasX = this.canvasPosition.left;
    const canvasY = this.canvasPosition.top;

    console.log('Marker | initCanvasSelectionTool');
    console.log('Marker | initCanvasSelectionTool | canvas offsets: ', canvasX, canvasY);

    this.canvas.onmousedown = (mouseEvent: MouseEvent) => {
      console.log('Marker | initCanvasSelectionTool | onmousedown clientXY: ', mouseEvent.clientX, mouseEvent.clientY);
      this.startMouseSelection(mouseEvent);
    };

    this.canvas.onmouseup = () => {
      if (this.mouseDrag) {
        this.mouseDrag = false;
        this.updateSelectionState();
      }
    };

    this.canvas.onmousemove = (mouseEvent: MouseEvent) => {
      this.drawSelectionRectangle(mouseEvent);
    };
  }

  private startMouseSelection(event: MouseEvent): void {
    console.log('Marker | startMouseSelection | event: ', event);
    const selectionStartX = (event.clientX) - this.canvasPosition.left;
    const selectionStartY = (event.clientY) - this.canvasPosition.top;
    this.selectedArea = new ROISelection2D(selectionStartX, selectionStartY, this._currentSlice);
    this.selections.delete(this._currentSlice);
    this.mouseDrag = true;
  }

  private drawSelectionRectangle(mouseEvent: MouseEvent): void {
    if (this.mouseDrag) {
      console.log('Marker | drawSelectionRectangle | onmousemove clienXY: ', mouseEvent.clientX, mouseEvent.clientY);
      this.updateSelection(mouseEvent);
      this.clearCanvasSelection();

      this.drawSelection(this.selectedArea, MarkerComponent.STYLE.CURRENT_SELECTION_COLOR);
    }
  }

  private updateSelection(event: MouseEvent): void {
    console.log('Marker | updateSelection | event: ', event);
    const newWidth = (event.clientX - this.canvasPosition.left) - this.selectedArea.positionX;
    const newHeight = (event.clientY - this.canvasPosition.top) - this.selectedArea.positionY;

    this.selectedArea.updateWidth(newWidth);
    this.selectedArea.updateHeight(newHeight);
  }
}
