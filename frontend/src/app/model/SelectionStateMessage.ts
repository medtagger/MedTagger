// Simple message format for label-explorer <-> marker <-> tool communication
import {LabelTag} from './labels/LabelTag';

export class SelectionStateMessage {
    toolName: string;
    labelTag: LabelTag;
    selectionId: number;
    sliceId: number;
    toDelete: boolean;

    constructor(toolName: string, labelTag: LabelTag, selectionId: number, sliceId: number, toDelete?: boolean) {
        this.toolName = toolName;
        this.labelTag = labelTag;
        this.selectionId = selectionId;
        this.sliceId = sliceId;
        this.toDelete = toDelete;
    }
}
