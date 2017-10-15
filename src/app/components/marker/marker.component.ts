import {Component, Input, OnInit} from '@angular/core';

@Component({
  selector: 'app-marker-component',
  templateUrl: './marker.component.html',
  // styleUrls: ['./marker.component.scss']
})
export class MarkerComponent implements OnInit {
  private testImage: HTMLImageElement;
  private canvas: HTMLCanvasElement;
  private canvasCtx: CanvasRenderingContext2D;
  private canvasPosition: ClientRect;

  public images: ImageData[] = [];
  public currentImage = 0;

  private selectedArea: { positionX: number, positionY: number, width: number, height: number };
  private mouseDrag = false;

  constructor() {
    this.images.push(new ImageData(10, 10));
    this.images.push(new ImageData(10, 10));
    this.images.push(new ImageData(10, 10));
    this.images.push(new ImageData(10, 10));
  }

  public isMarkerConnected(): boolean {
    return true;
  }

  ngOnInit() {
    console.log('Marker init');

    this.canvas = <HTMLCanvasElement>document.getElementById('markerCanvas');
    this.canvasCtx = this.canvas.getContext('2d');

    this.canvasPosition = this.canvas.getBoundingClientRect();

    this.selectedArea = {positionX: 0, positionY: 0, width: 0, height: 0};

    this.testImage = <HTMLImageElement>document.getElementById('markerBackgroundImage');
    this.testImage.onload = (ev: Event) => {
      this.initCanvasSelectionTool();
    };
    this.testImage.src = '../../assets/img/test_lung1.png';
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
