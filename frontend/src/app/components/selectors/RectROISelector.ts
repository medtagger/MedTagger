import {ROISelection2D} from '../../model/ROISelection2D';
import {EventEmitter} from '@angular/core';
import {SelectorBase} from './SelectorBase';
import {SelectionStateMessage} from '../../model/SelectionStateMessage';
import {Selector} from './Selector';
import {SliceSelection} from '../../model/SliceSelection';

export class RectROISelector extends SelectorBase<ROISelection2D> implements Selector<ROISelection2D> {
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
        this.selections = new Map<number, [ROISelection2D]>();
        this.selectedArea = undefined;
        this.currentSlice = undefined;
        this.currentTag = undefined;
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
        this.getSelections().forEach((selection: ROISelection2D) => {
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
        if (this.selectedArea) {
            this.drawSelection(this.selectedArea, this.STYLE.CURRENT_SELECTION_COLOR);
        }
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
        this.canvasCtx.textAlign = 'start';
        this.canvasCtx.fillText(selection.getId().toString(), scaledStartPoint.x + (fontSize / 4), scaledStartPoint.y + fontSize);
    }

    public onMouseDown(event: MouseEvent): boolean {
        console.log('RectROISelector | startMouseSelection | event: ', event);
        const selectionStartX = (event.clientX) - this.canvasPosition.left;
        const selectionStartY = (event.clientY) - this.canvasPosition.top;

        const normalizedPoint: { x: number, y: number } = this.normalizeByView(selectionStartX, selectionStartY);

        this.selectedArea = new ROISelection2D(normalizedPoint.x, normalizedPoint.y, this.currentSlice, this.currentTag.key);
        if (this.isOnlyOneSelectionPerSlice() && this.selections.get(this.currentSlice)) {
            this.selections.get(this.currentSlice).forEach((selection: SliceSelection) => this.stateChange.emit(
                new SelectionStateMessage(selection.getId(), selection.sliceIndex, true)));
            this.selections.delete(this.currentSlice);
        }
        this.mouseDrag = true;
        return true;
    }

    public onMouseMove(mouseEvent: MouseEvent): boolean {
        if (this.mouseDrag && this.selectedArea) {
            console.log('RectROISelector | drawSelectionRectangle | onmousemove clienXY: ', mouseEvent.clientX, mouseEvent.clientY);
            this.updateSelection(mouseEvent);
            return true;
        }
        return false;
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

    public onMouseUp(event: MouseEvent): boolean {
        if (this.mouseDrag) {
            this.mouseDrag = false;
            if (this.checkSquareSelection()) {
                this.addCurrentSelection();
            } else {
                this.clearSelectedArea();
            }
            return true;
        }
        return false;
    }

    public getSelectorName(): string {
        return 'RECTANGLE';
    }
}
