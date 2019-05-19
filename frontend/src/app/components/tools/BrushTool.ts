import { BrushSelection } from '../../model/selections/BrushSelection';
import { ToolAction, ToolActionType } from '../../model/ToolAction';
import { SliceSelectionType } from './../../model/selections/SliceSelection';
import { Tool } from './Tool';
import { ToolBase } from './ToolBase';

export enum BrushMode {
    BRUSH = 'Brush',
    ERASER = 'Eraser'
}

export class BrushTool extends ToolBase<BrushSelection> implements Tool<BrushSelection> {
    private mouseDrag = false;
    private mode: BrushMode = BrushMode.BRUSH;
    private readonly actions: Array<ToolAction>;

    constructor() {
        super();

        this.actions = [
            new ToolAction(
                'BRUSH.BRUSH',
                () => true,
                () => {
                    this.changeToolMode(BrushMode.BRUSH);
                },
                ToolActionType.BUTTON,
                true
            ),
            new ToolAction(
                'BRUSH.ERASER',
                () => !!this.getCurrentBrushSelection(),
                () => {
                    this.changeToolMode(BrushMode.ERASER);
                },
                ToolActionType.BUTTON,
                false
            )
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

    public reset(): void {
        this.mouseDrag = false;
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

    public drawSelection(selection: BrushSelection): any {
        console.log('BrushTool | drawSelection | selection: ', selection);

        const color = this.getColorForSelection(selection);
        selection.getSelectionLayer().then(
            (selectionLayerImage: HTMLImageElement) => {
                this.canvasCtx.drawImage(selectionLayerImage, 0, 0, this.canvasSize.width, this.canvasSize.height);

                // Recoloring of original selection
                if (selection.sliceIndex !== this.currentSlice) {
                    this.canvasCtx.fillStyle = color;
                    this.canvasCtx.globalCompositeOperation = 'source-in';
                    this.canvasCtx.fillRect(0, 0, this.canvasSize.width, this.canvasSize.height);
                    this.canvasCtx.globalCompositeOperation = 'source-over';
                }
            },
            (error: Error) => {
                console.error('Error while drawing brush selections!: ', error);
            }
        );
    }

    public onMouseDown(event: MouseEvent): void {
        console.log('BrushTool | onMouseDown | event: ', event);

        // starting new brush selection needs temporary canvas clear
        this.canvasCtx.clearRect(0, 0, this.canvasSize.width, this.canvasSize.height);

        const currentSelection = this.getCurrentBrushSelection();

        if (currentSelection) {
            this.canvasCtx.drawImage(currentSelection.selectionLayer, 0, 0, this.canvasSize.width, this.canvasSize.height);
        }

        const x = event.clientX - this.canvasPosition.left;
        const y = event.clientY - this.canvasPosition.top;

        this.mouseDrag = true;
        this.canvasCtx.lineWidth = this.getStyle().LINE_WIDTH;
        this.canvasCtx.lineJoin = this.getStyle().LINE_LINKS;
        this.canvasCtx.lineCap = this.getStyle().LINE_LINKS;
        this.canvasCtx.strokeStyle = this.getStyle().CURRENT_SELECTION_COLOR;
        this.canvasCtx.globalCompositeOperation = this.getStyle().DRAWING_COMPOSITE_OPERATION;

        this.canvasCtx.beginPath();
        this.canvasCtx.moveTo(x, y);
        this.canvasCtx.lineTo(x, y);
        this.canvasCtx.stroke();
    }

    public onMouseMove(event: MouseEvent): void {
        if (this.mouseDrag) {
            console.log('BrushTool | onMove | event: ', event);
            const x = event.clientX - this.canvasPosition.left;
            const y = event.clientY - this.canvasPosition.top;

            this.canvasCtx.lineTo(x, y);
            this.canvasCtx.stroke();
        }
    }

    public onMouseUp(event: MouseEvent): void {
        if (this.mouseDrag) {
            console.log('BrushTool | onUp | event: ', event);
            this.canvasCtx.globalCompositeOperation = this.getStyle().SAVING_COMPOSITE_OPERATION;
            this.canvasCtx.closePath();
            this.mouseDrag = false;

            const currentSelection = this.getCurrentBrushSelection();

            if (this.isCanvasBlank()) {
                if (currentSelection) {
                    this.removeSelection(currentSelection);
                    this.changeToolMode(BrushMode.BRUSH);
                }
            } else {
                // When canvas is cleared, we have only our brush selection in canvas
                const image: string = this.canvas.toDataURL();

                if (currentSelection) {
                    currentSelection.setImage(image);
                    currentSelection.isReady.then(() => {
                        this.redraw();
                    });
                } else {
                    const newSelections = new BrushSelection(image, this.currentSlice, this.currentTag, SliceSelectionType.NORMAL);
                    newSelections.isReady.then(() => {
                        this.addSelection(newSelections);
                    });
                }
            }
        }
    }

    // Checking if canvas is blank without iterating through pixels of canvas
    private isCanvasBlank(): boolean {
        const blankCanvas: HTMLCanvasElement = document.createElement('canvas');
        blankCanvas.width = this.canvas.width;
        blankCanvas.height = this.canvas.height;

        return this.canvas.toDataURL() === blankCanvas.toDataURL();
    }

    public canChangeSlice(): boolean {
        return !this.mouseDrag;
    }

    public getToolName(): string {
        return 'BRUSH';
    }

    private getCurrentBrushSelection(): BrushSelection {
        return this.selections.find(
            selection =>
                selection.labelTool === this.getToolName() &&
                selection.sliceIndex === this.currentSlice &&
                selection.labelTag === this.currentTag
        ) as BrushSelection;
    }

    private addCurrentBrushSelection(): void {
        console.log('Add brush selection');
        this.actions[2].isActive = false;
    }
}
