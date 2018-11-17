import {Component, OnInit, ViewChild} from '@angular/core';
import {ActivatedRoute} from '@angular/router';
import {ScanService} from '../../services/scan.service';
import {MarkerComponent} from '../../components/marker/marker.component';
import {ScanMetadata} from '../../model/ScanMetadata';
import {MarkerSlice} from '../../model/MarkerSlice';
import {Selection3D} from '../../model/selections/Selection3D';
import {RectangleTool} from '../../components/tools/RectangleTool';
import {SliceRequest} from '../../model/SliceRequest';
import {DialogService} from '../../services/dialog.service';
import {Router} from '@angular/router';
import {MatSnackBar} from '@angular/material';
import {LabelTag} from '../../model/labels/LabelTag';
import {LabelExplorerComponent} from '../../components/label-explorer/label-explorer.component';
import {Tool} from '../../components/tools/Tool';
import {PointTool} from '../../components/tools/PointTool';
import {BrushTool} from '../../components/tools/BrushTool';
import {FormControl, Validators} from '@angular/forms';
import {isUndefined} from 'util';
import {ChainTool} from '../../components/tools/ChainTool';
import {ToolAction, ToolActionType} from '../../model/ToolAction';
import {TaskService} from '../../services/task.service';
import {Task} from '../../model/Task';
import {HOME} from '../../constants/routes';
import {RectangleSelection} from '../../model/selections/RectangleSelection';
import {LabelService} from '../../services/label.service';
import {Label} from '../../model/labels/Label';
import {PredefinedBrushLabelElement} from '../../model/PredefinedBrushLabelElement';


@Component({
    selector: 'app-marker-page',
    templateUrl: './marker-page.component.html',
    providers: [ScanService, LabelService],
    styleUrls: ['./marker-page.component.scss']
})
export class MarkerPageComponent implements OnInit {

    private static readonly SLICE_BATCH_SIZE = 10;

    @ViewChild(MarkerComponent) marker: MarkerComponent;

    @ViewChild(LabelExplorerComponent) labelExplorer: LabelExplorerComponent;

    scan: ScanMetadata;
    task: Task;
    taskKey: string;
    lastSliceID = 0;
    startTime: Date;
    tools: Map<string, Tool<any>>;
    taskTags: FormControl;
    toolActions: Array<ToolAction> = [];
    labelComment: string;
    isInitialSliceLoad: boolean;
    homePage = '/' + HOME;

    getTaskPromise: Promise<Task>;

    ActionType = ToolActionType;

    zoomLevels = [1.0, 2.0, 4.0, 8.0];
    currentZoomLevelIndex = 0;

    constructor(private scanService: ScanService, private route: ActivatedRoute, private dialogService: DialogService,
                private router: Router, private snackBar: MatSnackBar, private taskService: TaskService,
                private labelService: LabelService) {
        console.log('MarkerPage constructor', this.marker);
        this.labelComment = '';
        this.isInitialSliceLoad = true;
    }

