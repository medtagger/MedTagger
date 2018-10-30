import {ToolBase} from './ToolBase';
import {Tool} from './Tool';
import {BrushSelection} from '../../model/selections/BrushSelection';
import {SelectionStateMessage} from '../../model/SelectionStateMessage';
import {ToolAction, ToolActionType} from '../../model/ToolAction';

export enum BrushMode {
    BRUSH = 'Brush',
    ERASER = 'Eraser'
}

export class BrushTool extends ToolBase<BrushSelection> implements Tool<BrushSelection> {
    protected canvas: HTMLCanvasElement;
    protected mouseDrag = false;
    protected lastTagDrawings: Map<string, HTMLImageElement> = new Map<string, HTMLImageElement>();
    private mode: BrushMode = BrushMode.BRUSH;
    private actions: Array<ToolAction>;

    constructor(canvas: HTMLCanvasElement) {
        super(canvas);

        // Aye, we cannot get data url from context so....
        this.canvas = canvas;

        this.selectedArea = undefined;
        this.currentSlice = undefined;
        this.singleSelectionPerSlice = true;

        this.actions = [
            new ToolAction(BrushMode.BRUSH, () => true, () => {
                this.changeToolMode(BrushMode.BRUSH);
                this.deactivateOtherActions(BrushMode.BRUSH);
            }, ToolActionType.BUTTON, true),
            new ToolAction(BrushMode.ERASER, () => !!this.lastTagDrawings[this.getCurrentSelectingContext()], () => {
                this.changeToolMode(BrushMode.ERASER);
                this.deactivateOtherActions(BrushMode.ERASER);
            }, ToolActionType.BUTTON, false)
        ];
        console.log('BrushTool created!');
    }

    protected getStyle(): any {
        if (this.mode === BrushMode.BRUSH) {
            return {
                ...super.getStyle(),
                LINE_WIDTH: 10,
                LINE_LINKS: 'round',
                SELECTION_FONT_COLOR: '#ffffff',
                DRAWING_COMPOSITE_OPERATION: 'source-over',
                SAVING_COMPOSITE_OPERATION: 'source-over'
            };
        } else if (this.mode === BrushMode.ERASER) {
            return {
                ...super.getStyle(),
                LINE_WIDTH: 10,
                LINE_LINKS: 'square',
                CURRENT_SELECTION_COLOR: 'rgba(0,0,0,1)',
                ARCHIVED_SELECTION_COLOR: 'rgba(0,0,0,1)',
                DRAWING_COMPOSITE_OPERATION: 'destination-out',
                SAVING_COMPOSITE_OPERATION: 'source-over'
            };
        } else {
            console.error('Error: wrong tool mode: ', this.mode);
        }
    }

    public getActions(): Array<ToolAction> {
        return this.actions;
    }

    public deactivateOtherActions(currentAction: string): void {
        this.actions.forEach(action => {
            if (action.isActive !== undefined) {
                action.isActive = action.name === currentAction;
            }
        });
    }

    public changeToolMode(newMode: BrushMode): void {
        this.mode = newMode;
        this.deactivateOtherActions(newMode);
    }

    drawSelection(selection: BrushSelection, color: string): any {
        console.log('BrushTool | drawSelection | selection: ', selection);

        selection.getSelectionLayer().then((selectionLayerImage: HTMLImageElement) => {
            this.canvasCtx.drawImage(selectionLayerImage, 0, 0, this.canvasSize.width, this.canvasSize.height);

            // Recoloring of original selection
            if (selection.sliceIndex !== this.currentSlice) {
                this.canvasCtx.fillStyle = color;
                this.canvasCtx.globalCompositeOperation = 'source-in';
                this.canvasCtx.fillRect(0, 0, this.canvasSize.width, this.canvasSize.height);
                this.canvasCtx.globalCompositeOperation = 'source-over';
            }

        }, (error: Error) => {
            console.error('Error while drawing brush selections!: ', error);
        });

    }

