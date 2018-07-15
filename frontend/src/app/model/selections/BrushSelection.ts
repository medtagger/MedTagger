import {SliceSelection} from './SliceSelection';

export class BrushSelection extends SliceSelection {
    _selectionLayer: HTMLImageElement;
    isReady: Promise<void>;

    constructor(selectionLayer: string, depth: number) {
        super();
        this._selectionLayer = new Image();

        this.isReady = new Promise((resolve, reject) => {
            this._selectionLayer.onload = () => resolve();
            this._selectionLayer.onerror = () => reject();

            this._selectionLayer.src = selectionLayer;
        });


        this.sliceIndex = depth;
    }

    public getSelectionLayer(): Promise<HTMLImageElement | Error> {
        return this.isReady.then( () => {
            return this._selectionLayer;
        }).catch( () => {
            return new Error('Cannot load image (BrushSelection)');
        });
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
