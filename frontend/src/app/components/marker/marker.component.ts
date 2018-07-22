import {Component, ElementRef, EventEmitter, OnInit, ViewChild} from '@angular/core';
import {MarkerSlice} from '../../model/MarkerSlice';
import {MatSlider} from '@angular/material/slider';
import {Subject} from 'rxjs';
import {ScanViewerComponent} from '../scan-viewer/scan-viewer.component';
import {SliceSelection} from '../../model/SliceSelection';
import {SliceRequest} from '../../model/SliceRequest';
import {LabelExplorerComponent} from '../label-explorer/label-explorer.component';
import {LabelListItem} from '../../model/LabelListItem';
import {SelectionStateMessage} from '../../model/SelectionStateMessage';
import {Selector} from '../selectors/Selector';
import {Subscription} from 'rxjs/Subscription';

@Component({
    selector: 'app-marker-component',
    templateUrl: './marker.component.html',
    styleUrls: ['./marker.component.scss']
})
export class MarkerComponent extends ScanViewerComponent implements OnInit {

    currentImage: HTMLImageElement;
    downloadingScanInProgress = false;
    downloadingSlicesInProgress = false;
    redrawRequestEmitter: EventEmitter<void> = new EventEmitter<void>();

    @ViewChild('image')
    set viewImage(viewElement: ElementRef) {
        this.currentImage = viewElement.nativeElement;
    }

    canvas: HTMLCanvasElement;

    private currentSelector: Selector<SliceSelection>;

    @ViewChild('canvas')
    set viewCanvas(viewElement: ElementRef) {
        this.canvas = viewElement.nativeElement;
    }

    @ViewChild('slider') slider: MatSlider;

    public selectionState: { isValid: boolean, is2d: boolean, hasArchive: boolean } = {
        isValid: false,
        is2d: false,
        hasArchive: false
    };

    public observableSliceRequest: Subject<SliceRequest>;

    private labelExplorer: LabelExplorerComponent;

    // TODO: dynamic context and tool changes
    private currentTaggingContext = 'ALL';

    private selectorSubscriptions: Array<Subscription> = [];

    private selectorsByName: Map<string, Selector<SliceSelection>> = new Map();

    constructor() {
        super();

        this.redrawRequestEmitter.subscribe(() => {
           this.redrawSelections();
        });
    }

    get currentSlice() {
        return this._currentSlice;
    }

    public setSelectors(newSelectors: Array<Selector<SliceSelection>>) {
        super.setSelectors(newSelectors);
        this.selectorsByName.clear();
        this.selectors.forEach((selector: Selector<SliceSelection>) => {
            selector.setRedrawRequestEmitter(this.redrawRequestEmitter);
            this.selectorsByName.set(selector.getSelectorName(), selector);
        });
        this.hookUpStateChangeSubscription();
    }

    public setCurrentSelector(selector: Selector<any>) {
        this.currentSelector = selector;
    }

    public setDownloadScanInProgress(isInProgress: boolean) {
        this.downloadingScanInProgress = isInProgress;
    }

    public setDownloadSlicesInProgress(isInProgress: boolean) {
        this.downloadingSlicesInProgress = isInProgress;
    }

    public selectMiddleSlice(): void {
        const slicesCount = this.slider.max - this.slider.min + 1;
        const middleSliceNumber = this.slider.min + Math.floor(slicesCount / 2) - 1;
        this.slider.value = middleSliceNumber;
        this.changeMarkerImage(middleSliceNumber);
        this.drawSelections();
    }

    public removeAllSelectionsOnCurrentSlice(): void {
        this.selectors.forEach((selector) => selector.removeSelectionsOnCurrentSlice());
        this.updateSelectionState();
    }

    private updateSelectionState(): void {
        this.selectionState.hasArchive = this.selectors.some((selector) => selector.hasArchivedSelections());
        this.selectionState.is2d = this.selectors.some((selector) => selector.hasSliceSelection());
        this.selectionState.isValid = this.selectors.every((selector) => selector.hasValidSelection());
    }

