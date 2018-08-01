import {BrushSelector} from './BrushSelector';
import {BrushSelection} from '../../model/selections/BrushSelection';
import {Selector} from './Selector';

export class EraserSelector extends BrushSelector implements Selector<BrushSelection> {
    protected getStyle(): any {
        return {
            ...super.getStyle(),
            LINE_WIDTH: 10,
            LINE_LINKS: 'square',
            CURRENT_SELECTION_COLOR: 'rgba(0,0,0,1)',
            OTHER_SELECTION_COLOR: 'rgba(0,0,0,1)',
            ARCHIVED_SELECTION_COLOR: 'rgba(0,0,0,1)',
            GLOBAL_COMPOSITE_OPERATION: 'destination-out'
        };
    }

    constructor(canvas: HTMLCanvasElement) {
        super(canvas);

        // Aye, we cannot get data url from context so....
        this.canvas = canvas;

        this.selectedArea = undefined;
        this.currentSlice = undefined;
        this.singleSelectionPerSlice = true;

        console.log('EraserSelector created!');
    }

    onMouseUp(event: MouseEvent): boolean {
        super.onMouseUp(event);

        return false;
    }

    getSelectorName(): string {
        return 'ERASER';
    }
}
