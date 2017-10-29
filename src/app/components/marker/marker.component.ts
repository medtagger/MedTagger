import {Component, ElementRef, OnInit, ViewChild} from '@angular/core';
import {MarkerSlice} from '../../model/MarkerSlice';
import {MockService} from '../../services/mock.service';
import {MatSlider} from '@angular/material/slider';
import {ROISelection2D} from '../../model/ROISelection2D';
import {ScanMetadata} from '../../model/ScanMetadata';

@Component({
  selector: 'app-marker-component',
  templateUrl: './marker.component.html',
  styleUrls: ['./marker.component.scss']
})
export class MarkerComponent implements OnInit {
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

  private scanMetadata: ScanMetadata;
  public slices: MarkerSlice[] = [];
  private currentSlice = 0;

  private selectedArea: ROISelection2D;
  private selections: Map<number, ROISelection2D>;
  private mouseDrag = false;

  public has3dSelection: boolean;
  public has2dSelection: boolean;


  constructor(private mockService: MockService) {
    // mockService.getMockSlicesURI().forEach((value: string, index: number) => {
    //   this.slices.push(new MarkerSlice(index, value));
    // });
  }

  public clearData(): void {
    this.slices = [];
    this.currentSlice = 0;
    this.selectedArea = undefined;
    this.selections = new Map<number, ROISelection2D>();
  }

  public removeCurrentSelection(): void {
    if (this.has2dSelection) {
      this.selections.delete(this.currentSlice);
      this.selectedArea = undefined;

      this.clearCanvasSelection();
    }
  }

  private updateSelectionState(): void {
    this.has2dSelection = !!this.selections.get(this.currentSlice) || !!this.selectedArea;
    this.has3dSelection = this.selections.size === 2;
  }

  public feedData(newSlice: MarkerSlice): void {
    console.log('Marker | feedData: ', newSlice);
    this.addSlice(newSlice);
  }

  private addSlice(newSlice: MarkerSlice) {
    this.slices.push(newSlice);
    if (this.slices.length === 1) {
      this.setCanvasImage();
    }
  }

  public setScanMetadata(scanMetadata: ScanMetadata): void {
    this.scanMetadata = scanMetadata;
  }

  ngOnInit() {
    console.log('Marker init');
    console.log('View elements: image ', this.currentImage, ', canvas ', this.canvas, ', slider ', this.slider);

    this.initializeCanvas();

    this.currentImage.onload = (event: Event) => {
      this.initCanvasSelectionTool();
    };

    this.setCanvasImage();

    this.selections = new Map<number, ROISelection2D>();

    this.slider.registerOnChange((sliderValue: number) => {
      console.log('Marker init | slider change: ', sliderValue);
      this.changeMarkerImage(sliderValue);
      this.drawPreviousSelections();

      this.updateSelectionState();
    });
  }

  private initializeCanvas(): void {
    this.canvasCtx = this.canvas.getContext('2d');
    this.canvasPosition = this.canvas.getBoundingClientRect();
  }

  private changeMarkerImage(sliceID: number): void {
    if (this.selectedArea) {
      this.selections.set(this.currentSlice, this.selectedArea);
      this.selectedArea = undefined;
    }
    this.currentSlice = sliceID;
    this.clearCanvasSelection();
    this.setCanvasImage();
  }

  private clearCanvasSelection(): void {
    this.canvasCtx.clearRect(0, 0, this.canvas.width, this.canvas.height);
    this.drawPreviousSelections();
  }

  private setCanvasImage(): void {
    if (this.slices[this.currentSlice]) {
      this.currentImage.src = this.slices[this.currentSlice].source;
    }
  }

  private drawPreviousSelections(): void {
    console.log('Marker | drawPreviousSelections | selection: ', this.selections);
    this.selections.forEach((selection: ROISelection2D) => {
      let color: string;
      if (selection.depth === this.currentSlice) {
        color = '#ff0000';
      } else {
        color = '#0022BB';
      }
      this.drawSelection(selection, color);
    });
  }

  private drawSelection(selection: ROISelection2D, color: string): void {
    console.log('Marker | drawSelection | selection: ', selection);
    this.canvasCtx.strokeStyle = color;
    this.canvasCtx.setLineDash([6]);
    this.canvasCtx.strokeRect(selection.positionX, selection.positionY,
      selection.width, selection.height);
  }

  private initCanvasSelectionTool(): void {
    const canvasX = this.canvasPosition.left;
    const canvasY = this.canvasPosition.top;

    console.log('Marker | initCanvasSelectionTool');
    console.log('Marker | initCanvasSelectionTool | canvas offsets: ', canvasX, canvasY);

    this.canvas.onmousedown = (mouseEvent: MouseEvent) => {
      console.log('Marker | initCanvasSelectionTool | onmousedown clienXY: ', mouseEvent.clientX, mouseEvent.clientY);
      this.startMouseSelection(mouseEvent);
    };

    this.canvas.onmouseup = (mouseEvent: MouseEvent) => {
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
    this.selectedArea = new ROISelection2D(selectionStartX, selectionStartY, this.currentSlice);
    this.mouseDrag = true;
  }

  private drawSelectionRectangle(mouseEvent: MouseEvent): void {
    if (this.mouseDrag) {
      console.log('Marker | drawSelectionRectangle | onmousemove clienXY: ', mouseEvent.clientX, mouseEvent.clientY);
      this.updateSelection(mouseEvent);
      this.clearCanvasSelection();

      this.drawSelection(this.selectedArea, '#ff0000');
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
