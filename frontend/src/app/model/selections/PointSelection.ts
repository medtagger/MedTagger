import {SliceSelection} from './SliceSelection';
import {LabelTag} from '../labels/LabelTag';

export class PointSelection extends SliceSelection {

      // Normalized parameters of selection (<0;1>)
    _positionX: number;
    _positionY: number;

    constructor(x: number, y: number, depth: number, tag: LabelTag) {
        super();
        this._positionX = x;
        this._positionY = y;
        this.sliceIndex = depth;
        this.label_tag = tag;
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

    public toJSON() {
        return {
            'slice_index': this.sliceIndex,
            'x': this._positionX,
            'y': this._positionY,
            'tag': this.label_tag.key,
            'tool': this.label_tool
        };
    }
}
