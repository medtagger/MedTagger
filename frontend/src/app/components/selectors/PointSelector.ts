import {EventEmitter} from "@angular/core";
import {SelectionStateMessage} from "../../model/SelectionStateMessage";
import {SelectorBase} from "./SelectorBase";
import {PointSelection} from "../../model/PointSelection";
import {Selector} from "./Selector";

export class PointSelector extends SelectorBase<PointSelection> implements Selector<PointSelection> {

    readonly STYLE = {
        RADIUS: 10,
        CURRENT_SELECTION_COLOR: '#ff0000',
        OTHER_SELECTION_COLOR: '#256fde',
        ARCHIVED_SELECTION_COLOR: '#5f27e5'
    };

    constructor(canvas: HTMLCanvasElement) {
        super();
        this.canvasCtx = canvas.getContext('2d');
        this.canvasSize = {
            width: canvas.width,
            height: canvas.height
        };
        this.selections = new Map<number, [PointSelection]>();
        this.selectedArea = undefined;
        this.currentSlice = undefined;
        this.stateChange = new EventEmitter<SelectionStateMessage>();
    }

    public formArchivedSelections(selectionMap: PointSelection[]): PointSelection[] {
        selectionMap.forEach((selection: PointSelection) => {
            this.drawSelection(selection, this.STYLE.ARCHIVED_SELECTION_COLOR);
            console.log('PointSelector | scaleToView selection: ', selection);
        });
        return selectionMap;
    }

    public drawSelections(): void {
        console.log('PointSelector | drawSelections | selection: ', this.selections);
        this.getSelections().forEach((selection: PointSelection) => {
            let color: string;
            const isCurrent: boolean = (selection.sliceIndex === this.currentSlice);
            if (isCurrent) {
                color = this.STYLE.CURRENT_SELECTION_COLOR;
            } else {
                color = this.STYLE.OTHER_SELECTION_COLOR;
            }
            if ((selection.pinned || isCurrent) && (!selection.hidden)) {
                this.drawSelection(selection, color);
            }
        });
    }

    public drawSelection(selection: PointSelection, color: string): void {
        console.log('PointSelector | drawSelection | selection: ', selection);
        this.canvasCtx.fillStyle = color;

        const scaledPointPosition: { x: number, y: number } = this.scaleToView(selection.positionX, selection.positionY);

        this.canvasCtx.beginPath();
        this.canvasCtx.arc(scaledPointPosition.x , scaledPointPosition.y, this.STYLE.RADIUS, 0, 2 * Math.PI);
        this.canvasCtx.fill();
    }

    private checkDistance(point: PointSelection, x: number, y: number) {
        const scaledPoint: { x: number, y: number } = this.scaleToView(point.positionX, point.positionY);
        const distance = Math.sqrt(Math.pow(scaledPoint.x - x, 2) + Math.pow(scaledPoint.y - y, 2));

        return distance < this.STYLE.RADIUS;
    }

    public onMouseDown(event: MouseEvent): boolean {
        console.log('PointSelector | onMouseDown | event: ', event);
        const x = (event.clientX) - this.canvasPosition.left;
        const y = (event.clientY) - this.canvasPosition.top;

        const currentSliceSelections = this.selections.get(this.currentSlice);
        if (currentSliceSelections) {
            currentSliceSelections.forEach((selection: PointSelection) => {
                if (!selection.hidden && this.checkDistance(selection, x, y)) {
                    this.mouseDrag = true;
                    this.selectedArea = selection;
                    return;
                }
            });
        }

        if (!this.mouseDrag) {
            const normalizedPoint: { x: number, y: number } = this.normalizeByView(x, y);
            this.selectedArea = new PointSelection(normalizedPoint.x, normalizedPoint.y, this.currentSlice);
            this.addCurrentSelection();
            return true;
        }
        return false;
    }

    public onMouseMove(mouseEvent: MouseEvent): boolean {
        if (this.mouseDrag && this.selectedArea) {
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
        this.mouseDrag = false;
        return false;
    }

    public getSelectorName(): string {
        return "POINT";
    }
}