    drawSelections(): any {
        console.log('BrushTool | drawSelections | selection: ', this.selections);

        const currentSelections: Array<BrushSelection> = [];

        this.getSelections().forEach((selection: BrushSelection) => {
            let color: string;
            const isCurrent: boolean = (selection.sliceIndex === this.currentSlice);
            if (isCurrent) {
                currentSelections.push(selection);
            } else {
                color = this.getStyle().OTHER_SELECTION_COLOR;
            }
            if ((selection.pinned) && (!selection.hidden)) {
                this.drawSelection(selection, color);
            }
        });

        if (currentSelections) {
            currentSelections.forEach((selection: BrushSelection) => {
                if (!selection.hidden) {
                    this.drawSelection(selection, this.getStyle().CURRENT_SELECTION_COLOR);
                }
            });
        }
    }

    formArchivedSelections(selectionMap: Array<BrushSelection>): Array<BrushSelection> {
        selectionMap.forEach((selection: BrushSelection) => {
            this.drawSelection(selection, this.getStyle().ARCHIVED_SELECTION_COLOR);
            console.log('BrushTool | scaleToView selection: ', selection);
        });
        return selectionMap;
    }

    onMouseDown(event: MouseEvent): void {
        console.log('BrushTool | onMouseDown | event: ', event);

        // starting new brush selection needs temporary canvas clear
        this.canvasCtx.clearRect(0, 0, this.canvasSize.width, this.canvasSize.height);

        const lastDrawing = this.lastTagDrawings[this.getCurrentSelectingContext()];

        if (!!lastDrawing) {
            this.canvasCtx.drawImage(lastDrawing, 0, 0,
                this.canvasSize.width, this.canvasSize.height);
        }

        const x = (event.clientX) - this.canvasPosition.left;
        const y = (event.clientY) - this.canvasPosition.top;

        this.mouseDrag = true;
        this.canvasCtx.lineWidth = this.getStyle().LINE_WIDTH;
        this.canvasCtx.lineJoin = this.getStyle().LINE_LINKS;
        this.canvasCtx.lineCap = this.getStyle().LINE_LINKS;
        this.canvasCtx.strokeStyle = this.getStyle().CURRENT_SELECTION_COLOR;
        this.canvasCtx.globalCompositeOperation = this.getStyle().DRAWING_COMPOSITE_OPERATION;

        this.canvasCtx.beginPath();
        this.canvasCtx.moveTo(x, y);
    }

    onMouseMove(event: MouseEvent): void {
        if (this.mouseDrag) {
            console.log('BrushTool | onMove | event: ', event);
            const x = (event.clientX) - this.canvasPosition.left;
            const y = (event.clientY) - this.canvasPosition.top;

            this.canvasCtx.lineTo(x, y);
            this.canvasCtx.stroke();
        }
    }

    onMouseUp(event: MouseEvent): void {
        if (this.mouseDrag) {
            console.log('BrushTool | onUp | event: ', event);
            const x = (event.clientX) - this.canvasPosition.left;
            const y = (event.clientY) - this.canvasPosition.top;

            this.canvasCtx.lineTo(x, y);
            this.canvasCtx.stroke();

            this.canvasCtx.globalCompositeOperation = this.getStyle().SAVING_COMPOSITE_OPERATION;

            this.mouseDrag = false;
            this.canvasCtx.closePath();

            // Get all brush selections on current slice
            const currentSliceSelections = this.selections.get(this.currentSlice);

            // Existing Brush selection index on current slice for given tag
            const existingSelectionIndex: number = this.getExistingSelectionIndex(currentSliceSelections);

            const selectionLabelId: number = existingSelectionIndex > -1
                ? currentSliceSelections[existingSelectionIndex].getId() // Modified selection will still use the same id
                : undefined; // New selection (for tag or at all), this will leave new generated id for new selection

            // When canvas is cleared, we have only our brush selection in canvas
            const selectionImageURL: string = this.canvas.toDataURL();

            console.log('BrushTool | onUp | SelectionLabelId: ', selectionLabelId);
            this.selectedArea = new BrushSelection(selectionImageURL, this.currentSlice, this.currentTag, selectionLabelId);

            const isSelectionErased: boolean = this.isCanvasBlank();

            // Note that currentSliceSelections is reference to this.selections
            if (currentSliceSelections && currentSliceSelections.length > 0) {
                if (isSelectionErased) {
                    // Remove selection when it is completely erased
                    currentSliceSelections.splice(existingSelectionIndex);
                } else {
                    // Update current selection by referencing new Selection object
                    currentSliceSelections[existingSelectionIndex] = this.selectedArea;
                }
            } else {
                // Without other brush selections we can simply set new selection for current slice
                this.selections.set(this.currentSlice, [this.selectedArea]);
            }

            if (isSelectionErased) {
                return this.finalizeSelectionRemoval(selectionLabelId);
            }

            return this.finalizeNewSelection();
        }
    }

