import { List } from 'immutable';
import { Component, OnInit, ViewChild, ElementRef, NgZone, Renderer2 } from '@angular/core';
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
import { SliceSelection } from '../../model/selections/SliceSelection';
import { SliceRequest } from '../../model/SliceRequest';
import { Task } from '../../model/Task';
import { ToolAction, ToolActionType } from '../../model/ToolAction';
import { DialogService } from '../../services/dialog.service';
import { LabelService } from '../../services/label.service';
import { ScanService } from '../../services/scan.service';
import { TaskService } from '../../services/task.service';
import { BrushSelection } from './../../model/selections/BrushSelection';
import { MarkerZoomHandler } from '../../model/MarkerZoomHandler';
import { NavBarComponent } from '../../components/nav-bar/nav-bar.component';
import { Operation, TaskStatus } from '../../model/TaskStatus';
import { TaskDescription } from '../../model/TaskDescription';
import { FormControl } from '@angular/forms';
import { TranslateService } from '@ngx-translate/core';


@Component({
    selector: 'app-marker-page',
    templateUrl: './marker-page.component.html',
    providers: [ScanService, LabelService],
    styleUrls: ['./marker-page.component.scss']
})
export class MarkerPageComponent implements OnInit {
    private static readonly SLICE_BATCH_SIZE = 10;
    private static readonly DEFAULT_COLOR_WINDOW_WIDTH = 255;
    private static readonly DEFAULT_COLOR_WINDOW_CENTER = 128;
    private static readonly HOME_PAGE = '/' + HOME;

    @ViewChild(MarkerComponent) marker: MarkerComponent;

    @ViewChild(LabelExplorerComponent) labelExplorer: LabelExplorerComponent;

    @ViewChild(NavBarComponent) navBar: NavBarComponent;

    @ViewChild('timer')
    public taskTimer: ElementRef;
    currentTime: string;
    taskStatus: TaskStatus;
    tooltipShowDelay = new FormControl(1000);

    selections: List<SliceSelection> = List();
    scan: ScanMetadata;
    task: Task;
    startTime: Date;
    tools: List<Tool<SliceSelection>>;
    currentTool: Tool<SliceSelection>;
    currentTag: LabelTag;
    labelComment = '';
    isInitialSliceLoad: boolean;

    public colorWindowPanelActive = false;
    public colorWindowWidth: number = MarkerPageComponent.DEFAULT_COLOR_WINDOW_WIDTH;
    public colorWindowCenter: number = MarkerPageComponent.DEFAULT_COLOR_WINDOW_CENTER;

    public taskDescription: TaskDescription;
    public taskDescriptionPanelActive = false;

    ActionType = ToolActionType;

    zoomHandler: MarkerZoomHandler;

    constructor(
        private scanService: ScanService,
        private route: ActivatedRoute,
        private dialogService: DialogService,
        private router: Router,
        private snackBar: MatSnackBar,
        private taskService: TaskService,
        private labelService: LabelService,
        private zone: NgZone,
        private renderer: Renderer2,
        private translateService: TranslateService
    ) {
        console.log('MarkerPage constructor', this.marker);
        this.isInitialSliceLoad = true;
    }

