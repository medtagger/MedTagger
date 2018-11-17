import {Component, EventEmitter, OnInit} from '@angular/core';
import {MarkerSlice} from '../../model/MarkerSlice';
import {MatSlider} from '@angular/material/slider';
import {Subject} from 'rxjs';
import {ScanViewerComponent} from '../scan-viewer/scan-viewer.component';
import {SliceRequest} from '../../model/SliceRequest';
import {SliceSelection} from '../../model/selections/SliceSelection';
import {LabelExplorerComponent} from '../label-explorer/label-explorer.component';
import {LabelListItem} from '../../model/labels/LabelListItem';
import {SelectionStateMessage} from '../../model/SelectionStateMessage';
import {Tool} from '../tools/Tool';
import {Subscription} from 'rxjs/Subscription';
import {isUndefined} from 'util';
import {MatSnackBar} from '@angular/material';
import {LabelTag} from '../../model/labels/LabelTag';
import {Label} from '../../model/labels/Label';
import {PredefinedBrushLabelElement} from '../../model/PredefinedBrushLabelElement';
import {BrushTool} from '../tools/BrushTool';

@Component({
    selector: 'app-marker-component',
    templateUrl: './marker.component.html',
    styleUrls: ['./marker.component.scss']
})
export class MarkerComponent extends ScanViewerComponent implements OnInit {

    redrawRequestEmitter: EventEmitter<void> = new EventEmitter<void>();

    private currentTool: Tool<SliceSelection>;
    private currentTag: LabelTag;

    public selectionState: { isValid: boolean, is2d: boolean, hasArchive: boolean } = {
        isValid: false,
        is2d: false,
        hasArchive: false
    };

    private labelExplorer: LabelExplorerComponent;

    private toolSubscriptions: Array<Subscription> = [];

    private toolsByName: Map<string, Tool<SliceSelection>> = new Map();

    constructor(public snackBar: MatSnackBar) {
        super();

        this.redrawRequestEmitter.subscribe(() => {
            this.redrawSelections();
        });
    }

    public setTools(newTools: Array<Tool<SliceSelection>>) {
        super.setTools(newTools);
        this.toolsByName.clear();
        this.tools.forEach((tool: Tool<SliceSelection>) => {
            tool.setRedrawRequestEmitter(this.redrawRequestEmitter);
            this.toolsByName.set(tool.getToolName(), tool);
        });
        this.hookUpStateChangeSubscription();
    }

    public getCurrentTool(): Tool<any> {
        return this.currentTool;
    }

    public setCurrentTool(tool: Tool<any>) {
        if (this.currentTool) {
            this.currentTool.onToolChange();
        }
        this.currentTool = tool;
        this.updateTagForCurrentTool(this.currentTag);
    }

    public updateTagForCurrentTool(tag: LabelTag): void {
        super.setCurrentTagForTool(this.currentTool, tag);
    }

    public clearCurrentTool() {
        this.currentTool = undefined;
    }

    public setCurrentTag(tag: LabelTag) {
        super.setCurrentTag(tag);
        this.currentTag = tag;
        this.updateTagForCurrentTool(this.currentTag);
    }

    public removeAllSelectionsOnCurrentSlice(): void {
        this.tools.forEach((tool) => tool.removeSelectionsOnCurrentSlice());
        this.updateSelectionState();
    }

    private updateSelectionState(): void {
        this.selectionState.hasArchive = this.tools.some((tool) => tool.hasArchivedSelections());
        this.selectionState.is2d = this.tools.some((tool) => tool.hasSliceSelection());
        this.selectionState.isValid = this.tools.every((tool) => tool.hasValidSelection());
    }

    public get3dSelection(): SliceSelection[] {
        return this.tools
            .map((tool) => tool.getSelections())
            .reduce((x, y) => x.concat(y), []);
    }

    public getCurrentTag() {
        return this.currentTag;
    }

