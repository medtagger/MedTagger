import {SliceSelection} from './SliceSelection';

export class BrushSelection extends SliceSelection {
    _selectionLayer: HTMLImageElement;

    constructor(selectionLayer: string, depth: number) {
        super();
        this._selectionLayer = new Image();
        this._selectionLayer.src = selectionLayer;
        this.sliceIndex = depth;
    }

    get selectionLayer(): HTMLImageElement {
        return this._selectionLayer;
    }

    toJSON(): Object {
        return {
            'width': 1,
            'height': 1,
            'image_key': this._selectionLayer.src,
            'slice_index': this.sliceIndex,
            'tag': this.label_tag,
            'tool': this.label_tool
        };
    }
}
