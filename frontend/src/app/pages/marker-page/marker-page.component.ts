import { List } from 'immutable';
import { Component, OnInit, ViewChild } from '@angular/core';
import { MatSnackBar } from '@angular/material';
import { ActivatedRoute, Router } from '@angular/router';
import { LabelExplorerComponent } from '../../components/label-explorer/label-explorer.component';
import { MarkerComponent } from '../../components/marker/marker.component';
import { BrushTool } from '../../components/tools/BrushTool';
import { ChainTool } from '../../components/tools/ChainTool';
import { PointTool } from '../../components/tools/PointTool';
import { RectangleTool } from '../../components/tools/RectangleTool';
import { Tool } from '../../components/tools/Tool';
import { HOME } from '../../constants/routes';
import { Label } from '../../model/labels/Label';
import { LabelTag } from '../../model/labels/LabelTag';
import { MarkerSlice } from '../../model/MarkerSlice';
import { PredefinedBrushLabelElement } from '../../model/PredefinedBrushLabelElement';
import { ScanMetadata } from '../../model/ScanMetadata';
import { Selection3D } from '../../model/selections/Selection3D';
import { SliceSelection, SliceSelectionType } from '../../model/selections/SliceSelection';
import { SliceRequest } from '../../model/SliceRequest';
import { Task } from '../../model/Task';
import { ToolAction, ToolActionType } from '../../model/ToolAction';
import { DialogService } from '../../services/dialog.service';
import { LabelService } from '../../services/label.service';
import { ScanService } from '../../services/scan.service';
import { TaskService } from '../../services/task.service';
import { BrushSelection } from './../../model/selections/BrushSelection';
import { MarkerAction } from './marker-actions/MarkerAction';

@Component({
    selector: 'app-marker-page',
    templateUrl: './marker-page.component.html',
    providers: [ScanService, LabelService],
    styleUrls: ['./marker-page.component.scss']
})
export class MarkerPageComponent implements OnInit {
    private static readonly SLICE_BATCH_SIZE = 10;
    private static readonly HOME_PAGE = '/' + HOME;

    @ViewChild(MarkerComponent) marker: MarkerComponent;

    @ViewChild(LabelExplorerComponent) labelExplorer: LabelExplorerComponent;

    selections: List<SliceSelection> = List();
    scan: ScanMetadata;
    task: Task;
    startTime: Date;
    tools: List<Tool<SliceSelection>>;
    currentTool: Tool<SliceSelection>;
    currentTag: LabelTag;
    markerActions: List<MarkerAction> = List();
    toolActions: List<ToolAction> = List();
    labelComment: string;
    isInitialSliceLoad: boolean;

    ActionType = ToolActionType;

    zoomLevels = List([1.0, 2.0, 4.0, 8.0]);
    currentZoomLevelIndex = 0;

    constructor(
        private scanService: ScanService,
        private route: ActivatedRoute,
        private dialogService: DialogService,
        private router: Router,
        private snackBar: MatSnackBar,
        private taskService: TaskService,
        private labelService: LabelService
    ) {
        console.log('MarkerPage constructor', this.marker);
        this.labelComment = '';
        this.isInitialSliceLoad = true;
    }

    ngOnInit() {
        console.log('MarkerPage init', this.marker);

        this.route.queryParamMap.subscribe(params => {
            const taskKey = params.get('task') || undefined;

            this.taskService.getTask(taskKey).then(
                (task: Task) => {
                    this.task = task;

                    if (this.task.tags.length === 0) {
                        this.dialogService
                            .openInfoDialog('There are no tags assigned to this task!', 'Please try another task!', 'Go back')
                            .afterClosed()
                            .subscribe(() => {
                                this.router.navigateByUrl(MarkerPageComponent.HOME_PAGE);
                            });
                    }

                    this.requestScan();

                    this.marker.hookUpSliceObserver(MarkerPageComponent.SLICE_BATCH_SIZE).then((isObserverHooked: boolean) => {
                        if (isObserverHooked) {
                            this.marker.observableSliceRequest.subscribe((request: SliceRequest) => {
                                const reversed = request.reversed;
                                let sliceRequest = request.slice;
                                console.log('MarkerPage | observable sliceRequest: ', sliceRequest, ' reversed: ', reversed);
                                let count = MarkerPageComponent.SLICE_BATCH_SIZE;
                                if (reversed === false && sliceRequest + count > this.scan.numberOfSlices) {
                                    count = this.scan.numberOfSlices - sliceRequest;
                                }
                                if (reversed === true) {
                                    sliceRequest -= count;
                                    if (sliceRequest < 0) {
                                        count += sliceRequest;
                                        sliceRequest = 0;
                                    }
                                }
                                if (count <= 0) {
                                    return;
                                }
                                if (this.marker.downloadingSlicesInProgress === false) {
                                    this.scanService.requestSlices(this.scan.scanId, this.task.key, sliceRequest, count, reversed);
                                    this.marker.setDownloadSlicesInProgress(true);
                                }
                            });
                        }
                    });
                },
                (_: Error) => {
                    if (!this.task) {
                        this.dialogService
                            .openInfoDialog('You did not choose task properly!', 'Please choose it again!', 'Go back')
                            .afterClosed()
                            .subscribe(() => {
                                this.router.navigateByUrl(MarkerPageComponent.HOME_PAGE);
                            });
                    }
                }
            );
        });

        // Brush tool should be first on the list to avoid canvas shenanigans
        this.tools = List([new BrushTool(), new RectangleTool(), new PointTool(), new ChainTool()]);

        this.scanService.slicesObservable().subscribe((slice: MarkerSlice) => {
            console.log('MarkerPage | ngOnInit | slicesObservable: ', slice);
            this.marker.feedData(slice);
            if (slice.isLastInBatch()) {
                if (this.marker.downloadingScanInProgress === true) {
                    this.indicateNewScanAppeared();
                }
                if (this.isInitialSliceLoad) {
                    this.marker.selectMiddleSlice();
                    this.isInitialSliceLoad = false;
                }
                this.marker.setDownloadSlicesInProgress(false);
                this.marker.setDownloadScanInProgress(false);
            }
        });

        this.scanService.predefinedBrushLabelElementsObservable().subscribe((labelElement: PredefinedBrushLabelElement) => {
            console.log('MarkerPage | ngOnInit | predefinedBrushLabelElementsObservable: ', labelElement);
            this.selections.forEach((selection: SliceSelection) => {
                if (
                    selection.sliceIndex === labelElement.index &&
                    selection.labelTag.key === labelElement.tag_key &&
                    selection.labelTool === 'BRUSH'
                ) {
                    const brushSelection: BrushSelection = selection as BrushSelection;
                    brushSelection.setImage(labelElement.source);
                }
            });
        });
    }

