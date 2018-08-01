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
        CURRENT_SELECTION_COLOR: '#ff0000',
        OTHER_SELECTION_COLOR: '#256fde',
        ARCHIVED_SELECTION_COLOR: '#5f27e5'
    };

    private canvas: HTMLCanvasElement;
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
        }, (error: Error) => {
            console.error('Error while drawing brush selections!: ', error);
        });

    }

    drawSelections(): any {
        console.log('BrushSelector | drawSelections | selection: ', this.selections);
        this.getSelections().forEach((selection: BrushSelection) => {
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

    formArchivedSelections(selectionMap: Array<BrushSelection>): Array<BrushSelection> {
        selectionMap.forEach((selection: BrushSelection) => {
            this.drawSelection(selection, this.STYLE.ARCHIVED_SELECTION_COLOR);
            console.log('BrushSelector | scaleToView selection: ', selection);
        });
        return selectionMap;
    }

    onMouseDown(event: MouseEvent): boolean {
        console.log('BrushSelector | onMouseDown | event: ', event);

        const x = (event.clientX) - this.canvasPosition.left;
        const y = (event.clientY) - this.canvasPosition.top;

        this.mouseDrag = true;
        this.canvasCtx.lineWidth = this.STYLE.LINE_WIDTH;
        this.canvasCtx.lineJoin = this.STYLE.LINE_LINKS;
        this.canvasCtx.lineCap = this.STYLE.LINE_LINKS;
        this.canvasCtx.strokeStyle = this.STYLE.CURRENT_SELECTION_COLOR;

        this.canvasCtx.beginPath();
        this.canvasCtx.moveTo(x, y);

        return false;
    }

    onMouseMove(event: MouseEvent): boolean {
        if (this.mouseDrag) {
            console.log('BrushSelector | onMove | event: ', event);
            const x = (event.clientX) - this.canvasPosition.left;
            const y = (event.clientY) - this.canvasPosition.top;

            this.canvasCtx.lineTo(x, y);
            this.canvasCtx.stroke();
        }
        return false;
    }

    onMouseUp(event: MouseEvent): boolean {
        if (this.mouseDrag) {
            console.log('BrushSelector | onUp | event: ', event);
            this.mouseDrag = false;
            this.canvasCtx.closePath();

            // when canvas is cleared, we have only our brush selection in canvas
            const selectionImage: string = this.canvas.toDataURL();
            this.selectedArea = new BrushSelection(selectionImage, this.currentSlice);

            this.selections.set(this.currentSlice, [this.selectedArea]);

            this.stateChange.emit(new SelectionStateMessage(this.selectedArea.getId(), this.selectedArea.sliceIndex, false));
            this.selectedArea = undefined;
            return true;
        }
        return false;
    }

    getSelectorName(): string {
        return 'BRUSH';
    }
}
