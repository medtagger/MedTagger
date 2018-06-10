import {LabelTag} from './LabelTag';

export class LabelListItem {
    tag: LabelTag;
    sliceIndex: number;
    pinned: boolean;
    hidden: boolean;
    toDelete: boolean;

    hovered: boolean;  // TODO: Can I do this in any better way?

    constructor(sliceIndex: number, tag: LabelTag) {
        this.sliceIndex = sliceIndex;
        this.tag = tag;
        this.hidden = false;
        this.pinned = false;
        this.hovered = false;
        this.toDelete = false;
    }
}