    public zoomIn(): void {
        this.currentZoomLevelIndex++;
        this.marker.scale = this.zoomLevels[this.currentZoomLevelIndex];
    }

    public zoomOut(): void {
        this.currentZoomLevelIndex--;
        this.marker.scale = this.zoomLevels[this.currentZoomLevelIndex];
    }

    private requestScan(): void {
        this.marker.setDownloadScanInProgress(true);
        this.scanService.getRandomScan(this.task.key).then(
            (scan: ScanMetadata) => {
                this.scan = scan;
                this.marker.setScanMetadata(this.scan);
                if (this.scan.predefinedLabelID) {
                    this.labelService.getLabelByID(this.scan.predefinedLabelID, this.task).then((label: Label) => {
                        this.selections = List(label.labelSelections);
                    });
                }

                const begin = Math.floor(Math.random() * (scan.numberOfSlices - MarkerPageComponent.SLICE_BATCH_SIZE));
                const count = MarkerPageComponent.SLICE_BATCH_SIZE;
                this.startTime = new Date();
                this.isInitialSliceLoad = true;
                this.scanService.requestSlices(this.scan.scanId, this.task.key, begin, count, false);
            },
            (errorResponse: Error) => {
                console.log(errorResponse);
                this.marker.setDownloadScanInProgress(false);
                this.marker.setDownloadSlicesInProgress(false);
                this.dialogService
                    .openInfoDialog('Nothing to do here!', 'No more Scans available for you in this dataset!', 'Go back')
                    .afterClosed()
                    .subscribe(() => {
                        this.router.navigateByUrl(MarkerPageComponent.HOME_PAGE);
                    });
            }
        );
    }

    public skipScan(): void {
        this.scanService.skipScan(this.scan.scanId).then();
        this.nextScan();
    }

    public nextScan(): void {
        this.marker.setDownloadScanInProgress(true);
        this.labelComment = '';
        this.requestScan();
    }

    public sendCompleteLabel(): void {
        this.sendSelection(new Selection3D(this.selections.toJS()), this.labelComment);
    }

    public sendEmptyLabel(): void {
        this.sendSelection(new Selection3D(), 'This is an empty Label');
    }

    private sendSelection(selection3d: Selection3D, comment: string) {
        const labelingTime = this.getLabelingTimeInSeconds(this.startTime);

        this.scanService
            .sendSelection(this.scan.scanId, this.task.key, selection3d, labelingTime, comment)
            .then((response: Response) => {
                console.log('MarkerPage | sendSelection | success!');
                this.indicateLabelHasBeenSend();
                this.nextScan();
            })
            .catch((errorResponse: Error) => {
                this.dialogService.openInfoDialog('Error', 'Cannot send selection', 'Ok');
            });
    }

    private getLabelingTimeInSeconds(startTime: Date): number {
        const endTime = new Date();
        return (endTime.getTime() - startTime.getTime()) / 1000.0;
    }

    private indicateLabelHasBeenSend(): void {
        this.snackBar.open('Label has been sent!', '', { duration: 2000 });
    }

    private indicateNewScanAppeared(): void {
        this.snackBar.open('New scan has been loaded!', '', { duration: 2000 });
    }

    public isCurrentTool(toolName: string): boolean {
        return this.currentTool && this.currentTool.getToolName() === toolName;
    }

    public isToolSupportedByCurrentTag(tool: string) {
        return this.currentTag && this.currentTag.tools.includes(tool);
    }

    public setTool(toolName: string) {
        this.currentTool = this.tools.find(tool => tool.getToolName() === toolName);
    }

    public setTag(tag: LabelTag) {
        this.currentTag = tag;
        if (this.currentTool && !this.isToolSupportedByCurrentTag(this.currentTool.getToolName())) {
            this.setTool(undefined);
        }
    }

    public getToolIconName(iconName: string): string {
        return LabelExplorerComponent.toolIconNames.get(iconName);
    }

    public addLabelComment(): void {
        this.marker.setSliderFocus(false);
        this.dialogService
            .openInputDialog(
                'Add comment to your label (optional)',
                '',
                this.labelComment,
                this.labelComment ? 'Save comment' : 'Add comment'
            )
            .afterClosed()
            .subscribe(comment => {
                this.labelComment = comment;
                this.marker.setSliderFocus(true);
            });
    }

    public isAnyNonDraftSelection(): boolean {
        return !!this.selections.find(selection => selection.type !== SliceSelectionType.DRAFT);
    }

    public canUndo(): boolean {
        return true;
    }

    public undo(): void {}

    public canRedo(): boolean {
        return true;
    }

    public redo(): void {}
}
