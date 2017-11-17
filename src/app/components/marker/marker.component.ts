import {Component, ElementRef, OnInit, ViewChild, HostListener} from '@angular/core';
import {MarkerSlice} from '../../model/MarkerSlice';
import {MatSlider} from '@angular/material/slider';
import {Subject} from 'rxjs/Subject';
import {ScanViewerComponent} from '../scan-viewer/scan-viewer.component';
import {SliceSelection} from '../SliceSelection';

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

  public removeCurrentSelection(): void {
    this.selector.removeCurrentSelection();
    this.updateSelectionState();
  }

  private updateSelectionState(): void {
    this.hasArchivedSelections = this.selector.hasArchivedSelections();
    this.has2dSelection = this.selector.hasSliceSelection();
    this.has3dSelection = this.selector.hasFullSelection();
  }

  public get3dSelection(): SliceSelection[] {
    this.selector.addCurrentSelection();
    this.selector.archiveSelections();
    this.updateSelectionState();

    this.selector.clearCanvasSelection();

    const coordinates: SliceSelection[] = this.selector.getSelections();
    this.selector.clearSelections();
    this.updateSelectionState();

    this.selector.drawPreviousSelections();

    return coordinates;
  }

  ngOnInit() {
    console.log('Marker init');
    console.log('View elements: image ', this.currentImage, ', canvas ', this.canvas, ', slider ', this.slider);

    this.slices = new Map<number, MarkerSlice>();

    this.selector.clearData();

    this.initializeCanvas();

    this.currentImage.onload = () => {
      this.initCanvasSelectionTool();
    };

    this.setCanvasImage();

    this.slider.registerOnChange((sliderValue: number) => {
      console.log('Marker init | slider change: ', sliderValue);

      this.requestSlicesIfNeeded(sliderValue);

      this.changeMarkerImage(sliderValue);
      this.selector.drawPreviousSelections();

      this.updateSelectionState();
    });
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
