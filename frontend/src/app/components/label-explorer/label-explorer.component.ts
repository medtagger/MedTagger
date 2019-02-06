import { LabelTag } from './../../model/labels/LabelTag';
import {Component, EventEmitter, OnInit, Input} from '@angular/core';
import { SliceSelection } from '../../model/selections/SliceSelection';

@Component({
    selector: 'app-label-explorer',
    templateUrl: './label-explorer.component.html',
    styleUrls: ['./label-explorer.component.scss']
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

    @Input() selections: Array<SliceSelection>;

    private hiddenTags: Array<String> = [];

    public getTags(): Array<LabelTag> {
        return this.selections
            .map(selection => selection.labelTag)
            .filter((tag, index, tags) => tags.findIndex(x => x.key === tag.key) === index)
            .sort((x, y) => x.name.localeCompare(y.name));
    }

    public getSelectionsForTag(tag: LabelTag): Array<SliceSelection> {
        return this.selections
            .filter(selection => selection.labelTag.key === tag.key)
            .sort((x, y) => x.getId() - y.getId())
            .sort((x, y) => x.sliceIndex - y.sliceIndex);
    }

    public getToolIconName(iconName: string): string {
        return LabelExplorerComponent.toolIconNames.get(iconName);
    }

    public removeSelection(selection: SliceSelection): void {
        this.selections.splice(this.selections.indexOf(selection), 1);
    }

    public isTagHidden(tag: LabelTag) {
        return this.hiddenTags.indexOf(tag.key) > -1;
    }

    public toggleTagVisibility(tag: LabelTag) {
        if (this.isTagHidden(tag)) {
            this.hiddenTags.splice(this.hiddenTags.indexOf(tag.key), 1);
        } else {
            this.hiddenTags.push(tag.key);
        }
    }
}
