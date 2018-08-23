import {LabelTag} from './labels/LabelTag';

export class Dataset {
    key: string;
    name: string;

    constructor(key: string, name: string) {
        this.key = key;
        this.name = name;
    }
}

export class ScanMetadata {
    scanId: string;
    status: string;
    numberOfSlices: number;
    width: number;
    height: number;
    predefinedLabelID: string;

    constructor(scanId: string, status: string, numberOfSlices: number, width: number, height: number,
                predefinedLabelID: string) {
        this.scanId = scanId;
        this.status = status;
        this.numberOfSlices = numberOfSlices;
        this.width = width;
        this.height = height;
        this.predefinedLabelID = predefinedLabelID;
    }
}
