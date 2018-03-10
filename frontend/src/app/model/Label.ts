import {SliceSelection} from './SliceSelection';

export class Label {
    labelId: string;
    scanId: string;
    labelStatus: string;
    labelSelections: SliceSelection[];

    constructor(labelId: string, scanId: string, status: string, selections: SliceSelection[]) {
        this.labelId = labelId;
        this.scanId = scanId;
        this.labelStatus = status;
        this.labelSelections = selections;
    }
}
