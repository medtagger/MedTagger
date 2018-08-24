import {SliceSelection} from './SliceSelection';
import {Point} from '../Point';
import {LabelTag} from "../labels/LabelTag";

export class ChainSelection extends SliceSelection {

    points: Array<Point>;
    loop = false;

    constructor(points: Array<Point>, depth: number, tag: LabelTag) {
        super();
        this.points = points;
        this.sliceIndex = depth;
        this.label_tag = tag;
        this.label_tool = 'CHAIN';
    }

    public getCoordinates() {
        return {x: this.points[0].x, y: this.points[0].y, z: this.sliceIndex};
    }

    public toJSON() {
        return {
            'slice_index': this.sliceIndex,
            'points': this.points,
            'loop': this.loop,
            'tag': this.label_tag.key,
            'tool': this.label_tool
        };
    }
}
