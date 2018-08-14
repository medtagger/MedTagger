import {SelectorBase} from './SelectorBase';
import {Selector} from './Selector';
import {BrushSelection} from '../../model/selections/BrushSelection';
import {SelectionStateMessage} from '../../model/SelectionStateMessage';

export class BrushSelector extends SelectorBase<BrushSelection> implements Selector<BrushSelection> {
    readonly STYLE = {
        LINE_WIDTH: 10,
        LINE_LINKS: 'round',
        SELECTION_FONT_SIZE: 14,
        SELECTION_FONT_COLOR: '#ffffff',
        CURRENT_SELECTION_COLOR: 'rgba(255, 0, 0, 1)',
        OTHER_SELECTION_COLOR: 'rgba(37, 111, 222, 1)',
        ARCHIVED_SELECTION_COLOR: '#5f27e5'
    };

    private canvas: HTMLCanvasElement;
    private lastTagDrawings: Map<string, HTMLImageElement> = new Map<string, HTMLImageElement>();
    private mouseDrag = false;

    constructor(canvas: HTMLCanvasElement) {
        super(canvas);

        // Aye, we cannot get data url from context so....
        this.canvas = canvas;

        this.selectedArea = undefined;
        this.currentSlice = undefined;
        this.singleSelectionPerSlice = true;
        console.log('BrushSelector created!');
    }

    drawSelection(selection: BrushSelection, color: string): any {
        console.log('BrushSelector | drawSelection | selection: ', selection);

        selection.getSelectionLayer().then((selectionLayerImage: HTMLImageElement) => {
            this.canvasCtx.drawImage(selectionLayerImage, 0, 0, this.canvasSize.width, this.canvasSize.height);

            // Recoloring of original selection
            if (color === this.STYLE.OTHER_SELECTION_COLOR) {
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

        let currentSelection: BrushSelection;

        this.getSelections().forEach((selection: BrushSelection) => {
            let color: string;
            const isCurrent: boolean = (selection.sliceIndex === this.currentSlice);
            if (isCurrent) {
                currentSelection = selection;
            } else {
                color = this.STYLE.OTHER_SELECTION_COLOR;
            }
            if ((selection.pinned) && (!selection.hidden)) {
                this.drawSelection(selection, color);
            }
        });

        if (currentSelection) {
            this.drawSelection(currentSelection, this.STYLE.CURRENT_SELECTION_COLOR);
        }
    }

    formArchivedSelections(selectionMap: Array<BrushSelection>): Array<BrushSelection> {
        selectionMap.forEach((selection: BrushSelection) => {
            this.drawSelection(selection, this.STYLE.ARCHIVED_SELECTION_COLOR);
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
        this.canvasCtx.lineWidth = this.STYLE.LINE_WIDTH;
        this.canvasCtx.lineJoin = this.STYLE.LINE_LINKS;
        this.canvasCtx.lineCap = this.STYLE.LINE_LINKS;
        this.canvasCtx.strokeStyle = this.STYLE.CURRENT_SELECTION_COLOR;

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

    // To differentiate selections by tags and slices
    private getSelectingContext(): string {
        return this.currentTag.name + this.currentSlice;
    }

    getSelectorName(): string {
        return 'BRUSH';
    }
}
