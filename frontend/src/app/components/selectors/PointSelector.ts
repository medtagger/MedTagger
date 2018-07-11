import {SelectorBase} from './SelectorBase';
import {PointSelection} from '../../model/PointSelection';
import {Selector} from './Selector';

export class PointSelector extends SelectorBase<PointSelection> implements Selector<PointSelection> {

    constructor(canvas: HTMLCanvasElement) {
        super(canvas);
    }

    protected getStyle(): any {
        return {
            ...super.getStyle(),
            RADIUS: 10,
            SELECTION_FONT_COLOR: '#ffffff',
        };
    }

    public drawSelection(selection: PointSelection, color: string): void {
        console.log('PointSelector | drawSelection | selection: ', selection);
        this.canvasCtx.fillStyle = color;

        const scaledPointPosition: { x: number, y: number } = this.scaleToView(selection.positionX, selection.positionY);

        this.canvasCtx.beginPath();
        this.canvasCtx.arc(scaledPointPosition.x , scaledPointPosition.y, this.getStyle().RADIUS, 0, 2 * Math.PI);
        this.canvasCtx.fill();

        const fontSize = this.getStyle().SELECTION_FONT_SIZE;
        this.canvasCtx.font = `${fontSize}px Arial`;
        this.canvasCtx.fillStyle = this.getStyle().SELECTION_FONT_COLOR;
        this.canvasCtx.textAlign = 'center';
        this.canvasCtx.fillText(selection.getId().toString(), scaledPointPosition.x,
            scaledPointPosition.y + this.getStyle().SELECTION_FONT_SIZE * 0.25);
    }

    private checkDistance(point: PointSelection, x: number, y: number) {
        const scaledPoint: { x: number, y: number } = this.scaleToView(point.positionX, point.positionY);
        const distance = Math.sqrt(Math.pow(scaledPoint.x - x, 2) + Math.pow(scaledPoint.y - y, 2));

        return distance < this.getStyle().RADIUS;
    }

    public onMouseDown(event: MouseEvent): boolean {
        console.log('PointSelector | onMouseDown | event: ', event);
        const x = (event.clientX) - this.canvasPosition.left;
        const y = (event.clientY) - this.canvasPosition.top;

        const currentSliceSelections = this.selections.get(this.currentSlice);
        if (currentSliceSelections) {
            currentSliceSelections.forEach((selection: PointSelection) => {
                if (!selection.hidden && this.checkDistance(selection, x, y)) {
                    this.selectedArea = selection;
                    return;
                }
            });
        }

        if (!this.selectedArea) {
            const normalizedPoint: { x: number, y: number } = this.normalizeByView(x, y);
            this.addSelection(new PointSelection(normalizedPoint.x, normalizedPoint.y, this.currentSlice));
            return true;
        }
        return false;
    }

    public onMouseMove(mouseEvent: MouseEvent): boolean {
        if (this.selectedArea) {
            console.log('PointSelector | drawSelectionRectangle | onmousemove clienXY: ', mouseEvent.clientX, mouseEvent.clientY);
            this.updateSelection(mouseEvent);
            return true;
        }
        return false;
    }

    public updateSelection(event: MouseEvent): void {
        console.log('PointSelector | updateSelection | event: ', event);

        if (this.selectedArea) {
            const newX = event.clientX - this.canvasPosition.left;
            const newY = event.clientY - this.canvasPosition.top;

            const normalizedValues: { x: number, y: number } = this.normalizeByView(newX, newY);

            this.selectedArea.updatePositionX(normalizedValues.x);
            this.selectedArea.updatePositionY(normalizedValues.y);
        }
    }

    public onMouseUp(event: MouseEvent): boolean {
        this.selectedArea = undefined;
        return false;
    }

    public getSelectorName(): string {
        return 'POINT';
    }
}