    ngOnInit() {
        console.log('MarkerPage init', this.marker);

        this.route.queryParamMap.subscribe(params => {
            this.taskKey = params.get('task') || undefined;
        });

        this.getTaskPromise = this.taskService.getTask(this.taskKey);
        this.getTaskPromise.then(
            (task: Task) => {
                this.task = task;

                if (this.task.tags.length === 0) {
                    this.dialogService
                        .openInfoDialog('There are no tags assigned to this task!', 'Please try another task!', 'Go back')
                        .afterClosed()
                        .subscribe(() => {
                            this.router.navigateByUrl(this.homePage);
                        });
                }
            },
            (errorResponse: Error) => {
                if (!this.task) {
                    this.dialogService
                        .openInfoDialog('You did not choose task properly!', 'Please choose it again!', 'Go back')
                        .afterClosed()
                        .subscribe(() => {
                            this.router.navigateByUrl(this.homePage);
                        });
                }
            });

        this.taskTags = new FormControl('', [Validators.required]);

        // Brush tool should be first on the list to avoid canvas shenanigans
        this.tools = new Map<string, Tool<any>>([
            ['BRUSH', new BrushTool(this.marker.getCanvas())],
            ['RECTANGLE', new RectangleTool(this.marker.getCanvas())],
            ['POINT', new PointTool(this.marker.getCanvas())],
            ['CHAIN', new ChainTool(this.marker.getCanvas())]
        ]);

        this.marker.setTools(Array.from(this.tools.values()));

        this.marker.setLabelExplorer(this.labelExplorer);

        this.requestScan();

        this.scanService.slicesObservable().subscribe((slice: MarkerSlice) => {
            console.log('MarkerPage | ngOnInit | slicesObservable: ', slice);
            if (slice.index > this.lastSliceID) {
                this.lastSliceID = slice.index;
            }
            this.marker.feedData(slice);
            if (slice.isLastInBatch()) {
                if (this.marker.downloadingScanInProgress === true) {
                    this.indicateNewScanAppeared();
                }
                if (this.isInitialSliceLoad === true) {
                    this.marker.selectMiddleSlice();
                    this.isInitialSliceLoad = false;
                }
                this.marker.setDownloadSlicesInProgress(false);
                this.marker.setDownloadScanInProgress(false);
            }
        });

        this.scanService.predefinedBrushLabelElementsObservable().subscribe((labelElement: PredefinedBrushLabelElement) => {
            console.log('MarkerPage | ngOnInit | predefinedBrushLabelElementsObservable: ', labelElement);
            this.marker.updatePredefinedBrushLabelElement(labelElement);
        });

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
                        this.scanService.requestSlices(this.scan.scanId, this.taskKey, sliceRequest, count, reversed);
                        this.marker.setDownloadSlicesInProgress(true);
                    }
                });
            }
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
        this.scanService.getRandomScan(this.taskKey).then(
            (scan: ScanMetadata) => {
                this.scan = scan;
                this.marker.setScanMetadata(this.scan);
                if (this.scan.predefinedLabelID) {
                    // Make sure that we've already resolved current Task
                    this.getTaskPromise.then((task: Task) => {
                        this.labelService.getLabelByID(this.scan.predefinedLabelID, task).then((label: Label) => {
                            this.marker.setLabel(label);
                        });
                    });
                }

                const begin = Math.floor(Math.random() * (scan.numberOfSlices - MarkerPageComponent.SLICE_BATCH_SIZE));
                const count = MarkerPageComponent.SLICE_BATCH_SIZE;
                this.startMeasuringLabelingTime();
                this.isInitialSliceLoad = true;
                this.scanService.requestSlices(this.scan.scanId, this.taskKey, begin, count, false);
            },
            (errorResponse: Error) => {
                console.log(errorResponse);
                this.marker.setDownloadScanInProgress(false);
                this.marker.setDownloadSlicesInProgress(false);
                this.dialogService
                    .openInfoDialog('Nothing to do here!', 'No more Scans available for you in this dataset!', 'Go back')
                    .afterClosed()
                    .subscribe(() => {
                        this.router.navigateByUrl(this.homePage);
                    });
            });
    }

    public skipScan(): void {
        this.scanService.skipScan(this.scan.scanId).then();
        this.nextScan();
    }

    public nextScan(): void {
        this.marker.setDownloadScanInProgress(true);
        this.marker.prepareForNewScan();
        this.labelComment = '';
        this.requestScan();
    }

    public sendCompleteLabel(): void {
        this.sendSelection(new Selection3D(<RectangleSelection[]>this.marker.get3dSelection()), this.labelComment);
    }

    public sendEmptyLabel(): void {
        this.sendSelection(new Selection3D(), 'This is an empty Label');
        this.nextScan();
    }

    private sendSelection(selection3d: Selection3D, comment: string) {
        const labelingTime = this.getLabelingTimeInSeconds(this.startTime);

        this.scanService.sendSelection(this.scan.scanId, this.task.key, selection3d, labelingTime, comment)
            .then((response: Response) => {
                console.log('MarkerPage | sendSelection | success!');
                this.indicateLabelHasBeenSend();
                this.labelExplorer.reinitializeExplorer();
                this.nextScan();
                this.startMeasuringLabelingTime();
            })
            .catch((errorResponse: Error) => {
                this.dialogService.openInfoDialog('Error', 'Cannot send selection', 'Ok');
            });
    }

    public remove2dSelection(): void {
        this.marker.removeAllSelectionsOnCurrentSlice();
    }

    private startMeasuringLabelingTime(): void {
        this.startTime = new Date();
    }

    private getLabelingTimeInSeconds(startTime: Date): number {
        const endTime = new Date();
        return (endTime.getTime() - startTime.getTime()) / 1000.0;
    }

    private indicateLabelHasBeenSend(): void {
        this.snackBar.open('Label has been sent!', '', {duration: 2000});
    }

    private indicateNewScanAppeared(): void {
        this.snackBar.open('New scan has been loaded!', '', {duration: 2000});
    }

    public isCurrentTool(toolName: string): boolean {
        const currentTool = this.marker.getCurrentTool();
        return currentTool && currentTool.getToolName() === toolName;
    }

    public isToolSupportedByCurrentTag(tool: string) {
        const tag = this.marker.getCurrentTag();
        if (isUndefined(tag)) {
            return false;
        }
        return tag.tools.includes(tool);
    }

    public setTool(toolName: string) {
        const tool = this.tools.get(toolName);
        if (tool) {
            this.marker.setCurrentTool(tool);
            this.toolActions = tool.getActions();
        } else {
            console.warn(`MarkerPage | setTool | Tool "${toolName}" doesn't exist`);
        }
    }

    public clearTool() {
        this.marker.clearCurrentTool();
        this.toolActions = [];
    }

    public setTag(tag: LabelTag) {
        this.marker.setCurrentTag(tag);
        const currentTool = this.marker.getCurrentTool();
        if (!isUndefined(currentTool)) {
            if (!this.isToolSupportedByCurrentTag(currentTool.getToolName())) {
                this.clearTool();
            }
        }
    }

    public getToolIconName(iconName: string): string {
        return LabelExplorerComponent.toolIconNames.get(iconName);
    }

    public addLabelComment(): void {
        this.marker.setFocusable(false);
        this.dialogService.openInputDialog('Add comment to your label (optional)', '',
            this.labelComment, this.labelComment ? 'Save comment' : 'Add comment').afterClosed().subscribe(comment => {
            this.labelComment = comment;
            this.marker.setFocusable(true);
        });
    }
}
