import { SliceSelection } from '../../model/selections/SliceSelection';
import { LabelTag } from './../../model/labels/LabelTag';
import { List } from 'immutable';

export class DrawingContext {

    public canvas: HTMLCanvasElement;
    public canvasCtx: CanvasRenderingContext2D;
    public canvasPosition: ClientRect;
    public canvasSize: { width: number, height: number };
    public selections: List<SliceSelection>;
    public currentSlice: number;
    public currentTag: LabelTag;
    public updateSelections: (selections: List<SliceSelection>) => void;

    public constructor(canvas: HTMLCanvasElement,
                       selections: List<SliceSelection>,
                       currentSlice: number,
                       currentTag: LabelTag,
                       updateSelections: (selections: List<SliceSelection>) => void) {

        this.canvas = canvas;
        this.canvasCtx = canvas.getContext('2d');
        this.canvasPosition = canvas.getBoundingClientRect();
        this.canvasSize = {
            width: canvas.width,
            height: canvas.height
        };
        this.selections = selections;
        this.currentSlice = currentSlice;
        this.currentTag = currentTag;
        this.updateSelections = updateSelections;
    }
}
