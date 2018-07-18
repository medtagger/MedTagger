import {EventEmitter} from '@angular/core';
import {SliceSelection} from '../../model/SliceSelection';
import {SelectionStateMessage} from '../../model/SelectionStateMessage';

export abstract class SelectorBase<CustomSliceSelection extends SliceSelection> {
    selectedArea: CustomSliceSelection;
    selections: Map<number, [CustomSliceSelection]>;
    archivedSelections: Array<CustomSliceSelection> = [];
    canvasCtx: CanvasRenderingContext2D;
    protected currentSlice;
    protected currentTag;
    protected mouseDrag = false;
    protected canvasPosition: ClientRect;
    canvasSize: { width: number, height: number };

    public stateChange: EventEmitter<SelectionStateMessage>;

    public isOnlyOneSelectionPerSlice(): boolean {
        return false;
    }

    public getStateChangeEmitter(): EventEmitter<SelectionStateMessage> {
        return this.stateChange;
    }

    public getSelections(): CustomSliceSelection[] {
        return Array.from(this.selections.values()).reduce((x, y) => x.concat(y), []);
    }

    public clearData(): void {
        this.selectedArea = undefined;
        this.selections = new Map<number, [CustomSliceSelection]>();
        this.archivedSelections = [];
        this.stateChange = new EventEmitter<SelectionStateMessage>();
    }

    public addCurrentSelection(): void {
        if (this.selectedArea) {
            console.log('RectROISelector | addCurrentSelection');
            if (this.isOnlyOneSelectionPerSlice()) {
                this.selections.set(this.currentSlice, [this.selectedArea]);
            } else {
                const currentSliceSelections = this.selections.get(this.currentSlice);
                if (currentSliceSelections) {
                    currentSliceSelections.push(this.selectedArea);
                } else {
                    this.selections.set(this.currentSlice, [this.selectedArea]);
                }
            }
            this.stateChange.emit(new SelectionStateMessage(this.selectedArea.getId(), this.selectedArea.sliceIndex, false));
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
            selectionMap = this.getSelections();
        }
        selectionMap.forEach((value: CustomSliceSelection) => {
            this.archivedSelections.push(value);
        });
    }

    public removeSelectionsOnCurrentSlice(): void {
        const selectionsOnCurrentSlice = this.selections.get(this.currentSlice);
        if (selectionsOnCurrentSlice) {
            selectionsOnCurrentSlice.forEach((selection) => this.stateChange.emit(
                new SelectionStateMessage(selection.getId(), selection.sliceIndex, true)));
            this.selections.delete(this.currentSlice);
        }

        this.selectedArea = undefined;
    }

    public removeSelectionsOnSlice(sliceId: number): void {
        const selectionsOnSlice = this.selections.get(sliceId);
        if (selectionsOnSlice) {
            selectionsOnSlice.forEach((selection) => this.stateChange.emit(
                new SelectionStateMessage(selection.getId(), selection.sliceIndex, true)));
            this.selections.delete(sliceId);
        }

        if (sliceId === this.currentSlice) {
            this.selectedArea = undefined;
        }
    }

    public clearSelections() {
        this.getSelections().forEach((selection) => this.stateChange.emit(
            new SelectionStateMessage(selection.getId(), selection.sliceIndex, true)));
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

    public removeSelection(selectionId: number): boolean {
        return this.findAndModifySelection(selectionId, (selections, index) => selections.splice(index, 1));
    }

    public pinSelection(selectionId: number, newValue: boolean): boolean {
        return this.findAndModifySelection(selectionId, (selections, index) => selections[index].pinned = newValue);
    }

    public hideSelection(selectionId: number, newValue: boolean): boolean {
         return this.findAndModifySelection(selectionId, (selections, index) => selections[index].hidden = newValue);
    }

    private findAndModifySelection(selectionId: number, modifyFunc: (selections: [CustomSliceSelection], index: number) => void): boolean {
        for (const selectionsBySlice of Array.from(this.selections.values())) {
            const index = selectionsBySlice.findIndex((selection) => selection.getId() === selectionId);
            if (index !== -1) {
                modifyFunc(selectionsBySlice, index);
                return true;
            }
        }
        return false;
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
}
