import {Component, ElementRef, OnInit, ViewChild, HostListener} from '@angular/core';
import {MarkerSlice} from '../../model/MarkerSlice';
import {MatSlider} from '@angular/material/slider';
import {Subject} from 'rxjs';
import {ScanViewerComponent} from '../scan-viewer/scan-viewer.component';
import {SliceSelection} from '../../model/SliceSelection';
import {LabelExplorerComponent} from "../label-explorer/label-explorer.component";
import {LabelListItem} from "../../model/LabelListItem";
import {SelectionStateMessage} from "../../model/SelectionStateMessage";

@Component({
    selector: 'app-marker-component',
    templateUrl: './marker.component.html',
    styleUrls: ['./marker.component.scss']
})
export class MarkerComponent extends ScanViewerComponent implements OnInit {

    currentImage: HTMLImageElement;
    downloadingScanInProgress = false;
    downloadingSlicesInProgress = false;

    @ViewChild('image')
    set viewImage(viewElement: ElementRef) {
        this.currentImage = viewElement.nativeElement;
    }

    canvas: HTMLCanvasElement;

    @ViewChild('canvas')
    set viewCanvas(viewElement: ElementRef) {
        this.canvas = viewElement.nativeElement;
    }

    @ViewChild('slider') slider: MatSlider;

    public selectionState: {isValid: boolean, is2d: boolean, hasArchive: boolean} = { isValid: false, is2d: false, hasArchive: false};

    public observableSliceRequest: Subject<number>;

    private labelExplorer: LabelExplorerComponent;

    //TODO: dynamic context and tool changes
    private currentTaggingContext: string = "ALL";
    private currentTool: string = "RECTANGLE";

    constructor() {
        super();
    }

    get currentSlice() {
        return this._currentSlice;
    }

    public setDownloadScanInProgress(isInProgress: boolean) {
        this.downloadingScanInProgress = isInProgress;
    }

    public setDownloadSlicesInProgress(isInProgress: boolean) {
        this.downloadingSlicesInProgress = isInProgress;
    }

    public removeCurrentSelection(): void {
        this.selector.removeCurrentSelection();
        this.updateSelectionState();
    }

    private updateSelectionState(): void {
        this.selectionState.hasArchive = this.selector.hasArchivedSelections();
        this.selectionState.is2d = this.selector.hasSliceSelection();
        this.selectionState.isValid = this.selector.hasValidSelection();
    }

    public get3dSelection(): SliceSelection[] {
        this.selector.archiveSelections();
        this.updateSelectionState();

        this.selector.clearCanvasSelection();

        const coordinates: SliceSelection[] = this.selector.getSelections();
        this.selector.clearSelections();
        this.updateSelectionState();

        this.selector.drawSelections();

        return coordinates;
    }

    private hookUpStateChangeSubscription(): void {
        this.selector.getStateChangeEmitter().subscribe((selectionStateMessage: SelectionStateMessage) => {
            console.log('Marker | getStateChange event from selector!');
            this.updateSelectionState();
            if (this.labelExplorer) {
            	if(selectionStateMessage.toDelete) {
					console.log('Marker | getStateChange remove slice from label explorer, sliceId: ', selectionStateMessage.sliceId);
					this.labelExplorer.removeLabel(selectionStateMessage.sliceId, this.currentTaggingContext, this.currentTool);
				} else {
					console.log('Marker | getStateChange adding new slice to label explorer, sliceId: ', selectionStateMessage.sliceId);
					this.labelExplorer.addLabel(selectionStateMessage.sliceId, this.currentTaggingContext, this.currentTool);
				}
			}
        });
    }

    private hookUpExplorerLabelChangeSubscription(): void {
    	if(this.labelExplorer) {
    		this.labelExplorer.getLabelChangeEmitter().subscribe( (labelChanged: LabelListItem)=> {
				console.log('Marker | getLabelChange event from label-explorer!');
				if(labelChanged.toDelete) {
					this.selector.removeSelection(labelChanged.sliceIndex);
				} else {
					this.selector.pinSelection(labelChanged.sliceIndex, labelChanged.pinned);
					this.selector.hideSelection(labelChanged.sliceIndex, labelChanged.hidden);
				}
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

        this.selector.clearData();

        this.hookUpStateChangeSubscription();

        this.initializeCanvas();

        this.initializeImage(() => {
        	this.afterImageLoad();
		});

        this.setCanvasImage();

        this.slider.registerOnChange((sliderValue: number) => {
            console.log('Marker init | slider change: ', sliderValue);

            this.requestSlicesIfNeeded(sliderValue);
            this.changeMarkerImage(sliderValue);

            this.selector.drawSelections();
        });

        this.initCanvasSelectionTool();

    }

    private afterImageLoad(): void {
		this.selector.clearCanvasSelection();

		this.selector.drawSelections();
		this.updateSelectionState();
	}

    private initCanvasSelectionTool(): void {
        console.log('Marker | initCanvasSelectionTool');

        this.canvas.onmousedown = (mouseEvent: MouseEvent) => {
            console.log('Marker | initCanvasSelectionTool | onmousedown clientXY: ', mouseEvent.clientX, mouseEvent.clientY);
            this.selector.onMouseDown(mouseEvent);
        };

        this.canvas.onmouseup = (mouseEvent: MouseEvent) => {
			console.log('Marker | initCanvasSelectionTool | onmouseup clientXY: ', mouseEvent.clientX, mouseEvent.clientY);
            this.selector.onMouseUp(mouseEvent);
        };

        this.canvas.onmousemove = (mouseEvent: MouseEvent) => {
            this.selector.onMouseMove(mouseEvent);
        };
    }

    public setLabelExplorer(labelExplorerRef: LabelExplorerComponent): void {
    	this.labelExplorer = labelExplorerRef;
    	this.hookUpExplorerLabelChangeSubscription();
	}
}
