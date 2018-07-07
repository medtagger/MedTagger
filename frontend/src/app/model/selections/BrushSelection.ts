import {SliceSelection} from './SliceSelection';

export class BrushSelection extends SliceSelection {
    _selectionLayer: string;

    constructor(selectionLayer: string, depth: number) {
        super();
        this._selectionLayer = selectionLayer;
        this.sliceIndex = depth;
    }

    toJSON(): Object {
        return {
            'width': 1,
            'height': 1,
            'image_key': this._selectionLayer,
            'slice_index': this.sliceIndex,
            'tag': this.label_tag,
            'tool': this.label_tool
        };
    }
}
