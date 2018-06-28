import {SliceSelection} from "./SliceSelection";

export class PointSelection extends SliceSelection {

      // Normalized parameters of selection (<0;1>)
    _positionX: number;
    _positionY: number;

    constructor(x: number, y: number, depth: number) {
        super();
        this._positionX = x;
        this._positionY = y;
        this.sliceIndex = depth;
        this.label_tag = 'LEFT_KIDNEY'; // TODO: Change these when introducing new marker page
        this.label_tool = 'POINT';
    }

    public get positionX() {
        return this._positionX;
    }

    public get positionY() {
        return this._positionY;
    }

    public updatePositionX(x: number) {
        this._positionX = x;
    }

    public updatePositionY(y: number) {
        this._positionY = y;
    }

    public getCoordinates() {
        return {x: this._positionX, y: this._positionY, z: this.sliceIndex};
    }

    public toJSON() {
        return {
            'slice_index': this.sliceIndex,
            'x': this._positionX,
            'y': this._positionY,
            'tag': this.label_tag,
            'tool': this.label_tool
        };
    }
}
