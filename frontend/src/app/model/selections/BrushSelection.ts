import {SliceSelection, SliceSelectionType} from './SliceSelection';
import {BinaryConverter} from '../../utils/BinaryConverter';
import {LabelTag} from '../labels/LabelTag';
import {isUndefined} from 'util';

export class BrushSelection extends SliceSelection {
    selectionLayer: HTMLImageElement;
    isReady: Promise<void>;

    constructor(image: string, depth: number, tag: LabelTag, type: SliceSelectionType) {
        super(depth, 'BRUSH', tag, type);
        this.selectionLayer = new Image();
        this.setImage(image);
    }

    public getSelectionLayer(): Promise<HTMLImageElement | Error> {
        return this.isReady.then( () => {
            return this.selectionLayer;
        }).catch( () => {
            return new Error('Cannot load image (BrushSelection)');
        });
    }

    public setImage(image: string): void {
        this.isReady = new Promise((resolve, reject) => {
            this.selectionLayer.onload = () => resolve();
            this.selectionLayer.onerror = () => reject();

            if (image) {
                this.selectionLayer.src = image;
            }
        });
    }

    toJSON(): Object {
        return {
            'width': 1,
            'height': 1,
            'image_key': this.getId().toString(),
            'slice_index': this.sliceIndex,
            'tag': this.labelTag.key,
            'tool': this.labelTool
        };
    }

    getAdditionalData(): Object {
        const additionalData: Object = {};
        additionalData[this.getId().toString()] = BinaryConverter.base64toBlob(this.selectionLayer.src);
        return additionalData;
    }
}
