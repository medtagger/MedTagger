import {Tool} from './Tool';
import {ToolBase} from './ToolBase';
import {Point} from '../../model/Point';
import {ChainSelection} from '../../model/selections/ChainSelection';

export class ChainTool extends ToolBase<ChainSelection> implements Tool<ChainSelection> {

    private selectedAreaPointIndex = -1;

    constructor(canvas: HTMLCanvasElement) {
        super(canvas);
    }

    protected getStyle(): any {
        return {
            ...super.getStyle(),
            RADIUS: 10,
            SELECTION_LINE_DENSITY: [0],
            SELECTION_LINE_WIDTH: 3,
            SELECTION_FONT_COLOR: '#ffffff',
        };
    }

    public drawSelection(selection: ChainSelection, color: string): void {
        console.log('ChainTool | drawSelection | selection: ', selection);

        this.canvasCtx.fillStyle = color;
        this.canvasCtx.strokeStyle = color;
        this.canvasCtx.setLineDash(this.getStyle().SELECTION_LINE_DENSITY);
        this.canvasCtx.lineWidth = this.getStyle().SELECTION_LINE_WIDTH;
        let lastPosition: { x: number, y: number };
        for (const point of selection.points) {
            const scaledPointPosition: { x: number, y: number } = this.scaleToView(point.x, point.y);

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
            const scaledPointPosition: { x: number, y: number } = this.scaleToView(selection.points[0].x, selection.points[0].y);
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
            const scaledPointPosition: { x: number, y: number } = this.scaleToView(point.x, point.y);
            this.canvasCtx.fillText(selection.getId().toString(), scaledPointPosition.x,
                scaledPointPosition.y + this.getStyle().SELECTION_FONT_SIZE * 0.25);
        }
    }

    private checkDistance(point: Point, x: number, y: number) {
        const scaledPoint: { x: number, y: number } = this.scaleToView(point.x, point.y);
        const distance = Math.sqrt(Math.pow(scaledPoint.x - x, 2) + Math.pow(scaledPoint.y - y, 2));

        return distance < this.getStyle().RADIUS;
    }

    private completeSelection(isLoop: boolean) {
        if (this.selectedArea && this.selectedArea.points.length > 1) {
            this.selectedArea.loop = isLoop;
            this.addSelection(this.selectedArea);
        }
        this.selectedArea = undefined;
        this.requestRedraw();
    }

    public onMouseDown(event: MouseEvent): void {
        console.log('ChainTool | onMouseDown | event: ', event);
        const x = (event.clientX) - this.canvasPosition.left;
        const y = (event.clientY) - this.canvasPosition.top;

        if (event.button === 0) {
            // left mouse button
            if (this.selectedArea) {
                if (this.checkDistance(this.selectedArea.points[0], x, y)) {
                    this.selectedArea.points.splice(this.selectedArea.points.length - 1, 1);
                    this.completeSelection(true);
                    return;
                }

                const normalizedPoint: { x: number, y: number } = this.normalizeByView(x, y);
                const point = new Point(normalizedPoint.x, normalizedPoint.y);
                this.selectedArea.points.push(point);
                this.requestRedraw();
            } else {
                const currentSliceSelections = this.selections.get(this.currentSlice);
                if (currentSliceSelections) {
                    currentSliceSelections.forEach((selection: ChainSelection) => {
                        if (!selection.hidden) {
                            for (const index in selection.points) {
                                if (this.checkDistance(selection.points[index], x, y)) {
                                    this.selectedArea = selection;
                                    this.selectedAreaPointIndex = +index;
                                }
                            }
                        }
                    });
                }

                if (!this.selectedArea) {
                    const normalizedPoint: { x: number, y: number } = this.normalizeByView(x, y);
                    const point = new Point(normalizedPoint.x, normalizedPoint.y);
                    this.selectedArea = new ChainSelection([point, point], false, this.currentSlice, this.currentTag);
                    this.requestRedraw();
                }
            }
        } else if (event.button === 2 && this.selectedArea) {
            // right mouse button
            this.selectedArea.points.splice(this.selectedArea.points.length - 1, 1);
            this.completeSelection(false);
        }
    }

    public onMouseMove(event: MouseEvent): void {
        if (this.selectedArea) {
            console.log('ChainTool | updateSelection | event: ', event);
            const newX = event.clientX - this.canvasPosition.left;
            const newY = event.clientY - this.canvasPosition.top;
            const normalizedValues: { x: number, y: number } = this.normalizeByView(newX, newY);
            if (this.isMovingPoint()) {
                this.selectedArea.points[this.selectedAreaPointIndex] = new Point(normalizedValues.x, normalizedValues.y);
            } else {
                if (this.checkDistance(this.selectedArea.points[0], newX, newY)) {
                    this.selectedArea.points[this.selectedArea.points.length - 1] = this.selectedArea.points[0];
                } else {
                    this.selectedArea.points[this.selectedArea.points.length - 1] = new Point(normalizedValues.x, normalizedValues.y);
                }
            }
            this.requestRedraw();
        }
    }

    public onMouseUp(event: MouseEvent): void {
        if (this.isMovingPoint()) {
            this.selectedArea = undefined;
            this.selectedAreaPointIndex = -1;
        }
    }

    public canChangeSlice(): boolean {
        return !this.selectedArea;
    }

    public getToolName(): string {
        return 'CHAIN';
    }

    public onToolChange(): void {
        // Pop to remove last 'moving' point 
        this.selectedArea.points.pop();

        this.completeSelection(false);
    }

    private isMovingPoint(): boolean {
        return this.selectedAreaPointIndex !== -1;
    }
}
