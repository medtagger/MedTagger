import {Component, ElementRef, OnInit, ViewChild, HostListener} from '@angular/core';
import {MarkerSlice} from '../../model/MarkerSlice';
import {MatSlider} from '@angular/material/slider';
import {ROISelection2D} from '../../model/ROISelection2D';
import {ScanMetadata} from '../../model/ScanMetadata';
import {ROISelection3D} from '../../model/ROISelection3D';
import {Subject} from 'rxjs/Subject';
import {MatSliderChange} from '@angular/material/slider';
import {ScanViewerComponent} from '../scan-viewer/scan-viewer.component';

@Component({
  selector: 'app-marker-component',
  templateUrl: './marker.component.html',
  styleUrls: ['./marker.component.scss']
})
export class MarkerComponent extends ScanViewerComponent implements OnInit {

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

  private mouseDrag = false;

  public has3dSelection: boolean;
  public has2dSelection: boolean;
  public hasArchivedSelections: boolean;

  public observableSliceRequest: Subject<number>;

  constructor() {
    super();
  }

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

      this.drawSelection(this.selectedArea, this.STYLE.CURRENT_SELECTION_COLOR);
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
