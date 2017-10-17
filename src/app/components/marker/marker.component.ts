///<reference path="../../../../node_modules/@angular/core/src/metadata/directives.d.ts"/>
import {Component, ElementRef, forwardRef, Input, OnInit, ViewChild} from '@angular/core';
import {Slice} from '../../model/Slice';
import {MockService} from '../../services/mock.service';
import {MatSlider} from '@angular/material/slider';

@Component({
  selector: 'app-marker-component',
  templateUrl: './marker.component.html',
  styleUrls: ['./marker.component.scss']
})
export class MarkerComponent implements OnInit {
  testImage: HTMLImageElement;
  @ViewChild('image')
  set viewImage(viewElement: ElementRef) {
    this.testImage = viewElement.nativeElement;
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
  public currentImage = 0;

  private selectedArea: { positionX: number, positionY: number, width: number, height: number };
  private mouseDrag = false;

  constructor(private mockService: MockService) {
    mockService.getMockSlicesURI().forEach((value: string, index: number) => {
      this.slices.push(new Slice(index, value));
    });
  }

  ngOnInit() {
    console.log('Marker init');

    // this.canvas = <HTMLCanvasElement>document.getElementById('markerCanvas');
    console.log('View elements: image ', this.testImage, ', canvas ', this.canvas, ', slider ', this.slider);
    this.canvasCtx = this.canvas.getContext('2d');
    this.canvasCtx.strokeStyle = '#ff0000';

    this.canvasPosition = this.canvas.getBoundingClientRect();

    this.selectedArea = {positionX: 0, positionY: 0, width: 0, height: 0};

    this.testImage.onload = (ev: Event) => {
      this.initCanvasSelectionTool();
    };

    this.setBackgroundImage();

    this.slider.registerOnChange( (value: number) => {
      console.log('Marker init | slider change: ', value);
      this.currentImage = value;
      this.setBackgroundImage();
    });
  }

  //TODO: refactor nazw, lepszy pomysł na logike
  private setBackgroundImage(): void {
    this.testImage.src = this.slices[this.currentImage].source;
  }

  private initCanvasSelectionTool(): void {
    const canvasX = this.canvasPosition.left;
    const canvasY = this.canvasPosition.top;
    console.log('Marker | initCanvasSelectionTool');
    console.log('Marker | initCanvasSelectionTool | canvas offsets: ', canvasX, canvasY);

    this.canvas.onmousedown = (ev: MouseEvent) => {
      console.log('Marker | initCanvasSelectionTool | onmousedown clienXY: ', ev.clientX, ev.clientY);
      this.selectedArea.positionX = (ev.clientX) - canvasX;
      this.selectedArea.positionY = (ev.clientY) - canvasY;
      this.mouseDrag = true;
    };

    this.canvas.onmouseup = (ev: MouseEvent) => {
      this.mouseDrag = false;
      // this.canvasCtx.clearRect(0, 0, this.canvas.width, this.canvas.height);
    };

    this.canvas.onmousemove = (ev: MouseEvent) => {
      if (this.mouseDrag) {
        console.log('Marker | initCanvasSelectionTool | onmousemove clienXY: ', ev.clientX, ev.clientY);
        this.selectedArea.width = (ev.clientX - canvasX) - this.selectedArea.positionX;
        this.selectedArea.height = (ev.clientY - canvasY) - this.selectedArea.positionY;
        this.canvasCtx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        this.canvasCtx.setLineDash([6]);
        this.canvasCtx.strokeRect(this.selectedArea.positionX, this.selectedArea.positionY,
          this.selectedArea.width, this.selectedArea.height);
      }
    };

  }
}
