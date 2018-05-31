import {EventEmitter} from '@angular/core';
import {SliceSelection} from '../../model/SliceSelection';
import {SelectionStateMessage} from '../../model/SelectionStateMessage';

export abstract class SelectorBase<CustomSliceSelection extends SliceSelection> {
    selectedArea: CustomSliceSelection;
    selections: Map<number, CustomSliceSelection>;
    archivedSelections: Array<CustomSliceSelection>;
    canvasCtx: CanvasRenderingContext2D;
    protected currentSlice;
    protected mouseDrag = false;
    protected canvasPosition: ClientRect;
    canvasSize: { width: number, height: number };

    public stateChange: EventEmitter<SelectionStateMessage>;

    public getStateChangeEmitter(): EventEmitter<SelectionStateMessage> {
        return this.stateChange;
    }

    public getSelections(): CustomSliceSelection[] {
        return Array.from(this.selections.values());
    }

    public clearData(): void {
        this.selectedArea = undefined;
        this.selections = new Map<number, CustomSliceSelection>();
        this.archivedSelections = [];
        this.stateChange = new EventEmitter<SelectionStateMessage>();
        this.clearCanvasSelection();
    }

    public clearCanvasSelection(): void {
        console.log('RectROISelector | clearCanvasSelection');
        this.canvasCtx.clearRect(0, 0, this.canvasSize.width, this.canvasSize.height);
    }

    public addCurrentSelection(): void {
        if (this.selectedArea) {
            console.log('RectROISelector | addCurrentSelection');
            this.selections.set(this.currentSlice, this.selectedArea);
            this.stateChange.emit(new SelectionStateMessage(this.currentSlice, false));
            this.clearSelectedArea();
        }
    }

    protected clearSelectedArea() {
        this.selectedArea = undefined;
    }

    public updateCurrentSlice(currentSliceId: number): void {
        this.currentSlice = currentSliceId;
    }

    public updateCanvasPosition(canvasRect: ClientRect) {
        this.canvasPosition = canvasRect;
    }

    public hasArchivedSelections(): boolean {
        return this.archivedSelections.length > 0;
    }

    public hasValidSelection(): boolean {
        return this.selections.size >= 1;
    }

    public hasSliceSelection(): boolean {
        return !!this.selections.get(this.currentSlice) || !!this.selectedArea;
    }

    public archiveSelections(selectionMap?: Array<CustomSliceSelection>): void {
        if (!selectionMap) {
            selectionMap = Array.from(this.selections.values());
        }
        selectionMap.forEach((value: CustomSliceSelection) => {
            this.archivedSelections.push(value);
        });
    }

    public removeCurrentSelection(): void {
        if (this.hasSliceSelection()) {
            this.selections.delete(this.currentSlice);

            this.selectedArea = undefined;
        }
    }

    public clearSelections() {
        this.selections.clear();
    }

    public updateCanvasHeight(height: number): void {
        if (height && height > 0) {
            this.canvasSize.height = height;
        } else {
            console.warn('RectROISelector | updateCanvasHeight - non numeric/positive height provided', height);
        }
    }

    public updateCanvasWidth(width: number): void {
        if (width && width > 0) {
            this.canvasSize.width = width;
        } else {
            console.warn('RectROISelector | updateCanvasWidth - non numeric/positive width provided', width);
        }
    }

    public removeSelection(selectionId: number): void {
        if (selectionId === this.currentSlice) {
            this.removeCurrentSelection();
        } else {
            this.selections.delete(selectionId);
            this.clearCanvasSelection();
        }
        this.redrawSelections();
    }

    public pinSelection(selectionId: number, newValue: boolean): void {
        const selection: CustomSliceSelection = this.selections.get(selectionId);
        if (selection) {
            if (selection.pinned !== newValue) {
                selection.pinned = newValue;
                this.redrawSelections();
            }
        } else {
            console.warn('RectROISelector | hideSelection | cannot pin non present selection!');
        }
    }

    public hideSelection(selectionId: number, newValue: boolean): void {
        const selection: SliceSelection = this.selections.get(selectionId);
        if (selection) {
            if (selection.hidden !== newValue) {
                selection.hidden = newValue;
                this.redrawSelections();
            }
        } else {
            console.warn('RectROISelector | hideSelection | cannot hide non present selection!');
        }
    }

    public normalizeByView(paramX: number, paramY: number): { x: number, y: number } {
        return {
            x: paramX / this.canvasSize.width,
            y: paramY / this.canvasSize.height
        };
    }

    public scaleToView(paramX: number, paramY: number): { x: number, y: number } {
        return {
            x: paramX * this.canvasSize.width,
            y: paramY * this.canvasSize.height
        };
    }

    abstract redrawSelections(): void;
}
