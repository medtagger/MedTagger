import { Component, Input, OnChanges, OnInit, SimpleChanges, Output, EventEmitter, ChangeDetectorRef } from '@angular/core';
import { MatSnackBar } from '@angular/material';
import { LabelTag } from '../../model/labels/LabelTag';
import { SliceSelection } from '../../model/selections/SliceSelection';
import { ScanViewerComponent } from '../scan-viewer/scan-viewer.component';
import { Tool } from '../tools/Tool';
import { DrawingContext } from './../tools/DrawingContext';
import { List } from 'immutable';
import { TranslateService } from '@ngx-translate/core';

@Component({
    selector: 'app-marker-component',
    templateUrl: './marker.component.html',
    styleUrls: ['./marker.component.scss']
})
export class MarkerComponent extends ScanViewerComponent implements OnInit, OnChanges {

    @Input() currentTool: Tool<SliceSelection>;

    @Input() currentTag: LabelTag;

    @Output() selectionsChange: EventEmitter<List<SliceSelection>> = new EventEmitter();

    constructor(private snackBar: MatSnackBar, private translateService: TranslateService) {
        super();
    }

    ngOnChanges(changes: SimpleChanges): void {
        super.ngOnChanges(changes);

        if (changes.currentTag) {
            this.refreshDrawingContext();
        }

        if (changes.currentTool && changes.currentTool.previousValue) {
            // timeout is needed to avoid ExpressionChangedAfterItHasBeenCheckedError
            setTimeout(() => {
                changes.currentTool.previousValue.reset();
                this.redrawSelections();
            });
        }
    }

    ngOnInit() {
        console.log('MarkerComponent init');

        this.initializeImage(() => this.redrawSelections());
    }

    public onMouseDown(mouseEvent: MouseEvent): void {
        if (!this.currentTag) {
            this.snackBar.open(this.translateService.instant('COMPONENT.MARKER.MESSAGE.SELECT_TAG'), '', { duration: 2000 });
            return;
        } else if (!this.currentTool) {
            this.snackBar.open(this.translateService.instant('COMPONENT.MARKER.MESSAGE.SELECT_TOOL'), '', { duration: 2000 });
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
        drawingContext.updateSelections = this.updateSelections.bind(this);
        return drawingContext;
    }

    private updateSelections(selections: List<SliceSelection>) {
        this.drawingContext.selections = selections;
        this.selectionsChange.emit(selections);
    }
}