    private hookUpStateChangeSubscription(): void {
        this.toolSubscriptions.forEach((subscription) => subscription.unsubscribe());
        this.toolSubscriptions = this.tools
            .map((tool) => tool.getStateChangeEmitter().subscribe((selection: SelectionStateMessage) => {
                console.log('Marker | getStateChange event from tool!');
                this.updateSelectionState();
                if (this.labelExplorer) {
                    if (selection.toDelete) {
                        console.log('Marker | getStateChange remove selection from label explorer, selectionId: ', selection.selectionId);
                        this.labelExplorer.removeLabel(selection.selectionId);
                    } else {
                        console.log('Marker | getStateChange adding new selection to label explorer, selectionId: ',
                            selection.selectionId);
                        if (!isUndefined(this.currentTool) && this.currentTool.isSingleSelectionPerSlice()) {
                            this.labelExplorer.replaceExistingLabel(selection.selectionId, selection.sliceId,
                                selection.labelTag, selection.toolName);
                        } else {
                            this.labelExplorer.addLabel(selection.selectionId, selection.sliceId, selection.labelTag,
                                selection.toolName);
                        }
                    }
                }
            }));
    }

    private hookUpExplorerLabelChangeSubscription(): void {
        if (this.labelExplorer) {
            this.labelExplorer.getLabelChangeEmitter().subscribe((labelChanged: LabelListItem) => {
                console.log('Marker | getLabelChange event from label-explorer!');
                if (labelChanged.toDelete) {
                    this.toolsByName.get(labelChanged.toolName).removeSelection(labelChanged.selectionId);
                } else {
                    this.toolsByName.get(labelChanged.toolName).pinSelection(labelChanged.selectionId, labelChanged.pinned);
                    this.toolsByName.get(labelChanged.toolName).hideSelection(labelChanged.selectionId, labelChanged.hidden);
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
        console.log('MarkerComponent init');

        this.slices = new Map<number, MarkerSlice>();

        this.updateCanvasPositionInTools();

        this.initializeImage(() => {
            this.clearCanvasSelections();
            this.drawSelections();
            this.updateSelectionState();
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

    public setLabel(label: Label): void {
        label.labelSelections.forEach( (selection: SliceSelection) => {
            this.toolsByName.get(selection.label_tool).addSelection(selection);
        });
    }

    public updatePredefinedBrushLabelElement(labelElement: PredefinedBrushLabelElement): void {
        const tool: BrushTool = this.toolsByName.get('BRUSH') as BrushTool;
        tool.updateBrushSelection(labelElement.index, labelElement.tag_key, labelElement.source);
    }

    private initCanvasSelectionTool(): void {
        console.log('Marker | initCanvasSelectionTool');

        this.canvas.onmousedown = (mouseEvent: MouseEvent) => {
            console.log('Marker | initCanvasSelectionTool | onmousedown clientXY: ', mouseEvent.clientX, mouseEvent.clientY);
            if (isUndefined(this.currentTag)) {
                this.snackBar.open('Please select Tag and Tool to start labeling.', '', {duration: 2000});
                return;
            } else if (isUndefined(this.currentTool)) {
                this.snackBar.open('Please select Tool to start labeling.', '', {duration: 2000});
                return;
            }
            if (this.currentTool) {
                this.currentTool.onMouseDown(mouseEvent);
            }
        };

        this.canvas.onmouseup = (mouseEvent: MouseEvent) => {
            console.log('Marker | initCanvasSelectionTool | onmouseup clientXY: ', mouseEvent.clientX, mouseEvent.clientY);
            if (this.currentTool) {
                this.currentTool.onMouseUp(mouseEvent);
            }
        };

        this.canvas.onmousemove = (mouseEvent: MouseEvent) => {
            if (this.currentTool) {
                this.currentTool.onMouseMove(mouseEvent);
            }
        };

        this.canvas.onwheel = (wheelEvent: WheelEvent) => {
            if (this.currentTool && !this.currentTool.canChangeSlice()) {
                return;
            }

            const sliderValue = wheelEvent.deltaY > 0 ? this.slider.value - 1 : this.slider.value + 1;

            if (sliderValue >= this.slider.min && sliderValue <= this.slider.max) {
                this.tools.forEach((tool) => tool.updateCurrentSlice(sliderValue));
                this.requestSlicesIfNeeded(sliderValue);

                this.changeMarkerImage(sliderValue);

                this.drawSelections();
            }
        };
    }

    public setLabelExplorer(labelExplorerRef: LabelExplorerComponent): void {
        this.labelExplorer = labelExplorerRef;
        this.hookUpExplorerLabelChangeSubscription();
    }

    public canChangeSlice(): boolean {
        return this.currentTool ? this.currentTool.canChangeSlice() : true;
    }
}
