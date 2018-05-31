import {EventEmitter} from '@angular/core';
import {SelectionStateMessage} from '../../model/SelectionStateMessage';

export interface Selector<SliceSelection> {

    drawSelections(): any;

    drawSelection(selection: SliceSelection, color: string): any;

    onMouseDown(event: MouseEvent): any;

    onMouseMove(event: MouseEvent): any;

    onMouseUp(event: MouseEvent): any;

    clearCanvasSelection(): any;

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

    removeCurrentSelection(): any;

    removeSelection(selectionId: number): void;

    clearSelections(): any;

    updateCanvasWidth(width: number): void;

    updateCanvasHeight(height: number): void;

    normalizeByView(paramX: number, paramY: number): {x: number, y: number};

    scaleToView(paramX: number, paramY: number): {x: number, y: number};

    // Show selection on all slice images
    pinSelection(selectionId: number, newValue: boolean): void;

    // Hides selection from user view without deleting from memory
    hideSelection(selectionId: number, newValue: boolean): void;
}
