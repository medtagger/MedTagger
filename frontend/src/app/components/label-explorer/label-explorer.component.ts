import { List } from 'immutable';
import { Component, Input, ChangeDetectionStrategy, Output, EventEmitter } from '@angular/core';
import { SliceSelection } from '../../model/selections/SliceSelection';
import { LabelTag } from './../../model/labels/LabelTag';

@Component({
    selector: 'app-label-explorer',
    templateUrl: './label-explorer.component.html',
    styleUrls: ['./label-explorer.component.scss'],
    changeDetection: ChangeDetectionStrategy.OnPush
})
export class LabelExplorerComponent {

    static readonly toolIconNames: Map<string, string> = new Map([
        ['RECTANGLE', 'crop'],
        ['BRUSH', 'brush'],
        ['POINT', 'gesture-tap'],
        ['CHAIN', 'vector-polyline'],
        ['ERASER', 'eraser'],
        ['ZOOM_IN', 'magnify-plus-outline'],
        ['ZOOM_OUT', 'magnify-minus-outline'],
        ['UNDO', 'undo'],
        ['REDO', 'redo']
    ]);

    @Input() selections: List<SliceSelection>;

    @Output() selectionsChange: EventEmitter<List<SliceSelection>> = new EventEmitter();

    private hiddenTags: List<String> = List([]);

    public getTags(): List<LabelTag> {
        return this.selections
            .map(selection => selection.labelTag)
            .filter((tag, index, tags) => tags.findIndex(x => x.key === tag.key) === index)
            .sort((x, y) => x.name.localeCompare(y.name));
    }

    public getSelectionsForTag(tag: LabelTag): List<SliceSelection> {
        return this.selections
            .filter(selection => selection.labelTag.key === tag.key)
            .sort((x, y) => x.getId() - y.getId())
            .sort((x, y) => x.sliceIndex - y.sliceIndex);
    }

    public getToolIconName(iconName: string): string {
        return LabelExplorerComponent.toolIconNames.get(iconName);
    }

    public removeSelection(selection: SliceSelection): void {
        this.selectionsChange.emit(this.selections.remove(this.selections.indexOf(selection)));
    }

    public toggleSelectionPinning(selection: SliceSelection): void {
        selection.pinned = !selection.pinned;
        this.selectionsChange.emit(List(this.selections.toArray()));
    }

    public toggleSelectionVisibility(selection: SliceSelection): void {
        selection.hidden = !selection.hidden;
        this.selectionsChange.emit(List(this.selections.toArray()));
    }

    public isTagHidden(tag: LabelTag): boolean {
        return this.hiddenTags.indexOf(tag.key) > -1;
    }

    public toggleTagVisibility(tag: LabelTag) {
        if (this.isTagHidden(tag)) {
            this.hiddenTags = this.hiddenTags.remove(this.hiddenTags.indexOf(tag.key));
        } else {
            this.hiddenTags = this.hiddenTags.push(tag.key);
        }
    }
}
