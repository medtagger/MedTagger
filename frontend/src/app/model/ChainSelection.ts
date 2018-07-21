import {SliceSelection} from './SliceSelection';
import {Point} from './Point';

export class ChainSelection extends SliceSelection {

    private _points: Array<Point>;
    private _isLoop: boolean;

    constructor(points: Array<Point>, depth: number) {
        super();
        this._points = points;
        this.sliceIndex = depth;
        this.label_tag = 'LEFT_KIDNEY'; // TODO: Change these when introducing new marker page
        this.label_tool = 'CHAIN';
    }

    public get points() {
        return this._points;
    }

    public set points(points: Array<Point>) {
        this._points = points;
    }

    get isLoop(): boolean {
        return this._isLoop;
    }

    set isLoop(value: boolean) {
        this._isLoop = value;
    }

    public getCoordinates() {
        return {x: this._points[0].x, y: this._points[0].y, z: this.sliceIndex};
    }

    public toJSON() {
        return {
            'slice_index': this.sliceIndex,
            'points': this._points,
            'loop': this._isLoop,
            'tag': this.label_tag,
            'tool': this.label_tool
        };
    }
}
