import {RectangleSelection} from '../../model/selections/RectangleSelection';
import {ToolBase} from './ToolBase';
import {Tool} from './Tool';
import { SliceSelectionType } from '../../model/selections/SliceSelection';

export class RectangleTool extends ToolBase<RectangleSelection> implements Tool<RectangleSelection> {

    private currentSelection: RectangleSelection;

    protected getStyle(): any {
        return {
            ...super.getStyle(),
            SELECTION_LINE_DENSITY: [6],
            SELECTION_LINE_WIDTH: 3,
        };
    }

    public reset(): void {
        if (this.currentSelection) {
            this.removeSelection(this.currentSelection);
            this.currentSelection = undefined;
        }
    }

    public drawSelection(selection: RectangleSelection): void {
        console.log('RectangleTool | drawSelection | selection: ', selection);
        const color = this.getColorForSelection(selection);
        this.canvasCtx.strokeStyle = color;
        this.canvasCtx.setLineDash(this.getStyle().SELECTION_LINE_DENSITY);
        this.canvasCtx.lineWidth = this.getStyle().SELECTION_LINE_WIDTH;

        const scaledStartPoint: { x: number, y: number } = this.scaleToView(selection.x, selection.y);

        const scaledSelectionValues: { x: number, y: number } = this.scaleToView(selection.width, selection.height);

        this.canvasCtx.strokeRect(scaledStartPoint.x, scaledStartPoint.y,
            scaledSelectionValues.x, scaledSelectionValues.y);

        const fontSize = this.getStyle().SELECTION_FONT_SIZE;
        this.canvasCtx.font = `${fontSize}px Arial`;
        this.canvasCtx.fillStyle = color;
        this.canvasCtx.textAlign = 'start';
        this.canvasCtx.fillText(selection.getId().toString(), scaledStartPoint.x + (fontSize / 4), scaledStartPoint.y + fontSize);
        this.canvasCtx.setLineDash([]);
    }

    public onMouseDown(event: MouseEvent): void {
        console.log('RectangleTool | startMouseSelection | event: ', event);
        const selectionStartX = (event.clientX) - this.canvasPosition.left;
        const selectionStartY = (event.clientY) - this.canvasPosition.top;

        const { x, y } = this.normalizeByView(selectionStartX, selectionStartY);

        this.currentSelection = new RectangleSelection(x, y, this.currentSlice, this.currentTag, SliceSelectionType.NORMAL);
        this.addSelection(this.currentSelection);
    }

    public onMouseMove(event: MouseEvent): void {
        if (this.currentSelection) {
            const { x, y } = this.scaleToView(this.currentSelection.x, this.currentSelection.y);

            const newWidth = (event.clientX - this.canvasPosition.left) - x;
            const newHeight = (event.clientY - this.canvasPosition.top) - y;

            const normalizedValues: { x: number, y: number } = this.normalizeByView(newWidth, newHeight);

            this.currentSelection.width = normalizedValues.x;
            this.currentSelection.height = normalizedValues.y;
            this.redraw();
        }
    }

    public onMouseUp(): void {
        if (this.currentSelection) {
            const isSelectionInvalid = this.currentSelection.height === 0 || this.currentSelection.width === 0;
            if (isSelectionInvalid) {
                this.removeSelection(this.currentSelection);
            }
            this.currentSelection = undefined;
        }
    }

    public canChangeSlice(): boolean {
        return !this.currentSelection;
    }

    public getToolName(): string {
        return 'RECTANGLE';
    }

}
