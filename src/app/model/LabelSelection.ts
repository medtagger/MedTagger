export class LabelSelection {
  positionX: number;
  positionY: number;
  sliceIndex: number;
  shapeWidth: number;
  shapeHeight: number;


  constructor(positionX: number, positionY: number, sliceIndex: number, shapeWidth: number, shapeHeight: number) {
    this.positionX = positionX;
    this.positionY = positionY;
    this.sliceIndex = sliceIndex;
    this.shapeWidth = shapeWidth;
    this.shapeHeight = shapeHeight;
  }
}
