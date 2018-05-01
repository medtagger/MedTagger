import {LabelTag} from "./LabelTag";

export class LabelListItem {
	sliceIndex: number;
	pinned: boolean;
	visible: boolean;
	tag: LabelTag;
	hovered: boolean;  // TODO: Can I do this in any better way?

	constructor(sliceIndex: number, tag: LabelTag) {
		this.sliceIndex = sliceIndex;
		this.tag = tag;
		this.visible = true;
		this.pinned = false;
		this.hovered = false;
	}
}