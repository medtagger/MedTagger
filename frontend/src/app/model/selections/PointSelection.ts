import {SliceSelection, SliceSelectionType} from './SliceSelection';
import {LabelTag} from '../labels/LabelTag';

export class PointSelection extends SliceSelection {

    // Normalized parameters of selection (<0;1>)
    x: number;
    y: number;

    constructor(x: number, y: number, depth: number, tag: LabelTag, type: SliceSelectionType) {
        super(depth, 'POINT', tag, type);
        this.x = x;
        this.y = y;
    }

    public toJSON() {
        return {
            'slice_index': this.sliceIndex,
            'x': this.x,
            'y': this.y,
            'tag': this.labelTag.key,
            'tool': this.labelTool
        };
    }
}
