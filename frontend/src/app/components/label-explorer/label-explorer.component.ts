import {Component, OnInit} from '@angular/core';
import {LabelTag} from "../../model/LabelTag";
import {LabelListItem} from "../../model/LabelListItem";

@Component({
	selector: 'app-label-explorer',
	templateUrl: './label-explorer.component.html',
	styleUrls: ['./label-explorer.component.scss']
})
export class LabelExplorerComponent implements OnInit {

	protected tags: Array<LabelTag> = [];

	// new LabelTag("Left Kidney", "LEFT_KIDNEY", ["RECTANGLE"]),
	// new LabelTag("Right Kidney", "RIGHT_KIDNEY", ["RECTANGLE"]),

	protected labels: Array<LabelListItem> = [];

	// new LabelListItem(25, this.tags[0]),
	// new LabelListItem(26, this.tags[0]),
	// new LabelListItem(27, this.tags[0]),
	// new LabelListItem(22, this.tags[1]),

	constructor() {
	}

	ngOnInit() {
		// Mock-up!
		// this.labels[0].visible = false;
		// this.labels[1].pinned = true;
	}

	public getLabelsLength(): number {
		return this.labels.length;
	}

	private reinitializeExplorer(): void {
		this.labels = [];
		this.tags = [];
	}

	public getLabelsForTag(tag: LabelTag): Array<LabelListItem> {
		return this.labels.filter(label => label.tag.key == tag.key);
	}

	public deleteLabel(label: LabelListItem): void {
		let index = this.labels.indexOf(label);
		if (index > -1) {
			this.labels.splice(index, 1);
		}
	}

	//TODO: tagKey should be part of dict stored in backend (labelling context)
	//TODO: tools should be part of dict stored in backend (available tools)
	public addLabel(labelSlice: number, tagKey: string, tool: string): void {
		let tag: LabelTag = this.getLabelTag(tagKey, tool);
		this.labels.push(new LabelListItem(labelSlice, tag));
	}

	private getLabelTag(tagKey: string, tool: string): LabelTag {
		let found: LabelTag = this.tags.find(tag => tag.key == tagKey);
		if (found) {
			return found;
		} else {
			//TODO: get name for tag key, now mocked generic name
			let name = 'All';
			let created = new LabelTag(name, tagKey, [tool]);
			this.tags.push(created);
			return created;
		}
	}
}
