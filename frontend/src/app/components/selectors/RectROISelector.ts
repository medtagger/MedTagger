import {ROISelection2D} from '../../model/ROISelection2D';
import {EventEmitter} from '@angular/core';
import {SelectorBase} from './SelectorBase';
import {SelectionStateMessage} from '../../model/SelectionStateMessage';

export class RectROISelector extends SelectorBase<ROISelection2D> {
    readonly STYLE = {
        SELECTION_FONT_SIZE: 14,
        SELECTION_LINE_DENSITY: [6],
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
        this.selections = new Map<number, ROISelection2D>();
        this.selectedArea = undefined;
        this.currentSlice = undefined;
        this.stateChange = new EventEmitter<SelectionStateMessage>();
    }

    public formArchivedSelections(selectionMap: ROISelection2D[]): ROISelection2D[] {
        selectionMap.forEach((selection: ROISelection2D) => {
            this.drawSelection(selection, this.STYLE.ARCHIVED_SELECTION_COLOR);
            console.log('RectROISelector | scaleToView selection: ', selection);
        });
        return selectionMap;
    }

    public drawSelections(): void {
        console.log('RectROISelector | drawSelections | selection: ', this.selections);
        this.selections.forEach((selection: ROISelection2D) => {
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

    public drawSelection(selection: ROISelection2D, color: string): void {
        console.log('RectROISelector | drawSelection | selection: ', selection);
        this.canvasCtx.strokeStyle = color;
        this.canvasCtx.setLineDash(this.STYLE.SELECTION_LINE_DENSITY);

        const scaledStartPoint: { x: number, y: number } = this.scaleToView(selection.positionX, selection.positionY);

        const scaledSelectionValues: { x: number, y: number } = this.scaleToView(selection.width, selection.height);

        this.canvasCtx.strokeRect(scaledStartPoint.x, scaledStartPoint.y,
            scaledSelectionValues.x, scaledSelectionValues.y);

        const fontSize = this.STYLE.SELECTION_FONT_SIZE;
        this.canvasCtx.font = `${fontSize}px Arial`;
        this.canvasCtx.fillStyle = color;
        this.canvasCtx.fillText(selection.sliceIndex.toString(), scaledStartPoint.x + (fontSize / 4), scaledStartPoint.y + fontSize);
    }

    public onMouseDown(event: MouseEvent): void {
        console.log('RectROISelector | startMouseSelection | event: ', event);
        const selectionStartX = (event.clientX) - this.canvasPosition.left;
        const selectionStartY = (event.clientY) - this.canvasPosition.top;

        const normalizedPoint: { x: number, y: number } = this.normalizeByView(selectionStartX, selectionStartY);

        this.selectedArea = new ROISelection2D(normalizedPoint.x, normalizedPoint.y, this.currentSlice);
        this.selections.delete(this.currentSlice);
        this.mouseDrag = true;
    }

    public onMouseMove(mouseEvent: MouseEvent): void {
        if (this.mouseDrag && this.selectedArea) {
            console.log('RectROISelector | drawSelectionRectangle | onmousemove clienXY: ', mouseEvent.clientX, mouseEvent.clientY);
            this.updateSelection(mouseEvent);

            this.redrawSelections();

            this.drawSelection(this.selectedArea, this.STYLE.CURRENT_SELECTION_COLOR);
        }
    }

    public updateSelection(event: MouseEvent): void {
        console.log('RectROISelector | updateSelection | event: ', event);

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

    public onMouseUp(event: MouseEvent): void {
        if (this.mouseDrag) {
            this.mouseDrag = false;
            if (this.checkSquareSelection()) {
                this.addCurrentSelection();
            } else {
                this.stateChange.emit(new SelectionStateMessage(this.currentSlice, true));
                this.clearSelectedArea();
                this.clearCanvasSelection();
                this.redrawSelections();
            }
        }
    }

    public redrawSelections(): void {
        this.clearCanvasSelection();

        this.drawSelections();
    }
}
