import {Component, EventEmitter, OnInit} from '@angular/core';
import {LabelTag} from '../../model/labels/LabelTag';
import {LabelListItem} from '../../model/labels/LabelListItem';

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
        let labels = this.labels.filter(label => label.tag.key === tag.key);
        // Sorts ascending by SelectionID
        labels = labels.sort((tagA, tagB) => tagA.selectionId - tagB.selectionId);
        // Sorts ascending by SliceIndex (leaving order by SelectionID)
        labels = labels.sort((tagA, tagB) => tagA.sliceIndex - tagB.sliceIndex);
        return labels;
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

    public addLabel(selectionId: number, labelSlice: number, tag: LabelTag, tool: string): void {
        this.addTag(tag);
        const newItem: LabelListItem = new LabelListItem(selectionId, labelSlice, tag, tool);
        this.labels.push(newItem);
    }

    public replaceExistingLabel(selectionId: number, labelSlice: number, tag: LabelTag, tool: string): void {
        const currentLabelIndex = this.labels.findIndex(label => label.tag === tag
            && label.sliceIndex === labelSlice
            && label.toolName === tool);
        console.log('currentLabelIndex: ', currentLabelIndex);
        if (currentLabelIndex > -1) {
            this.labels[currentLabelIndex] = new LabelListItem(selectionId, labelSlice, tag, tool);
            console.log('Replace existing label');
        } else {
            this.addLabel(selectionId, labelSlice, tag, tool);
        }
    }

    private addTag(tag: LabelTag) {
        const found: LabelTag = this.tags.find(labelTag => labelTag.key === tag.key);
        if (found) {
            return;
        } else {
            this.tags.push(tag);
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
