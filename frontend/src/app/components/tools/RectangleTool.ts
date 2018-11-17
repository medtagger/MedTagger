import {RectangleSelection} from '../../model/selections/RectangleSelection';
import {ToolBase} from './ToolBase';
import {Tool} from './Tool';

export class RectangleTool extends ToolBase<RectangleSelection> implements Tool<RectangleSelection> {

    constructor(canvas: HTMLCanvasElement) {
        super(canvas);
    }

    protected getStyle(): any {
        return {
            ...super.getStyle(),
            SELECTION_LINE_DENSITY: [6],
            SELECTION_LINE_WIDTH: 1,
        };
    }

    public drawSelection(selection: RectangleSelection, color: string): void {
        console.log('RectangleTool | drawSelection | selection: ', selection);
        this.canvasCtx.strokeStyle = color;
        this.canvasCtx.setLineDash(this.getStyle().SELECTION_LINE_DENSITY);
        this.canvasCtx.lineWidth = this.getStyle().SELECTION_LINE_WIDTH;

        const scaledStartPoint: { x: number, y: number } = this.scaleToView(selection.positionX, selection.positionY);

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

        const normalizedPoint: { x: number, y: number } = this.normalizeByView(selectionStartX, selectionStartY);

        this.selectedArea = new RectangleSelection(normalizedPoint.x, normalizedPoint.y, this.currentSlice, this.currentTag);
        this.requestRedraw();
    }

    public onMouseMove(mouseEvent: MouseEvent): boolean {
        if (this.selectedArea) {
            console.log('RectangleTool | drawSelectionRectangle | onmousemove clientXY: ', mouseEvent.clientX, mouseEvent.clientY);
            this.updateSelection(mouseEvent);
            this.requestRedraw();
            return true;
        }
        return false;
    }

    public updateSelection(event: MouseEvent): void {
        console.log('RectangleTool | updateSelection | event: ', event);

        if (this.selectedArea) {

            const scaledStartPoint: { x: number, y: number } = this.scaleToView(this.selectedArea.positionX, this.selectedArea.positionY);

            const newWidth = (event.clientX - this.canvasPosition.left) - scaledStartPoint.x;
            const newHeight = (event.clientY - this.canvasPosition.top) - scaledStartPoint.y;

            const normalizedValues: { x: number, y: number } = this.normalizeByView(newWidth, newHeight);

            this.selectedArea.updateWidth(normalizedValues.x);
            this.selectedArea.updateHeight(normalizedValues.y);
        }
    }

    private checkSquareSelection(): boolean {
        return !!this.selectedArea && this.selectedArea.height !== 0 && this.selectedArea.width !== 0;
    }

    public onMouseUp(event: MouseEvent): boolean {
        if (this.selectedArea) {
            if (this.checkSquareSelection()) {
                this.addSelection(this.selectedArea);
            }
            this.selectedArea = undefined;
            this.requestRedraw();
            return true;
        }
        return false;
    }

    public canChangeSlice(): boolean {
        return !this.selectedArea;
    }

    public getToolName(): string {
        return 'RECTANGLE';
    }

    public onToolChange(): void {
        this.selectedArea = undefined;
        this.requestRedraw();
    }
}