    public get3dSelection(): SliceSelection[] {
        this.selectors.forEach((selector) => selector.archiveSelections());
        this.updateSelectionState();

        this.clearCanvasSelections();

        const coordinates: SliceSelection[] = this.selectors
            .map((selector) => selector.getSelections())
            .reduce((x, y) => x.concat(y), []);
        this.selectors.forEach((selector) => selector.clearSelections());
        this.updateSelectionState();

        this.drawSelections();

        return coordinates;
    }

    private hookUpStateChangeSubscription(): void {
        this.selectorSubscriptions.forEach((subscription) => subscription.unsubscribe());
        this.selectorSubscriptions = this.selectors
            .map((selector) => selector.getStateChangeEmitter().subscribe((selection: SelectionStateMessage) => {
                console.log('Marker | getStateChange event from selector!');
                this.updateSelectionState();
                if (this.labelExplorer) {
                    if (selection.toDelete) {
                        console.log('Marker | getStateChange remove selection from label explorer, selectionId: ', selection.selectionId);
                        this.labelExplorer.removeLabel(selection.selectionId);
                    } else {
                        console.log('Marker | getStateChange adding new selection to label explorer, selectionId: ',
                            selection.selectionId);
                        this.labelExplorer.addLabel(selection.selectionId, selection.sliceId, this.currentTaggingContext,
                            this.currentSelector.getSelectorName());
                    }
                }
        }));
    }

    private hookUpExplorerLabelChangeSubscription(): void {
        if (this.labelExplorer) {
            this.labelExplorer.getLabelChangeEmitter().subscribe((labelChanged: LabelListItem) => {
                console.log('Marker | getLabelChange event from label-explorer!');
                if (labelChanged.toDelete) {
                    this.selectorsByName.get(labelChanged.selectorName).removeSelection(labelChanged.selectionId);
                } else {
                    this.selectorsByName.get(labelChanged.selectorName).pinSelection(labelChanged.selectionId, labelChanged.pinned);
                    this.selectorsByName.get(labelChanged.selectorName).hideSelection(labelChanged.selectionId, labelChanged.hidden);
                }
                this.redrawSelections();
            });
        } else {
            console.warn(`Marker | hookUpExplorerLabelChangeSubscription cannot hook up observer when labelExplorer isn't present!`);
        }
    }

    public prepareForNewScan(): void {
        this.clearData();
        this.labelExplorer.reinitializeExplorer();
        this.hookUpStateChangeSubscription();
    }

    ngOnInit() {
        console.log('Marker init');
        console.log('View elements: image ', this.currentImage, ', canvas ', this.canvas, ', slider ', this.slider);

        this.slices = new Map<number, MarkerSlice>();

        this.initializeCanvas();

        this.initializeImage(() => {
            this.afterImageLoad();
        });

        this.setCanvasImage();

        this.slider.registerOnChange((sliderValue: number) => {
            console.log('Marker init | slider change: ', sliderValue);

            this.requestSlicesIfNeeded(sliderValue);
            this.changeMarkerImage(sliderValue);

            this.drawSelections();
        });

        this.initCanvasSelectionTool();

    }

    private afterImageLoad(): void {
        this.clearCanvasSelections();

        this.drawSelections();
        this.updateSelectionState();
    }

    private initCanvasSelectionTool(): void {
        console.log('Marker | initCanvasSelectionTool');

        this.canvas.onmousedown = (mouseEvent: MouseEvent) => {
            console.log('Marker | initCanvasSelectionTool | onmousedown clientXY: ', mouseEvent.clientX, mouseEvent.clientY);
            if (this.currentSelector.onMouseDown(mouseEvent)) {
                this.redrawSelections();
            }
        };

        this.canvas.onmouseup = (mouseEvent: MouseEvent) => {
            console.log('Marker | initCanvasSelectionTool | onmouseup clientXY: ', mouseEvent.clientX, mouseEvent.clientY);
            if (this.currentSelector.onMouseUp(mouseEvent)) {
                this.redrawSelections();
            }
        };

        this.canvas.onmousemove = (mouseEvent: MouseEvent) => {
            if (this.currentSelector.onMouseMove(mouseEvent)) {
                this.redrawSelections();
            }
        };
    }

    public setLabelExplorer(labelExplorerRef: LabelExplorerComponent): void {
        this.labelExplorer = labelExplorerRef;
        this.hookUpExplorerLabelChangeSubscription();
    }
}
