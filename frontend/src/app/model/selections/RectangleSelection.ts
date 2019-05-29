import { SliceSelection, SliceSelectionType } from './SliceSelection';
import { LabelTag } from '../labels/LabelTag';

export class RectangleSelection extends SliceSelection {

    // Normalized parameters of selection (<0;1>)
    x: number;
    y: number;
    width: number;
    height: number;

    constructor(x: number, y: number, depth: number, tag: LabelTag, type: SliceSelectionType, width?: number, height?: number) {
        super(depth, 'RECTANGLE', tag, type);
        this.x = x;
        this.y = y;
        this.width = width ? width : 0;
        this.height = height ? height : 0;
    }

    public toJSON() {
        let correctPositionX = this.x;
        let correctPositionY = this.y;
        let correctWidth = this.width;
        let correctHeight = this.height;

        if (this.width < 0) {
            correctPositionX += this.width;
            correctWidth = Math.abs(this.width);
        }
        if (this.height < 0) {
            correctPositionY += this.height;
            correctHeight = Math.abs(this.height);
        }
        return {
            'slice_index': this.sliceIndex,
            'x': correctPositionX,
            'y': correctPositionY,
            'width': correctWidth,
            'height': correctHeight,
            'tag': this.labelTag.key,
            'tool': this.labelTool
        };
    }
}
