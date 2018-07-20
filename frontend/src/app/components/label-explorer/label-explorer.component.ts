import { Component, EventEmitter, OnInit } from '@angular/core';
import { LabelTag } from '../../model/LabelTag';
import { LabelListItem } from '../../model/LabelListItem';

@Component({
    selector: 'app-label-explorer',
    templateUrl: './label-explorer.component.html',
    styleUrls: ['./label-explorer.component.scss']
})

export class LabelExplorerComponent implements OnInit {

    static readonly toolIconNames: Map<string, string> = new Map([
        ['RECTANGLE', 'crop'],
        ['BRUSH', 'brush'],
        ['POINT', 'gesture-tap'],
        ['CHAIN', 'vector-polyline'],
        ['ERASER', 'eraser'],
        ['ZOOM_IN', 'magnify-plus-outline'],
        ['ZOOM_OUT', 'magnify-minus-outline']
    ]);

    public tags: Array<LabelTag> = [];
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
        return this.labels.filter(label => label.tag.key === tag.key);
    }

    public deleteLabel(label: LabelListItem): void {
        const index = this.labels.indexOf(label);
        if (index > -1) {
            this.labels.splice(index, 1);
        }

        label.toDelete = true;
        this.emitLabelChange(label);
    }

    public removeLabel(selectionId: number): void {
        const index = this.labels.findIndex((item) => item.selectionId === selectionId);
        if (index !== -1) {
            this.labels.splice(index, 1);
        } else {
            console.warn(`LabelExplorerComponent | removeLabel: cannot find label for selectionId ${selectionId}`);
        }
    }

    // TODO: tools should be part of dict stored in backend (available tools)
    public addLabel(selectionId: number, labelSlice: number, tag: LabelTag, tool: string): void {
        const t: LabelTag = this.getLabelTag(tag.key, tool);
        const newItem: LabelListItem = new LabelListItem(selectionId, labelSlice, t, tool);
        this.labels.push(newItem);
    }

    private getLabelTag(tagKey: string, tool: string): LabelTag {
        const found: LabelTag = this.tags.find(tag => tag.key === tagKey);
        if (found) {
            return found;
        } else {
            // TODO: get name for tag key, now mocked generic name
            const name = 'All';
            const created = new LabelTag(name, tagKey, [tool]);
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

    public getToolIconName(iconName: string): string {
        return LabelExplorerComponent.toolIconNames.get(iconName);
    }
}
