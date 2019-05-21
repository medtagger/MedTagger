/**
 * Operations with associated resource key name
 */
enum Operation {
    SENDING_SELECTION = 'OPERATION.SENDING_SELECTION',
    LABELLING = 'OPERATION.LABELLING',
    DOWNLOADING_SLICES = 'OPERATION.DOWNLOADING_SLICES',
    DOWNLOADING_SCAN = 'OPERATION.DOWNLOADING_SCAN',
    DRAG_TO_SELECT = 'OPERATION.DRAG_TO_SELECT',
    CLICK_TO_SELECT = 'OPERATION.CLICK_TO_SELECT',
    CHOOSE_TAG = 'OPERATION.CHOOSE_TAG',
    CHOOSE_TOOL = 'OPERATION.CHOOSE_TOOL'
}

export class TaskStatus {

    public labellingTime: number;
    private scansToLabel: number;
    private currentProgress: number;
    private operation: Operation;

    constructor(scansToLabel: number) {
        this.labellingTime = Date.now();
        this.scansToLabel = scansToLabel;
        this.currentProgress = 1;
        this.operation = Operation.CHOOSE_TOOL;
    }

    public changeStatusOperation(operation: Operation) {
        this.operation = operation;
    }

    public updateProgress() {
        this.currentProgress++;
    }
}