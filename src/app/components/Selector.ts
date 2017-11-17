import {SliceSelection} from './SliceSelection';

export interface Selector<SliceSelection> {

  drawPreviousSelections(): any;

  drawSelection(selection: SliceSelection, color: string): any;

  onMouseDown(event: MouseEvent): any;

  onMouseMove(event: MouseEvent): any;

  onMouseUp(event: MouseEvent): any;

  clearCanvasSelection(): any;

  clearData(): any;

  addCurrentSelection(): any;

  updateCurrentSlice(currentSliceId: number): any;

  updateCanvasPosition(canvasRect: ClientRect): any;

  hasArchivedSelections(): boolean;

  hasSliceSelection(): boolean;

  hasFullSelection(): boolean;

  getSelections(): SliceSelection[];

  archiveSelections(selectionMap?: Map<number, SliceSelection>): any;

  removeCurrentSelection(): any;

  clearSelections(): any;

}
