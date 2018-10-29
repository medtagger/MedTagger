import {EventEmitter} from '@angular/core';
import {SelectionStateMessage} from '../../model/SelectionStateMessage';
import {ToolAction} from '../../model/ToolAction';
import {LabelTag} from '../../model/labels/LabelTag';

export interface Tool<SliceSelection> {

    drawSelections(): any;

    drawSelection(selection: SliceSelection, color: string): any;

    onMouseDown(event: MouseEvent): void;

    onMouseMove(event: MouseEvent): void;

    onMouseUp(event: MouseEvent): void;

    clearData(): any;

    setRedrawRequestEmitter(emitter: EventEmitter<void>): void;

    getStateChangeEmitter(): EventEmitter<SelectionStateMessage>;

    addSelection(selection: SliceSelection): void;

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

    getToolName(): string;

    getActions(): Array<ToolAction>;

    isSingleSelectionPerSlice(): boolean;

    canChangeSlice(): boolean;

    onToolChange(): void;
}
