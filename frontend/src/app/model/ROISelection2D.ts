import {SelectionData} from './SelectionData';
import {SliceSelection} from './SliceSelection';

export class ROISelection2D implements SliceSelection {
  _positionX: number;
  _positionY: number;
  _width: number;
  _height: number;
  sliceIndex: number;

  constructor(x: number, y: number, depth: number, width?: number, height?: number) {
    this._positionX = x;
    this._positionY = y;
    this._width = width ? width : 0;
    this._height = height ? height : 0;
    this.sliceIndex = depth;
  }

  public get positionX() {
    return this._positionX;
  }

  public get positionY() {
    return this._positionY;
  }

  public get width() {
    return this._width;
  }

  public get height() {
    return this._height;
  }

  public get coordinates() {
    return {x: this._positionX, y: this._positionY, z: this.sliceIndex};
  }

  public updateWidth(newWidth: number): void {
    this._width = newWidth;
  }

  public updateHeight(newHeight: number): void {
    this._height = newHeight;
  }

  public toJSON(scalar: number): SelectionData {
    return new SelectionData(
      this.sliceIndex,
      this.normalize(this._positionX, scalar),
      this.normalize(this._positionY, scalar),
      this.normalize(this._width, scalar),
      this.normalize(this._height, scalar)
    );
  }

  private normalize(arg: number, scalar: number): number {
    return arg / scalar;
  }

  public scaleToView(scalar: number): void {
    this._positionX = this.scale(this._positionX, scalar);
    this._positionY = this.scale(this._positionY, scalar);
    this._width = this.scale(this._width, scalar);
    this._height = this.scale(this._height, scalar);
  }

  private scale(arg: number, scalar: number): number {
    return arg * scalar;
  }
}
