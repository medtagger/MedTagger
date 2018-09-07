import {EventEmitter} from '@angular/core';
import {SelectionStateMessage} from '../../model/SelectionStateMessage';
import {SelectorAction} from '../../model/SelectorAction';
import {LabelTag} from '../../model/labels/LabelTag';

export interface Selector<SliceSelection> {

    drawSelections(): any;

    drawSelection(selection: SliceSelection, color: string): any;

    onMouseDown(event: MouseEvent): void;

    onMouseMove(event: MouseEvent): void;

    onMouseUp(event: MouseEvent): void;

    clearData(): any;

    setRedrawRequestEmitter(emitter: EventEmitter<void>): void;

    getStateChangeEmitter(): EventEmitter<SelectionStateMessage>;

    updateCurrentSlice(currentSliceId: number): any;

    updateCurrentTag(tag: LabelTag);

    updateCanvasPosition(canvasRect: ClientRect): any;

    hasArchivedSelections(): boolean;

    hasSliceSelection(): boolean;

    hasValidSelection(...validityFlags: boolean[]): boolean;

    getSelections(): SliceSelection[];

    formArchivedSelections(selectionMap: Array<SliceSelection>): Array<SliceSelection>;

    archiveSelections(selectionMap?: Array<SliceSelection>): any;

    removeSelectionsOnCurrentSlice(): any;

    removeSelectionsOnSlice(sliceId: number): void;

    removeSelection(selectionId: number): boolean;

    clearSelections(): any;

    updateCanvasWidth(width: number): void;

    updateCanvasHeight(height: number): void;

    // Show selection on all slice images, return true if selection with selectionId exists
    pinSelection(selectionId: number, newValue: boolean): boolean;

    // Hides selection from user view without deleting from memory, return true if selection with selectionId exists
    hideSelection(selectionId: number, newValue: boolean): boolean;

    getSelectorName(): string;

    getActions(): Array<SelectorAction>;

    deselect(): void;

    isSingleSelectionPerSlice(): boolean;

    // Used to check if using mouse wheel is safe with current selector
    canUseMouseWheel(): boolean;
}
