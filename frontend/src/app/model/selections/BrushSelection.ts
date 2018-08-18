import {SliceSelection} from './SliceSelection';
import {BinaryConverter} from '../../utils/BinaryConverter';

export class BrushSelection extends SliceSelection {
    _selectionLayer: HTMLImageElement;
    isReady: Promise<void>;

    constructor(selectionLayer: string, depth: number, tag: string) {
        super();
        this._selectionLayer = new Image();

        this.isReady = new Promise((resolve, reject) => {
            this._selectionLayer.onload = () => resolve();
            this._selectionLayer.onerror = () => reject();

            this._selectionLayer.src = selectionLayer;
        });


        this.sliceIndex = depth;
        this.label_tag = tag;
        this.label_tool = 'BRUSH';
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
            'image_key': this.getId().toString(),
            'slice_index': this.sliceIndex,
            'tag': this.label_tag,
            'tool': this.label_tool
        };
    }

    getAdditionalData(): Object {
        const additionalData: Object = {};
        additionalData[this.getId().toString()] = BinaryConverter.base64toBlob(this._selectionLayer.src);
        return additionalData;
    }
}
