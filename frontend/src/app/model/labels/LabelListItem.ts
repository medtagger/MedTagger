import {LabelTag} from './LabelTag';

export class LabelListItem {
    tag: LabelTag;
    selectionId: number;
    sliceIndex: number;
    toolName: string;
    pinned: boolean;
    hidden: boolean;
    toDelete: boolean;

    hovered: boolean;  // TODO: Can I do this in any better way?

    constructor(selectionId: number, sliceIndex: number, tag: LabelTag, toolName: string) {
        this.selectionId = selectionId;
        this.sliceIndex = sliceIndex;
        this.tag = tag;
        this.toolName = toolName;
        this.hidden = false;
        this.pinned = false;
        this.hovered = false;
        this.toDelete = false;
    }
}
