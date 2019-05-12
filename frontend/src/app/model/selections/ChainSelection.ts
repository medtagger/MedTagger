import { SliceSelection, SliceSelectionType } from './SliceSelection';
import {Point} from '../Point';
import {LabelTag} from '../labels/LabelTag';

export class ChainSelection extends SliceSelection {

    points: Array<Point>;
    loop = false;

    constructor(points: Array<Point>, loop: boolean, depth: number, tag: LabelTag, type: SliceSelectionType) {
        super(depth, 'CHAIN', tag, type);
        this.points = points;
        this.loop = loop;
    }

    public getCoordinates() {
        return {x: this.points[0].x, y: this.points[0].y, z: this.sliceIndex};
    }

    public toJSON() {
        return {
            'slice_index': this.sliceIndex,
            'points': this.points,
            'loop': this.loop,
            'tag': this.labelTag.key,
            'tool': this.labelTool
        };
    }
}
