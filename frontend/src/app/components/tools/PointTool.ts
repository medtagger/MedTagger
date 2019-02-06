import { ToolBase } from './ToolBase';
import { PointSelection } from '../../model/selections/PointSelection';
import { Tool } from './Tool';
import { SliceSelectionType } from '../../model/selections/SliceSelection';

export class PointTool extends ToolBase<PointSelection> implements Tool<PointSelection> {
    private draggedSelection: PointSelection;

    protected getStyle(): any {
        return {
            ...super.getStyle(),
            RADIUS: 10,
            SELECTION_FONT_COLOR: '#ffffff'
        };
    }

    public drawSelection(selection: PointSelection): void {
        console.log('PointTool | drawSelection | selection: ', selection);
        this.canvasCtx.fillStyle = this.getColorForSelection(selection);

        const scaledPointPosition: { x: number; y: number } = this.scaleToView(selection.x, selection.y);

        this.canvasCtx.beginPath();
        this.canvasCtx.arc(scaledPointPosition.x, scaledPointPosition.y, this.getStyle().RADIUS, 0, 2 * Math.PI);
        this.canvasCtx.fill();

        const fontSize = this.getStyle().SELECTION_FONT_SIZE;
        this.canvasCtx.font = `${fontSize}px Arial`;
        this.canvasCtx.fillStyle = this.getStyle().SELECTION_FONT_COLOR;
        this.canvasCtx.textAlign = 'center';
        this.canvasCtx.fillText(
            selection.getId().toString(),
            scaledPointPosition.x,
            scaledPointPosition.y + this.getStyle().SELECTION_FONT_SIZE * 0.25
        );
        this.canvasCtx.closePath();
    }

    private checkDistance(point: PointSelection, x: number, y: number) {
        const scaledPoint: { x: number; y: number } = this.scaleToView(point.x, point.y);
        const distance = Math.sqrt(Math.pow(scaledPoint.x - x, 2) + Math.pow(scaledPoint.y - y, 2));

        return distance < this.getStyle().RADIUS;
    }

    public onMouseDown(event: MouseEvent): void {
        console.log('PointTool | onMouseDown | event: ', event);
        const x = event.clientX - this.canvasPosition.left;
        const y = event.clientY - this.canvasPosition.top;

        this.draggedSelection = this.getOwnSelectionsOnCurrentSlice().find(
            (selection: PointSelection) => !selection.hidden && this.checkDistance(selection, x, y)
        );

        if (!this.draggedSelection) {
            const { x: normalizedX, y: normalizedY } = this.normalizeByView(x, y);
            this.addSelection(new PointSelection(normalizedX, normalizedY, this.currentSlice, this.currentTag, SliceSelectionType.NORMAL));
        }
    }

    public onMouseMove(event: MouseEvent): void {
        if (this.draggedSelection) {
            const newX = event.clientX - this.canvasPosition.left;
            const newY = event.clientY - this.canvasPosition.top;
            const normalizedValues: { x: number; y: number } = this.normalizeByView(newX, newY);

            this.draggedSelection.x = normalizedValues.x;
            this.draggedSelection.y = normalizedValues.y;
            this.draggedSelection = this.updateSelection(this.draggedSelection);
        }
    }

    public onMouseUp(): void {
        this.draggedSelection = undefined;
    }

    public getToolName(): string {
        return 'POINT';
    }
}
