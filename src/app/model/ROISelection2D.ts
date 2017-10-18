export class ROISelection2D {
  _positionX: number;
  _positionY: number;
  _width: number;
  _height: number;
  _depth: number;

  constructor(x: number, y: number, depth: number) {
    this._positionX = x;
    this._positionY = y;
    this._width = 0;
    this._height = 0;
    this._depth = depth;
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

  public get depth() {
    return this._depth;
  }

  public get coordinates() {
    return {x: this._positionX, y: this._positionY, z: this._depth};
  }

  public updateWidth(newWidth: number): void {
    this._width = newWidth;
  }

  public updateHeight(newHeight: number): void {
    this._height = newHeight;
  }
}