    ngOnInit() {
        console.log('MarkerPage init', this.marker);

        this.zoomHandler = new MarkerZoomHandler();

        this.route.queryParamMap.subscribe(params => {
            const taskKey = params.get('task') || undefined;

            this.taskService.getTask(taskKey).then(
                (task: Task) => {
                    this.task = task;

                    // TODO: just for testing
                    this.taskStatus = new TaskStatus(5);
                    // tslint:disable-next-line: max-line-length
                    this.taskDescription = new TaskDescription('Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent scelerisque nulla non laoreet eleifend. Quisque gravida sem sit amet quam consequat malesuada. Nunc tellus nisl, euismod et augue efficitur, egestas sollicitudin neque. Etiam convallis, diam quis convallis posuere, dolor mi blandit ante, ut blandit diam orci quis dolor. Morbi tellus felis, blandit et lorem ac, hendrerit luctus risus. Cras sodales urna ultricies est dignissim tempor. Sed at velit ac odio lacinia dignissim sit amet.',
                     new Array('../../../assets/img/login_pic.jpg', '../../../assets/img/login_pic.jpg'));

                    this.zone.runOutsideAngular(this.printCurrentLabellingTime.bind(this));

                    if (this.task.tags.length === 0) {
                        this.dialogService
                            .openTranslatedInfoDialog('MARKER.DIALOG.NO_TAGS')
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
                                    sliceRequest = sliceRequest - count + 1; // We still want requested slice thats why +1
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
                                    this.taskStatus.changeStatusOperation(Operation.DOWNLOADING_SLICES);
                                }
                            });
                        }
                    });
                },
                (_: Error) => {
                    if (!this.task) {
                        this.taskStatus.changeStatusOperation(Operation.DOWNLOADING_ERROR);
                        this.dialogService
                            .openTranslatedInfoDialog('MARKER.DIALOG.NO_TASK')
                            .afterClosed()
                            .subscribe(() => {
                                this.router.navigateByUrl(MarkerPageComponent.HOME_PAGE);
                            });
                    }
                }
            );
        });

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
                this.taskStatus.changeStatusOperation(Operation.WAITING);
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

        this.marker.setZoomHandler(this.zoomHandler);
    }

    private printCurrentLabellingTime() {
        setInterval(() => {
            if (!!this.taskStatus) {
                const newTime = new Date(Date.now() - this.taskStatus.labellingTime);
                const minutes = newTime.getMinutes();
                const seconds = newTime.getSeconds();

                this.currentTime = `${minutes < 10 ? '0' + minutes : minutes}:${seconds < 10 ? '0' + seconds : seconds}`;

                this.renderer.setProperty(this.taskTimer.nativeElement, 'textContent', this.currentTime);
            }
        }, 1000);
    }

    onStatusUpdate(eventOperation: Operation) {
        this.taskStatus.changeStatusOperation(eventOperation);
    }

    public zoomIn(): void {
        this.marker.scale = this.zoomHandler.zoomIn();
        this.snackBar.open(this.translateService.instant('MARKER.ZOOM_INFO'), '', { duration: 3000 });
    }

    public zoomOut(): void {
        this.marker.scale = this.zoomHandler.zoomOut();
    }

    public get toolActions(): List<ToolAction> {
        return this.currentTool ? List(this.currentTool.getActions()) : List();
    }

    private requestScan(): void {
        this.marker.setDownloadScanInProgress(true);
        this.taskStatus.changeStatusOperation(Operation.DOWNLOADING_SCAN);
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
                    .openTranslatedInfoDialog('MARKER.DIALOG.NO_SCANS')
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
        this.taskStatus.changeStatusOperation(Operation.DOWNLOADING_SCAN);
        this.labelComment = '';
        this.selections = List();
        this.currentTool = undefined;
        this.marker.clearData();
        this.requestScan();
    }

    public sendCompleteLabel(): void {
        let dialogPackage;
        if (this.checkForSingleSliceSelection()) {
            dialogPackage = 'SINGLE_SELECTION';
        } else if (this.checkForIncompleteTagSelections()) {
            dialogPackage = 'SINGLE_TAG';
        }

        if (dialogPackage) {
            this.dialogService
            .openTranslatedConfirmDialog('MARKER.DIALOG.' + dialogPackage)
            .afterClosed()
            .subscribe((confirmed: boolean) => {
                if (confirmed) {
                    this.sendSelection(new Selection3D(this.selections.toJS()), this.labelComment);
                }
            });
        } else {
            this.sendSelection(new Selection3D(this.selections.toJS()), this.labelComment);
        }
    }

    private checkForSingleSliceSelection(): boolean {
        const sliceIndex = (this.selections.first() as SliceSelection).sliceIndex;
        return this.selections.every((selection) => selection.sliceIndex === sliceIndex);
    }

    private checkForIncompleteTagSelections(): boolean {
        // So now we need 2x selections from each tag
        let tagsWithoutSelections = this.labelExplorer.getTags().concat(this.labelExplorer.getTags());
        console.log(tagsWithoutSelections);

        let tagId;
        this.selections.forEach((selection) => {
            tagId = tagsWithoutSelections.findIndex((tag) => tag.key === selection.labelTag.key);
            if (tagId >= 0) {
                tagsWithoutSelections = tagsWithoutSelections.remove(tagId);
            }
        });

        return tagsWithoutSelections.size !== 0;
    }

    public sendEmptyLabel(): void {
        this.dialogService
            .openTranslatedConfirmDialog('MARKER.DIALOG.EMPTY_LABEL')
            .afterClosed()
            .subscribe((confirmed: boolean) => {
                if (confirmed) {
                    this.sendSelection(new Selection3D(), 'This is an empty Label');
                }
            });
    }

    private sendSelection(selection3d: Selection3D, comment: string) {
        const labelingTime = this.getLabelingTimeInSeconds(this.startTime);
        this.taskStatus.changeStatusOperation(Operation.SENDING_SELECTION);
        this.taskStatus.updateProgress();

        this.scanService
            .sendSelection(this.scan.scanId, this.task.key, selection3d, labelingTime, comment)
            .then((response: Response) => {
                console.log('MarkerPage | sendSelection | success!');
                this.indicateLabelHasBeenSend();
                this.nextScan();
            })
            .catch((errorResponse: Error) => {
                this.taskStatus.changeStatusOperation(Operation.DOWNLOADING_ERROR);
                this.dialogService.openTranslatedInfoDialog('MARKER.DIALOG.SEND_ERROR');
            });
    }

    private getLabelingTimeInSeconds(startTime: Date): number {
        const endTime = new Date();
        return (endTime.getTime() - startTime.getTime()) / 1000.0;
    }

    private indicateLabelHasBeenSend(): void {
        this.snackBar.open(this.translateService.instant('MARKER.LABEL_SEND_INFO'), '', { duration: 2000 });
    }

    private indicateNewScanAppeared(): void {
        this.snackBar.open(this.translateService.instant('MARKER.SCAN_LOADED_INFO'), '', { duration: 2000 });
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

        const supportedTools = this.tools.filter((tool: Tool<SliceSelection>) => this.isToolSupportedByCurrentTag(tool.getToolName()));
        if (supportedTools.size === 1) {
            this.setTool(supportedTools.get(0).getToolName());
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
                if (comment !== undefined) {
                    this.labelComment = comment;
                }
                this.marker.setSliderFocus(true);
            });
    }

    private hasTaskDescription(): boolean {
        return !!this.taskDescription;
    }

    public toggleTaskDescriptionPanel(): void {
        this.taskDescriptionPanelActive = !this.taskDescriptionPanelActive;
    }

    public toggleColorWindowPanel(): void {
        this.colorWindowPanelActive = !this.colorWindowPanelActive;
    }

    public resetColorWindowPanel(): void {
        this.colorWindowWidth = MarkerPageComponent.DEFAULT_COLOR_WINDOW_WIDTH;
        this.colorWindowCenter = MarkerPageComponent.DEFAULT_COLOR_WINDOW_CENTER;
        this.rescaleImageColorWindow();
    }

    public changeImageWindowWidth(newValue: number): void {
        this.colorWindowWidth = newValue;
        this.rescaleImageColorWindow();
    }

    public changeImageWindowCenter(newValue: number): void {
        this.colorWindowCenter = newValue;
        this.rescaleImageColorWindow();
    }

    private rescaleImageColorWindow(): void {
        this.marker.modifyViewerImage(this.applyWindowScaling.bind(this));
    }

    private applyWindowScaling(imageRGBBytes: Uint8ClampedArray): Uint8ClampedArray {
        const lowestVisibleValue = this.colorWindowCenter - (this.colorWindowWidth / 2);
        const highestVisibleValue = this.colorWindowCenter + (this.colorWindowWidth / 2);

        for (let i = 0; i < imageRGBBytes.length; i += 4) {

            const greyScaleValue = imageRGBBytes[i]; // red channel here, same as the next two beeing greyscale image
            const alpha = imageRGBBytes[i + 3];

            if (alpha === 0) {
                continue;
            }

            let pixelValue;
            if (greyScaleValue <= lowestVisibleValue) {
                pixelValue = 0;
            } else if (greyScaleValue > highestVisibleValue) {
                pixelValue = 255;
            } else {
                pixelValue = (((greyScaleValue - (this.colorWindowCenter - 0.5)) / (this.colorWindowWidth - 1)) + 0.5) * 255;
            }


            imageRGBBytes[i] = imageRGBBytes[i + 1] = imageRGBBytes[i + 2] = pixelValue;
            imageRGBBytes[i + 3] = 255;
        }

        return imageRGBBytes;
    }
}
