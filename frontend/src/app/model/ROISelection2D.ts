import {SelectionData} from './SelectionData';
import {SliceSelection} from './SliceSelection';

export class ROISelection2D implements SliceSelection {
    _positionX: number;
    _positionY: number;
    _width: number;
    _height: number;
    sliceIndex: number;
    label_tool: string;
    label_tag: string;

    constructor(x: number, y: number, depth: number, width?: number, height?: number) {
        this._positionX = x;
        this._positionY = y;
        this._width = width ? width : 0;
        this._height = height ? height : 0;
        this.sliceIndex = depth;
        this.label_tag = 'LEFT_KIDNEY'; // TODO: Change these when introducing new marker page
        this.label_tool = 'RECTANGLE';
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

    public toJSON(): SelectionData {
        // TODO: Avoid using scalar or provide it by some static context
        const scalar = 600;

        let correctPositionX = this._positionX;
        let correctPositionY = this._positionY;
        let correctWidth = this._width;
        let correctHeight = this._height;

        if (this._width < 0) {
            correctPositionX += this._width;
            correctWidth = Math.abs(this._width);
        }
        if (this._height < 0) {
            correctPositionY += this._height;
            correctHeight = Math.abs(this._height);
        }
        return new SelectionData(
            this.sliceIndex,
            this.normalize(correctPositionX, scalar),
            this.normalize(correctPositionY, scalar),
            this.normalize(correctWidth, scalar),
            this.normalize(correctHeight, scalar),
            this.label_tag,
            this.label_tool
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
