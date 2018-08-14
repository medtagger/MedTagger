import {Selector} from './Selector';
import {SelectorBase} from './SelectorBase';
import {Point} from '../../model/Point';
import {SelectorAction} from '../../model/SelectorAction';
import {ChainSelection} from '../../model/selections/ChainSelection';

export class ChainSelector extends SelectorBase<ChainSelection> implements Selector<ChainSelection> {

    private selectedAreaPointIndex = -1;
    private selectingInProgress = false;

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

    public getActions(): Array<SelectorAction> {
        return [
            new SelectorAction('Stop', () => this.selectingInProgress, () => {
                this.completeSelection(false);
            }),
            new SelectorAction('Loop', () => this.selectingInProgress && this.selectedArea.points.length > 2, () => {
                this.completeSelection(true);
            })
        ];
    }

    public drawSelection(selection: ChainSelection, color: string): void {
        console.log('ChainSelector | drawSelection | selection: ', selection);

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
        this.selectingInProgress = undefined;
        this.requestRedraw();
    }

    public onMouseDown(event: MouseEvent): void {
        console.log('ChainSelector | onMouseDown | event: ', event);
        const x = (event.clientX) - this.canvasPosition.left;
        const y = (event.clientY) - this.canvasPosition.top;

        if (this.selectingInProgress) {
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
                                return;
                            }
                        }
                    }
                });
            }

            if (!this.selectedArea) {
                const normalizedPoint: { x: number, y: number } = this.normalizeByView(x, y);
                const point = new Point(normalizedPoint.x, normalizedPoint.y);
                this.selectedArea = new ChainSelection([point], this.currentSlice, this.currentTag.key);
                this.selectingInProgress = true;
                this.requestRedraw();
            }
        }
    }

    public onMouseMove(event: MouseEvent): void {
        if (this.selectedArea && !this.selectingInProgress) {
            console.log('ChainSelector | updateSelection | event: ', event);

            const newX = event.clientX - this.canvasPosition.left;
            const newY = event.clientY - this.canvasPosition.top;

            const normalizedValues: { x: number, y: number } = this.normalizeByView(newX, newY);

            this.selectedArea.points[this.selectedAreaPointIndex] = new Point(normalizedValues.x, normalizedValues.y);
            this.requestRedraw();
        }
    }

    public onMouseUp(event: MouseEvent): void {
        if (!this.selectingInProgress) {
            this.selectedArea = undefined;
        }
    }

    public deselect(): void {
        this.completeSelection(false);
    }

    public getSelectorName(): string {
        return 'CHAIN';
    }
}
