import {SliceSelection} from '../selections/SliceSelection';

export class Label {
    labelId: string;
    scanId: string;
    labelStatus: string;
    labelingTime: number;
    labelComment: string;
    labelSelections: SliceSelection[];

    constructor(labelId: string, scanId: string, status: string, selections: SliceSelection[], labelingTime: number, labelComment: string) {
        this.labelId = labelId;
        this.scanId = scanId;
        this.labelStatus = status;
        this.labelSelections = selections;
        this.labelingTime = labelingTime;
        this.labelComment = labelComment;
    }
}
