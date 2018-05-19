import {Component, EventEmitter, OnInit} from '@angular/core';
import {LabelTag} from "../../model/LabelTag";
import {LabelListItem} from "../../model/LabelListItem";

@Component({
	selector: 'app-label-explorer',
	templateUrl: './label-explorer.component.html',
	styleUrls: ['./label-explorer.component.scss']
})
export class LabelExplorerComponent implements OnInit {

	protected tags: Array<LabelTag> = [];

	protected labels: Array<LabelListItem> = [];

	public labelChange: EventEmitter<LabelListItem> = new EventEmitter<LabelListItem>();

	constructor() {
	}

	ngOnInit() {
	}

	public getLabelChangeEmitter(): EventEmitter<LabelListItem> {
		return this.labelChange;
	}

	public getLabelsLength(): number {
		return this.labels.length;
	}

	public reinitializeExplorer(): void {
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

		label.toDelete = true;
		this.emitLabelChange(label);
	}

	public removeLabel(sliceId: number, tagKey: string, tool: string): void {
		let tag: LabelTag = this.tags.find((item: LabelTag) => item.key == tagKey && item.tools.includes(tool));

		if (tag) {
			let index = this.labels.findIndex(
				(item: LabelListItem) =>
					(item.sliceIndex == sliceId) &&
					(item.tag == tag)
			);
			if (index > -1) {
				this.labels.splice(index, 1);
			} else {
				console.warn(`LabelExplorerComponent | removeLabel: cannot find label for sliceId: ${sliceId} and tag: ${tag}`);
			}
		} else {
			console.warn(`LabelExplorerComponent | removeLabel: cannot find tag for key: ${tagKey} and tool: ${tool}`);
		}
	}

	//TODO: tagKey should be part of dict stored in backend (labelling context)
	//TODO: tools should be part of dict stored in backend (available tools)
	public addLabel(labelSlice: number, tagKey: string, tool: string): void {
		let tag: LabelTag = this.getLabelTag(tagKey, tool);
		let newItem: LabelListItem = new LabelListItem(labelSlice, tag);
		if (!this.labels.find(label => label.sliceIndex == newItem.sliceIndex)) {
			this.labels.push(new LabelListItem(labelSlice, tag));
		}
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

	public hideLabel(label: LabelListItem, newValue: boolean): void {
		label.hidden = newValue;
		this.emitLabelChange(label);
	}

	public pinLabel(label: LabelListItem, newValue: boolean): void {
		label.pinned = newValue;
		this.emitLabelChange(label);
	}

	private emitLabelChange(label: LabelListItem): void {
		this.labelChange.emit(label);
	}
}
