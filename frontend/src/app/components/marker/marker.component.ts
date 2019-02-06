import { Component, Input, OnChanges, OnInit, SimpleChanges } from '@angular/core';
import { MatSnackBar } from '@angular/material';
import { LabelTag } from '../../model/labels/LabelTag';
import { SliceSelection } from '../../model/selections/SliceSelection';
import { ScanViewerComponent } from '../scan-viewer/scan-viewer.component';
import { Tool } from '../tools/Tool';
import { DrawingContext } from './../tools/DrawingContext';

@Component({
    selector: 'app-marker-component',
    templateUrl: './marker.component.html',
    styleUrls: ['./marker.component.scss']
})
export class MarkerComponent extends ScanViewerComponent implements OnInit, OnChanges {

    @Input() currentTool: Tool<SliceSelection>;

    @Input() currentTag: LabelTag;

    constructor(private snackBar: MatSnackBar) {
        super();
    }

    ngOnChanges(changes: SimpleChanges): void {
        super.ngOnChanges(changes);

        if (changes.currentTag) {
            this.refreshDrawingContext();
        }
    }

    ngOnInit() {
        console.log('MarkerComponent init');

        this.initializeImage(() => this.redrawSelections());
    }

    public onMouseDown(mouseEvent: MouseEvent): void {
        if (!this.currentTag) {
            this.snackBar.open('Please select Tag and Tool to start labeling.', '', {duration: 2000});
            return;
        } else if (!this.currentTool) {
            this.snackBar.open('Please select Tool to start labeling.', '', {duration: 2000});
            return;
        }

        this.currentTool.onMouseDown(mouseEvent);
    }

    public onMouseUp(mouseEvent: MouseEvent): void {
        console.log('Marker | initCanvasSelectionTool | onmouseup clientXY: ', mouseEvent.clientX, mouseEvent.clientY);
            if (this.currentTool) {
                this.currentTool.onMouseUp(mouseEvent);
            }
    }

    public onMouseMove(mouseEvent: MouseEvent): void {
        if (this.currentTool) {
            this.currentTool.onMouseMove(mouseEvent);
        }
    }

    public onWheel(wheelEvent: WheelEvent): void {
        wheelEvent.preventDefault();

        if (this.currentTool && !this.currentTool.canChangeSlice()) {
            return;
        }

        const newSliceIndex = wheelEvent.deltaY > 0 ? this.currentSlice - 1 : this.currentSlice + 1;

        this.changeSlice(newSliceIndex);
    }

    public canChangeSlice(): boolean {
        return this.currentTool ? this.currentTool.canChangeSlice() : true;
    }

    protected createDrawingContext(): DrawingContext {
        const drawingContext = super.createDrawingContext();
        drawingContext.currentTag = this.currentTag;
        return drawingContext;
    }
}
