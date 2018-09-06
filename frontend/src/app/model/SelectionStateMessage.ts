// Simple message format for label-explorer <-> marker <-> selector communication
import {LabelTag} from './labels/LabelTag';

export class SelectionStateMessage {
    selectorName: string;
    labelTag: LabelTag;
    selectionId: number;
    sliceId: number;
    toDelete: boolean;

    constructor(selectorName: string, labelTag: LabelTag, selectionId: number, sliceId: number, toDelete?: boolean) {
        this.selectorName = selectorName;
        this.labelTag = labelTag;
        this.selectionId = selectionId;
        this.sliceId = sliceId;
        this.toDelete = toDelete;
    }
}
