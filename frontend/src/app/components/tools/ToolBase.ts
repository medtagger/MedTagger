import { List } from 'immutable';
import { LabelTag } from '../../model/labels/LabelTag';
import { SliceSelection } from '../../model/selections/SliceSelection';
import { ToolAction } from '../../model/ToolAction';
import { DrawingContext } from './DrawingContext';
import { Tool } from './Tool';

export abstract class ToolBase<CustomSliceSelection extends SliceSelection> implements Tool<CustomSliceSelection> {

    protected drawingContext: DrawingContext;

    public setDrawingContext(drawingContext: DrawingContext): void {
        this.drawingContext = drawingContext;
    }

    protected getStyle(): any {
        return {
            SELECTION_FONT_SIZE: 14,
            CURRENT_SELECTION_COLOR: '#ff0000',
            OTHER_SELECTION_COLOR: '#256fde',
            ARCHIVED_SELECTION_COLOR: '#5f27e5'
        };
    }

    protected normalizeByView(paramX: number, paramY: number): { x: number, y: number } {
        return {
            x: paramX / this.drawingContext.canvasSize.width,
            y: paramY / this.drawingContext.canvasSize.height
        };
    }

    protected scaleToView(paramX: number, paramY: number): { x: number, y: number } {
        return {
            x: paramX * this.drawingContext.canvasSize.width,
            y: paramY * this.drawingContext.canvasSize.height
        };
    }

    public getActions(): Array<ToolAction> {
        return [];
    }

    public canChangeSlice(): boolean {
        return true;
    }

    public abstract drawSelection(selection: CustomSliceSelection): any;

    public abstract getToolName(): string;

    public abstract onMouseDown(event: MouseEvent): void;

    public abstract onMouseMove(event: MouseEvent): void;

    public abstract onMouseUp(event: MouseEvent): void;

    protected getOwnSelectionsOnCurrentSlice(): List<CustomSliceSelection> {
        return this.getOwnSelections().filter(x => x.sliceIndex === this.currentSlice);
    }

    protected getOwnSelections(): List<CustomSliceSelection> {
        return this.selections.filter(x => x.labelTool === this.getToolName()) as List<CustomSliceSelection>;
    }

    protected getColorForSelection(selection: SliceSelection): string {
        const isOnCurrentSlice = selection.sliceIndex === this.currentSlice;
        return isOnCurrentSlice ? this.getStyle().CURRENT_SELECTION_COLOR : this.getStyle().OTHER_SELECTION_COLOR;
    }

    protected addSelection(selection: SliceSelection): void {
        this.drawingContext.updateSelections(this.selections.push(selection));
    }

    protected removeSelection(selection: SliceSelection): void {
        const selectionIndexToDelete = this.selections.findIndex(x => x === selection);
        this.drawingContext.updateSelections(this.selections.splice(selectionIndexToDelete, 1));
    }

    protected updateSelection<T extends SliceSelection>(selection: T): T {
        const selectionIndexToReplace = this.selections.findIndex(x => x.getId() === selection.getId());
        // objects must not be reference equal to detect change
        if (selection === this.selections.get(selectionIndexToReplace)) {
            selection = Object.create(selection);
        }
        this.drawingContext.updateSelections(this.selections.set(selectionIndexToReplace, selection));
        return selection;
    }

    protected get canvas(): HTMLCanvasElement {
        return this.drawingContext.canvas;
    }

    protected get canvasCtx(): CanvasRenderingContext2D {
        return this.drawingContext.canvasCtx;
    }

    protected get currentSlice(): number {
        return this.drawingContext.currentSlice;
    }

    protected get currentTag(): LabelTag {
        return this.drawingContext.currentTag;
    }

    protected get canvasPosition(): ClientRect {
        return this.drawingContext.canvasPosition;
    }

    protected get canvasSize(): { width: number, height: number } {
        return this.drawingContext.canvasSize;
    }

    protected get selections(): List<SliceSelection> {
        return this.drawingContext.selections;
    }
}