    private getExistingSelectionIndex(currentSliceSelections: Array<BrushSelection>): number {
        if (currentSliceSelections) {
            return currentSliceSelections.findIndex(
                (selection: BrushSelection) => selection.label_tag === this.currentTag
            );
        }

        // First selection for that tag (or at all) for current slice
        return -1;
    }

    private finalizeSelectionRemoval(labelToDeleteId: number): void {
        console.log('BrushTool | inUp | blank selection, removing label...');
        this.stateChange.emit(new SelectionStateMessage(this.getToolName(), this.currentTag, labelToDeleteId,
            this.selectedArea.sliceIndex, true));

        this.clearSliceDrawingCacheOf(labelToDeleteId);
        this.selectedArea = undefined;
        this.requestRedraw();

        this.changeToolMode(BrushMode.BRUSH);
    }

    private finalizeNewSelection(): void {
        this.selectedArea.getSelectionLayer().then((image: HTMLImageElement) => {
            this.lastTagDrawings[this.getCurrentSelectingContext()] = image;

            this.stateChange.emit(new SelectionStateMessage(this.getToolName(), this.currentTag, this.selectedArea.getId(),
                this.selectedArea.sliceIndex, false));
            this.selectedArea = undefined;
            this.requestRedraw();
        });
    }

    public updateCurrentSlice(currentSliceId: number): any {
        super.updateCurrentSlice(currentSliceId);

        this.returnToBrushModeIfNeeded();
    }

    public updateBrushSelection(sliceIndex: number, tag_key: string, source: string): void {
        this.getSelections().forEach((selection: BrushSelection) => {
            if (selection.sliceIndex === sliceIndex && selection.label_tag.key === tag_key) {
                selection._selectionLayer.src = source;
                this.lastTagDrawings[selection.label_tag.key + selection.sliceIndex] = selection._selectionLayer;
            }
        });
    }

    // Changing mode to avoid situation when we are in eraser mode on slice that lacks brush selection
    private returnToBrushModeIfNeeded(): void {
        const hasDrawing: boolean = this.lastTagDrawings[this.getCurrentSelectingContext()] !== undefined;
        if (this.mode === BrushMode.ERASER && !hasDrawing) {
            this.changeToolMode(BrushMode.BRUSH);
        }
    }

    // To differentiate selections by tags and slices
    private getCurrentSelectingContext(): string {
        if (this.currentTag && this.currentSlice) {
            return this.currentTag.key + this.currentSlice;
        } else {
            return '';
        }
    }

    public removeSelection(selectionId: number): boolean {
        this.clearSliceDrawingCacheOf(selectionId);
        this.changeToolMode(BrushMode.BRUSH);
        this.returnToBrushModeIfNeeded();

        return super.removeSelection(selectionId);
    }

    private clearSliceDrawingCacheOf(selectionId: number): void {
        const selectionToDelete = this.getSelections().find(selection => selection.getId() === selectionId);
        if (!!selectionToDelete) {
            this.lastTagDrawings[selectionToDelete.label_tag.key + selectionToDelete.sliceIndex] = undefined;
        } else {
            console.warn('BrushTool | clearSliceDrawingCacheOf | no selection to delete!');
        }
    }

    // Checking if canvas is blank without iterating through pixels of canvas
    private isCanvasBlank(): boolean {
        const blankCanvas: HTMLCanvasElement = document.createElement('canvas');
        blankCanvas.width = this.canvas.width;
        blankCanvas.height = this.canvas.height;

        return this.canvas.toDataURL() === blankCanvas.toDataURL();
    }

    public canUseMouseWheel(): boolean {
        return !this.mouseDrag;
    }

    public getToolName(): string {
        return 'BRUSH';
    }
}
