import {ROISelection2D} from '../model/ROISelection2D';
import {Selector} from './Selector';

export class RectROISelector implements Selector<ROISelection2D> {
  readonly STYLE = {
    SELECTION_FONT_SIZE: 14,
    SELECTION_LINE_DENSITY: [6],
    CURRENT_SELECTION_COLOR: '#ff0000',
    OTHER_SELECTION_COLOR: '#256fde',
    ARCHIVED_SELECTION_COLOR: '#5f27e5'
  };

  selectedArea: ROISelection2D;
  selections: Map<number, ROISelection2D>;
  archivedSelections: Array<ROISelection2D>;
  canvasCtx: CanvasRenderingContext2D;
  protected currentSlice;
  protected mouseDrag = false;
  protected canvasPosition: ClientRect;
  canvasSize: { width: number, height: number };

  constructor(canvas: HTMLCanvasElement) {
    this.canvasCtx = canvas.getContext('2d');
    this.canvasSize = {
      width: canvas.width,
      height: canvas.height
    };
    this.selections = new Map<number, ROISelection2D>();
    this.archivedSelections = [];
    this.selectedArea = undefined;
    this.currentSlice = undefined;
  }

  public getSelections(): ROISelection2D[] {
    return Array.from(this.selections.values());
  }

  public drawPreviousSelections(): void {
    console.log('RectROISelector | drawPreviousSelections | selection: ', this.selections);
    this.selections.forEach((selection: ROISelection2D) => {
      let color: string;
      if (selection.depth === this.currentSlice) {
        color = this.STYLE.CURRENT_SELECTION_COLOR;
      } else {
        color = this.STYLE.OTHER_SELECTION_COLOR;
      }
      this.drawSelection(selection, color);
    });
    console.log('RectROISelector | drawPreviousSelections | archived: ', this.archivedSelections);
    this.archivedSelections.forEach((selection: ROISelection2D) => {
      this.drawSelection(selection, this.STYLE.ARCHIVED_SELECTION_COLOR);
    });
  }

  public drawSelection(selection: ROISelection2D, color: string): void {
    console.log('RectROISelector | drawSelection | selection: ', selection);
    this.canvasCtx.strokeStyle = color;
    this.canvasCtx.setLineDash(this.STYLE.SELECTION_LINE_DENSITY);
    this.canvasCtx.strokeRect(selection.positionX, selection.positionY,
      selection.width, selection.height);

    const fontSize = this.STYLE.SELECTION_FONT_SIZE;
    this.canvasCtx.font = `${fontSize}px Arial`;
    this.canvasCtx.fillStyle = color;
    this.canvasCtx.fillText(selection.depth.toString(), selection.positionX + (fontSize / 4), selection.positionY + fontSize);
  }

  public onMouseDown(event: MouseEvent): void {
    console.log('RectROISelector | startMouseSelection | event: ', event);
    const selectionStartX = (event.clientX) - this.canvasPosition.left;
    const selectionStartY = (event.clientY) - this.canvasPosition.top;
    this.selectedArea = new ROISelection2D(selectionStartX, selectionStartY, this.currentSlice);
    this.selections.delete(this.currentSlice);
    this.mouseDrag = true;
  }

  public onMouseMove(mouseEvent: MouseEvent): void {
    if (this.mouseDrag) {
      console.log('RectROISelector | drawSelectionRectangle | onmousemove clienXY: ', mouseEvent.clientX, mouseEvent.clientY);
      this.updateSelection(mouseEvent);
      this.clearCanvasSelection();

      this.drawSelection(this.selectedArea, this.STYLE.CURRENT_SELECTION_COLOR);
    }
  }

  public updateSelection(event: MouseEvent): void {
    console.log('RectROISelector | updateSelection | event: ', event);
    const newWidth = (event.clientX - this.canvasPosition.left) - this.selectedArea.positionX;
    const newHeight = (event.clientY - this.canvasPosition.top) - this.selectedArea.positionY;

    this.selectedArea.updateWidth(newWidth);
    this.selectedArea.updateHeight(newHeight);
  }

  public onMouseUp(event: MouseEvent): void {
    if (this.mouseDrag) {
      this.mouseDrag = false;
    }
  }

  public clearCanvasSelection(): void {
    this.canvasCtx.clearRect(0, 0, this.canvasSize.width, this.canvasSize.height);
    this.drawPreviousSelections();
  }

  public clearData(): void {
    this.selectedArea = undefined;
    this.selections = new Map<number, ROISelection2D>();
    this.archivedSelections = [];
    this.clearCanvasSelection();
  }

  public addCurrentSelection(): void {
    if (this.selectedArea) {
      this.selections.set(this.currentSlice, this.selectedArea);
      this.selectedArea = undefined;
    }
  }

  public updateCurrentSlice(currentSliceId: number): void {
    this.currentSlice = currentSliceId;
  }

  public updateCanvasPosition(canvasRect: ClientRect) {
    this.canvasPosition = canvasRect;
  }

  public hasArchivedSelections(): boolean {
    return this.archivedSelections.length > 0;
  }

  public hasFullSelection(): boolean {
    return this.selections.size >= 2 || (this.selections.size === 1 && !!this.selectedArea);
  }

  public hasSliceSelection(): boolean {
    return !!this.selections.get(this.currentSlice) || !!this.selectedArea;
  }

  public archiveSelections(selectionMap?: Map<number, ROISelection2D>): void {
    if (!selectionMap) {
      selectionMap = this.selections;
    }
    selectionMap.forEach((value: ROISelection2D) => {
      this.archivedSelections.push(value);
    });
  }

  public removeCurrentSelection(): void {
    if (this.hasSliceSelection()) {
      this.selections.delete(this.currentSlice);
      this.selectedArea = undefined;

      this.clearCanvasSelection();
    }
  }

  public clearSelections() {
    this.selections.clear();
  }
}
