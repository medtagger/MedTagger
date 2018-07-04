import {ROISelection2D} from '../../model/ROISelection2D';
import {Selector} from './Selector';
import {RectROISelector} from './RectROISelector';

export class CircleROISelector extends RectROISelector implements Selector<ROISelection2D> {
    constructor(canvas: HTMLCanvasElement) {
        super(canvas);
    }

    public drawSelection(selection: ROISelection2D, color: string): void {
        console.log('CircleROISelector | drawSelection | selection: ', selection);
        this.canvasCtx.strokeStyle = color;
        this.canvasCtx.setLineDash(this.STYLE.SELECTION_LINE_DENSITY);
        this.canvasCtx.beginPath();
        this.canvasCtx.arc(((selection.width / 2) + selection.positionX),
            ((selection.height / 2) + selection.positionY), (selection.width / 2), 0, 2 * Math.PI);
        this.canvasCtx.stroke();
        const fontSize = this.STYLE.SELECTION_FONT_SIZE;
        this.canvasCtx.font = `${fontSize}px Arial`;
        this.canvasCtx.fillStyle = color;
        this.canvasCtx.textAlign = 'start';
        this.canvasCtx.fillText(selection.getId().toString(), selection.positionX + (fontSize / 4), selection.positionY + fontSize);
    }

    public getSelectorName(): string {
        return 'CIRCLE';
    }
}
