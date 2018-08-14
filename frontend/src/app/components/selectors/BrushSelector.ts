import {SelectorBase} from './SelectorBase';
import {Selector} from './Selector';
import {BrushSelection} from '../../model/selections/BrushSelection';
import {SelectionStateMessage} from '../../model/SelectionStateMessage';
import {SelectorAction} from '../../model/SelectorAction';

export enum BrushMode {
    BRUSH = 'Brush',
    ERASER = 'Eraser'
}

export class BrushSelector extends SelectorBase<BrushSelection> implements Selector<BrushSelection> {
    protected canvas: HTMLCanvasElement;
    protected mouseDrag = false;
    protected lastTagDrawings: Map<string, HTMLImageElement> = new Map<string, HTMLImageElement>();
    private mode: BrushMode = BrushMode.BRUSH;
    private actions: Array<SelectorAction>;

    constructor(canvas: HTMLCanvasElement) {
        super(canvas);

        // Aye, we cannot get data url from context so....
        this.canvas = canvas;

        this.selectedArea = undefined;
        this.currentSlice = undefined;
        this.singleSelectionPerSlice = true;

        this.actions = [
            new SelectorAction(BrushMode.ERASER, () => !!this.lastTagDrawings[this.getSelectingContext()], () => {
                this.changeSelectorMode(BrushMode.ERASER);
                this.deactivateOtherActions(BrushMode.ERASER);
            }, false),
            new SelectorAction(BrushMode.BRUSH, () => true, () => {
                this.changeSelectorMode(BrushMode.BRUSH);
                this.deactivateOtherActions(BrushMode.BRUSH);
            }, true)
        ];
        console.log('BrushSelector created!');
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
                OTHER_SELECTION_COLOR: 'rgba(0,0,0,1)',
                ARCHIVED_SELECTION_COLOR: 'rgba(0,0,0,1)',
                DRAWING_COMPOSITE_OPERATION: 'destination-out',
                SAVING_COMPOSITE_OPERATION: 'source-over'
            };
        } else {
            console.error('Error: wrong selector mode: ', this.mode);
        }
    }

    public getActions(): Array<SelectorAction> {
        return this.actions;
    }

    public deactivateOtherActions(currentAction: string): void {
        this.actions.forEach(action => {
            if (action.isActive !== undefined) {
                action.isActive = action.name === currentAction;
            }
        });
    }

    public changeSelectorMode(newMode: BrushMode): void {
        this.mode = newMode;
    }

    drawSelection(selection: BrushSelection, color: string): any {
        console.log('BrushSelector | drawSelection | selection: ', selection);

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
        console.log('BrushSelector | drawSelections | selection: ', this.selections);

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
            console.log('BrushSelector | scaleToView selection: ', selection);
        });
        return selectionMap;
    }

    onMouseDown(event: MouseEvent): void {
        console.log('BrushSelector | onMouseDown | event: ', event);

        // starting new brush selection needs temporary canvas clear
        this.canvasCtx.clearRect(0, 0, this.canvasSize.width, this.canvasSize.height);

        const lastDrawing = this.lastTagDrawings[this.getSelectingContext()];

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
            console.log('BrushSelector | onMove | event: ', event);
            const x = (event.clientX) - this.canvasPosition.left;
            const y = (event.clientY) - this.canvasPosition.top;

            this.canvasCtx.lineTo(x, y);
            this.canvasCtx.stroke();
        }
    }

    onMouseUp(event: MouseEvent): void {
        if (this.mouseDrag) {
            console.log('BrushSelector | onUp | event: ', event);

            this.canvasCtx.globalCompositeOperation = this.getStyle().SAVING_COMPOSITE_OPERATION;

            this.mouseDrag = false;
            this.canvasCtx.closePath();

            // when canvas is cleared, we have only our brush selection in canvas
            const selectionImageURL: string = this.canvas.toDataURL();
            this.selectedArea = new BrushSelection(selectionImageURL, this.currentSlice, this.currentTag.name);

            this.selectedArea.getSelectionLayer().then((image: HTMLImageElement) => {
                this.lastTagDrawings[this.getSelectingContext()] = image;

                const currentSliceSelections = this.selections.get(this.currentSlice);

                if (currentSliceSelections) {
                    const labelTagSelectionIndex: number = currentSliceSelections.findIndex(
                        (selection: BrushSelection) => selection.label_tag === this.currentTag.name
                    );

                    if (labelTagSelectionIndex > -1) {
                        currentSliceSelections[labelTagSelectionIndex] = this.selectedArea;
                    } else {
                        currentSliceSelections.push(this.selectedArea);
                    }
                } else {
                    this.selections.set(this.currentSlice, [this.selectedArea]);
                }

                this.stateChange.emit(new SelectionStateMessage(this.selectedArea.getId(), this.selectedArea.sliceIndex, false));
                this.selectedArea = undefined;
                this.requestRedraw();
            });
        }
    }

    public updateCurrentSlice(currentSliceId: number): any {
        super.updateCurrentSlice(currentSliceId);

        // Changing mode to avoid situation when we are in eraser mode on slice that lacks brush selection
        if (this.mode === BrushMode.ERASER && !this.lastTagDrawings[this.getSelectingContext()]) {
            this.changeSelectorMode(BrushMode.BRUSH);
            this.deactivateOtherActions(BrushMode.BRUSH);
        }
    }

    // To differentiate selections by tags and slices
    private getSelectingContext(): string {
        return this.currentTag.name + this.currentSlice;
    }

    getSelectorName(): string {
        return 'BRUSH';
    }
}
