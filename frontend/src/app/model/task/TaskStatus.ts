/**
 * Operations with associated resource key name
 */
export enum Operation {
    SENDING_SELECTION = 'OPERATION.SENDING_SELECTION',
    LABELLING = 'OPERATION.LABELLING',
    DOWNLOADING_SLICES = 'OPERATION.DOWNLOADING_SLICES',
    DOWNLOADING_SCAN = 'OPERATION.DOWNLOADING_SCAN',
    WAITING = 'OPERATION.WAITING',
    DOWNLOADING_ERROR = 'OPERATION.DOWNLOADING_ERROR',
    DRAG_TO_SELECT = 'OPERATION.DRAG_TO_SELECT',
    CLICK_TO_SELECT = 'OPERATION.CLICK_TO_SELECT',
    CHOOSE_TAG = 'OPERATION.CHOOSE_TAG',
    CHOOSE_TOOL = 'OPERATION.CHOOSE_TOOL'
}

export class TaskStatus {
    private _labellingTime: number;
    private _scansToLabel: number;
    private _currentProgress: number;
    private _operation: Operation;

    constructor(scansToLabel: number) {
        this._labellingTime = Date.now();
        this._scansToLabel = scansToLabel;
        this._currentProgress = 1;
        this._operation = Operation.WAITING;
    }

    public get labellingTime(): number {
        return this._labellingTime;
    }

    public get scansToLabel(): number {
        return this._scansToLabel;
    }

    public get currentProgress(): number {
        return this._currentProgress;
    }

    public get operation(): Operation {
        return this._operation;
    }

    public changeStatusOperation(operation: Operation) {
        this._operation = operation;
    }

    public updateProgress() {
        this._currentProgress++;
    }
}
