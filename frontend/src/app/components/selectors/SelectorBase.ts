import {EventEmitter} from '@angular/core';
import {SliceSelection} from '../../model/SliceSelection';
import {SelectionStateMessage} from '../../model/SelectionStateMessage';
import {SelectorAction} from "../../model/SelectorAction";
import {Selector} from "./Selector";

export abstract class SelectorBase<CustomSliceSelection extends SliceSelection> {

    protected selectedArea: CustomSliceSelection;
    protected selections: Map<number, [CustomSliceSelection]>;
    protected archivedSelections: Array<CustomSliceSelection> = [];
    protected canvasCtx: CanvasRenderingContext2D;
    protected currentSlice;
    protected canvasPosition: ClientRect;
    protected canvasSize: { width: number, height: number };
    protected stateChange: EventEmitter<SelectionStateMessage>;
    protected redrawRequestEmitter: EventEmitter<void>;

    protected constructor(canvas: HTMLCanvasElement) {
        this.canvasCtx = canvas.getContext('2d');
        this.canvasSize = {
            width: canvas.width,
            height: canvas.height
        };
        this.stateChange = new EventEmitter<SelectionStateMessage>();
        this.selections = new Map<number, [CustomSliceSelection]>();
    }

    protected getStyle(): any {
        return {
            SELECTION_FONT_SIZE: 14,
            CURRENT_SELECTION_COLOR: '#ff0000',
            OTHER_SELECTION_COLOR: '#256fde',
            ARCHIVED_SELECTION_COLOR: '#5f27e5'
        };
    }

    public formArchivedSelections(selectionMap: CustomSliceSelection[]): CustomSliceSelection[] {
        selectionMap.forEach((selection: CustomSliceSelection) => {
            this.drawSelection(selection, this.getStyle().ARCHIVED_SELECTION_COLOR);
            console.log('Selector | scaleToView selection: ', selection);
        });
        return selectionMap;
    }

    public drawSelections(): void {
        console.log('RectROISelector | drawSelections | selection: ', this.selections);
        this.getSelections().forEach((selection: CustomSliceSelection) => {
            let color: string;
            const isCurrent: boolean = (selection.sliceIndex === this.currentSlice);
            if (isCurrent) {
                color = this.getStyle().CURRENT_SELECTION_COLOR;
            } else {
                color = this.getStyle().OTHER_SELECTION_COLOR;
            }
            if ((selection.pinned || isCurrent) && (!selection.hidden)) {
                this.drawSelection(selection, color);
            }
        });
        if (this.selectedArea) {
            this.drawSelection(this.selectedArea, this.getStyle().CURRENT_SELECTION_COLOR);
        }
    }

    protected isOnlyOneSelectionPerSlice(): boolean {
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

    protected addSelection(selection: CustomSliceSelection): void {
        console.log('Selector | addCurrentSelection');
        if (this.isOnlyOneSelectionPerSlice()) {
            this.removeSelectionsOnCurrentSlice();
            this.selections.set(this.currentSlice, [selection]);
        } else {
            const currentSliceSelections = this.selections.get(this.currentSlice);
            if (currentSliceSelections) {
                currentSliceSelections.push(selection);
            } else {
                this.selections.set(this.currentSlice, [selection]);
            }
        }
        this.stateChange.emit(new SelectionStateMessage(selection.getId(), selection.sliceIndex, false));
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

    protected normalizeByView(paramX: number, paramY: number): { x: number, y: number } {
        return {
            x: paramX / this.canvasSize.width,
            y: paramY / this.canvasSize.height
        };
    }

    protected scaleToView(paramX: number, paramY: number): { x: number, y: number } {
        return {
            x: paramX * this.canvasSize.width,
            y: paramY * this.canvasSize.height
        };
    }

    public abstract drawSelection(selection: CustomSliceSelection, color: string): any;

    public getActions(): Array<SelectorAction> {
        return [];
    }

    public setRedrawRequestEmitter(emitter: EventEmitter<void>): void {
        this.redrawRequestEmitter = emitter;
    }

    protected requestRedraw(): void {
        this.redrawRequestEmitter.emit();
    }
}

