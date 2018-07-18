import {EventEmitter} from '@angular/core';
import {SelectionStateMessage} from '../../model/SelectionStateMessage';
import { LabelTag } from '../../model/LabelTag';

export interface Selector<SliceSelection> {

    drawSelections(): any;

    drawSelection(selection: SliceSelection, color: string): any;

    onMouseDown(event: MouseEvent): boolean;

    onMouseMove(event: MouseEvent): boolean;

    onMouseUp(event: MouseEvent): boolean;

    clearData(): any;

    getStateChangeEmitter(): EventEmitter<SelectionStateMessage>;

    addCurrentSelection(): any;

    updateCurrentSlice(currentSliceId: number): any;

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

    normalizeByView(paramX: number, paramY: number): {x: number, y: number};

    scaleToView(paramX: number, paramY: number): {x: number, y: number};

    // Show selection on all slice images, return true if selection with selectionId exists
    pinSelection(selectionId: number, newValue: boolean): boolean;

    // Hides selection from user view without deleting from memory, return true if selection with selectionId exists
    hideSelection(selectionId: number, newValue: boolean): boolean;

    getSelectorName(): string;

    setCurrentTag(tag: LabelTag);
}
