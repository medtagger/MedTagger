import {Selector} from './Selector';
import {SelectorBase} from './SelectorBase';
import {SelectionStateMessage} from '../../model/SelectionStateMessage';
import {ChainSelection} from '../../model/ChainSelection';
import {Point} from '../../model/Point';

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
            this.canvasCtx.arc(scaledPointPosition.x , scaledPointPosition.y, this.getStyle().RADIUS, 0, 2 * Math.PI);
            this.canvasCtx.fill();

            if (lastPosition) {
                this.canvasCtx.beginPath();
                this.canvasCtx.moveTo(lastPosition.x, lastPosition.y);
                this.canvasCtx.lineTo(scaledPointPosition.x, scaledPointPosition.y);
                this.canvasCtx.stroke();
            }

            lastPosition = scaledPointPosition;
        }
        if (selection.isLoop) {
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

    private raycast(x: number, y: number, selections: Array<ChainSelection>): [ChainSelection, number] {
        let result: [ChainSelection, number] = [undefined, -1];
        selections.forEach((selection: ChainSelection) => {
            if (!selection.hidden) {
                for (const index in selection.points) {
                    if (this.checkDistance(selection.points[index], x, y)) {
                        result = [selection, +index];
                        return;
                    }
                }
            }
        });
        return result;
    }

    private checkDistance(point: Point, x: number, y: number) {
        const scaledPoint: { x: number, y: number } = this.scaleToView(point.x, point.y);
        const distance = Math.sqrt(Math.pow(scaledPoint.x - x, 2) + Math.pow(scaledPoint.y - y, 2));

        return distance < this.getStyle().RADIUS;
    }

    public onMouseDown(event: MouseEvent): boolean {
        console.log('ChainSelector | onMouseDown | event: ', event);
        const x = (event.clientX) - this.canvasPosition.left;
        const y = (event.clientY) - this.canvasPosition.top;

        if (event.button === 0) {
            if (this.selectingInProgress) {
                const [overSelection, index] = this.raycast(x, y, [this.selectedArea]);
                if (overSelection && index === 0 && overSelection.points.length > 2) {
                    this.selectedArea.points.pop();
                    this.selectedArea.isLoop = true;
                    this.selectedArea = undefined;
                    this.selectingInProgress = false;
                } else {
                    const normalizedPoint: { x: number, y: number } = this.normalizeByView(x, y);
                    const point = new Point(normalizedPoint.x, normalizedPoint.y);
                    this.selectedArea.points.push(point);
                    this.selectedAreaPointIndex += 1;
                }
                return true;
            } else {
                const currentSliceSelections = this.selections.get(this.currentSlice) || [];
                [this.selectedArea, this.selectedAreaPointIndex] = this.raycast(x, y, currentSliceSelections);

                if (!this.selectedArea) {
                    const normalizedPoint: { x: number, y: number } = this.normalizeByView(x, y);
                    const point = new Point(normalizedPoint.x, normalizedPoint.y);
                    this.selectedArea = new ChainSelection([point, point], this.currentSlice);
                    this.selectedAreaPointIndex = 1;
                    this.addSelection(this.selectedArea);
                    this.selectingInProgress = true;
                    return true;
                }
            }
        } else if (event.button === 2 && this.selectingInProgress) {
            if (this.selectedArea.points.length === 2) {
                this.removeSelection(this.selectedArea.getId());
                this.stateChange.emit(new SelectionStateMessage(this.selectedArea.getId(), this.selectedArea.sliceIndex, true));
            } else {
                this.selectedArea.points.pop();
            }
            this.selectedArea = undefined;
            this.selectingInProgress = false;
            return true;
        }

        return false;
    }

    public onMouseMove(mouseEvent: MouseEvent): boolean {
        if (this.selectedArea) {
            console.log('ChainSelector | drawSelectionRectangle | onmousemove clienXY: ', mouseEvent.clientX, mouseEvent.clientY);
            this.updateSelection(mouseEvent);
            return true;
        }
        return false;
    }

    private updateSelection(event: MouseEvent): void {
        console.log('ChainSelector | updateSelection | event: ', event);

        if (this.selectedArea) {
            const newX = event.clientX - this.canvasPosition.left;
            const newY = event.clientY - this.canvasPosition.top;

            const normalizedValues: { x: number, y: number } = this.normalizeByView(newX, newY);

            this.selectedArea.points[this.selectedAreaPointIndex] = new Point(normalizedValues.x, normalizedValues.y);
        }
    }

    public onMouseUp(event: MouseEvent): boolean {
        if (!this.selectingInProgress) {
            this.selectedArea = undefined;
        }
        return false;
    }

    public getSelectorName(): string {
        return 'CHAIN';
    }
}
