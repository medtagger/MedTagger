import { Tool } from './Tool';
import { ToolBase } from './ToolBase';
import { Point } from '../../model/Point';
import { ChainSelection } from '../../model/selections/ChainSelection';
import { SliceSelectionType } from '../../model/selections/SliceSelection';

export class ChainTool extends ToolBase<ChainSelection> implements Tool<ChainSelection> {
    private currentSelection: ChainSelection;
    private draggedPointIndex = -1;

    protected getStyle(): any {
        return {
            ...super.getStyle(),
            RADIUS: 10,
            SELECTION_LINE_DENSITY: [0],
            SELECTION_LINE_WIDTH: 3,
            SELECTION_FONT_COLOR: '#ffffff'
        };
    }

    public reset(): void {
        if (this.currentSelection) {
            this.currentSelection.points.splice(this.currentSelection.points.length - 1, 1);
            this.completeSelection(false);
            this.draggedPointIndex = -1;
        }
    }

    public drawSelection(selection: ChainSelection): void {
        console.log('ChainTool | drawSelection | selection: ', selection);
        const color = this.getColorForSelection(selection);
        this.canvasCtx.fillStyle = color;
        this.canvasCtx.strokeStyle = color;
        this.canvasCtx.setLineDash(this.getStyle().SELECTION_LINE_DENSITY);
        this.canvasCtx.lineWidth = this.getStyle().SELECTION_LINE_WIDTH;
        let lastPosition: { x: number; y: number };
        for (const point of selection.points) {
            const scaledPointPosition: { x: number; y: number } = this.scaleToView(point.x, point.y);

            this.canvasCtx.beginPath();
            this.canvasCtx.arc(scaledPointPosition.x, scaledPointPosition.y, this.getStyle().RADIUS, 0, 2 * Math.PI);
            this.canvasCtx.fill();

            if (lastPosition) {
                this.canvasCtx.beginPath();
                this.canvasCtx.moveTo(lastPosition.x, lastPosition.y);
                this.canvasCtx.lineTo(scaledPointPosition.x, scaledPointPosition.y);
                this.canvasCtx.stroke();
            }

            lastPosition = scaledPointPosition;
        }
        if (selection.loop) {
            const scaledPointPosition: { x: number; y: number } = this.scaleToView(selection.points[0].x, selection.points[0].y);
            this.canvasCtx.beginPath();
            this.canvasCtx.moveTo(lastPosition.x, lastPosition.y);
            this.canvasCtx.lineTo(scaledPointPosition.x, scaledPointPosition.y);
            this.canvasCtx.stroke();
        }

        const fontSize = this.getStyle().SELECTION_FONT_SIZE;
        this.canvasCtx.font = `${fontSize}px Arial`;
        this.canvasCtx.fillStyle = this.getStyle().SELECTION_FONT_COLOR;
        this.canvasCtx.textAlign = 'center';
        for (const point of selection.points) {
            const scaledPointPosition: { x: number; y: number } = this.scaleToView(point.x, point.y);
            this.canvasCtx.fillText(
                selection.getId().toString(),
                scaledPointPosition.x,
                scaledPointPosition.y + this.getStyle().SELECTION_FONT_SIZE * 0.25
            );
        }
    }

    private checkDistance(point: Point, x: number, y: number) {
        const scaledPoint: { x: number; y: number } = this.scaleToView(point.x, point.y);
        const distance = Math.sqrt(Math.pow(scaledPoint.x - x, 2) + Math.pow(scaledPoint.y - y, 2));

        return distance < this.getStyle().RADIUS;
    }

    private completeSelection(isLoop: boolean) {
        if (this.currentSelection) {
            if (this.currentSelection.points.length > 1) {
                this.currentSelection.loop = isLoop;
                this.redraw();
            } else {
                this.removeSelection(this.currentSelection);
            }
        }
        this.currentSelection = undefined;
    }

    public onMouseDown(event: MouseEvent): void {
        console.log('ChainTool | onMouseDown | event: ', event);
        const x = event.clientX - this.canvasPosition.left;
        const y = event.clientY - this.canvasPosition.top;

        if (event.button === 0) {
            // left mouse button
            if (this.currentSelection) {
                if (this.checkDistance(this.currentSelection.points[0], x, y)) {
                    this.currentSelection.points.splice(this.currentSelection.points.length - 1, 1);
                    this.completeSelection(true);
                    return;
                }

                const normalizedPoint: { x: number; y: number } = this.normalizeByView(x, y);
                const point = new Point(normalizedPoint.x, normalizedPoint.y);
                this.currentSelection.points.push(point);
                this.redraw();
            } else {
                this.getOwnSelectionsOnCurrentSlice().forEach((selection: ChainSelection) => {
                    if (!selection.hidden) {
                        for (const index in selection.points) {
                            if (this.checkDistance(selection.points[index], x, y)) {
                                this.currentSelection = selection;
                                this.draggedPointIndex = +index;
                            }
                        }
                    }
                });

                if (!this.currentSelection) {
                    const normalizedPoint: { x: number; y: number } = this.normalizeByView(x, y);
                    const point = new Point(normalizedPoint.x, normalizedPoint.y);
                    this.currentSelection = new ChainSelection(
                        [point, point],
                        false,
                        this.currentSlice,
                        this.currentTag,
                        SliceSelectionType.NORMAL
                    );
                    this.addSelection(this.currentSelection);
                }
            }
        } else if (event.button === 2 && this.currentSelection) {
            // right mouse button
            this.currentSelection.points.splice(this.currentSelection.points.length - 1, 1);
            this.completeSelection(false);
        }
    }

    public onMouseMove(event: MouseEvent): void {
        if (this.currentSelection) {
            console.log('ChainTool | updateSelection | event: ', event);
            const newX = event.clientX - this.canvasPosition.left;
            const newY = event.clientY - this.canvasPosition.top;
            const normalizedValues: { x: number; y: number } = this.normalizeByView(newX, newY);
            if (this.isMovingPoint()) {
                this.currentSelection.points[this.draggedPointIndex] = new Point(normalizedValues.x, normalizedValues.y);
            } else {
                const lastIndex = this.currentSelection.points.length - 1;
                if (this.checkDistance(this.currentSelection.points[0], newX, newY)) {
                    this.currentSelection.points[lastIndex] = this.currentSelection.points[0];
                } else {
                    this.currentSelection.points[lastIndex] = new Point(normalizedValues.x, normalizedValues.y);
                }
            }
            this.redraw();
        }
    }

    public onMouseUp(event: MouseEvent): void {
        if (this.isMovingPoint()) {
            this.currentSelection = undefined;
            this.draggedPointIndex = -1;
        }
    }

    public canChangeSlice(): boolean {
        return !this.currentSelection;
    }

    public getToolName(): string {
        return 'CHAIN';
    }

    private isMovingPoint(): boolean {
        return this.draggedPointIndex !== -1;
    }
}
