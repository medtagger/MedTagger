import {EventEmitter} from "@angular/core";

export interface Selector<SliceSelection> {

    drawPreviousSelections(): any;

    drawSelection(selection: SliceSelection, color: string): any;

    onMouseDown(event: MouseEvent): any;

    onMouseMove(event: MouseEvent): any;

    onMouseUp(event: MouseEvent): any;

    clearCanvasSelection(): any;

    clearData(): any;

    getStateChangeEmitter(): EventEmitter<void>;

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
}
