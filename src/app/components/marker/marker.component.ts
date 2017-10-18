import {Component, ElementRef, OnInit, ViewChild} from '@angular/core';
import {Slice} from '../../model/Slice';
import {MockService} from '../../services/mock.service';
import {MatSlider} from '@angular/material/slider';
import {ROISelection2D} from '../../model/ROISelection2D';

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

  public slices: Slice[] = [];
  private currentSlice = 0;

  private selectedArea: ROISelection2D;
  private selections: ROISelection2D[] = [];
  private mouseDrag = false;


  constructor(private mockService: MockService) {
    mockService.getMockSlicesURI().forEach((value: string, index: number) => {
      this.slices.push(new Slice(index, value));
    });
  }

  ngOnInit() {
    console.log('Marker init');
    console.log('View elements: image ', this.currentImage, ', canvas ', this.canvas, ', slider ', this.slider);

    this.initializeCanvas();

    this.currentImage.onload = (event: Event) => {
      this.initCanvasSelectionTool();
    };

    this.setCanvasImage();

    this.slider.registerOnChange((sliderValue: number) => {
      console.log('Marker init | slider change: ', sliderValue);
      this.changeMarkerImage(sliderValue);
      this.drawPreviousSelections();
    });
  }

  private initializeCanvas(): void {
    this.canvasCtx = this.canvas.getContext('2d');
    this.canvasPosition = this.canvas.getBoundingClientRect();
  }

  private changeMarkerImage(sliceID: number): void {
    this.currentSlice = sliceID;
    this.selections.push(this.selectedArea);
    this.clearCanvasSelection();
    this.setCanvasImage();
  }

  private clearCanvasSelection(): void {
    this.canvasCtx.clearRect(0, 0, this.canvas.width, this.canvas.height);
    this.drawPreviousSelections();
  }

  private setCanvasImage(): void {
    this.currentImage.src = this.slices[this.currentSlice].source;
  }

  private drawPreviousSelections(): void {
    this.selections.forEach((selection: ROISelection2D) => {
      this.drawSelection(selection, '#0022BB');
    });
  }

  private drawSelection(selection: ROISelection2D, color: string): void {
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
      this.mouseDrag = false;
    };

    this.canvas.onmousemove = (mouseEvent: MouseEvent) => {
      this.drawSelectionRectangle(mouseEvent);
    };
  }

  private startMouseSelection(event: MouseEvent): void {
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
    const newWidth = (event.clientX - this.canvasPosition.left) - this.selectedArea.positionX;
    const newHeight = (event.clientY - this.canvasPosition.top) - this.selectedArea.positionY;

    this.selectedArea.updateWidth(newWidth);
    this.selectedArea.updateHeight(newHeight);
  }
}
