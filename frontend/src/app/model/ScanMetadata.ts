import {LabelTag} from './labels/LabelTag';

export class ScanCategory {
    key: string;
    name: string;
    imagePath: string;
    tags: LabelTag[];

    constructor(key: string, name: string, imagePath: string, tags: LabelTag[]) {
        this.key = key;
        this.name = name;
        this.imagePath = imagePath;
        this.tags = tags;
    }
}

export class ScanMetadata {
    scanId: string;
    status: string;
    numberOfSlices: number;
    width: number;
    height: number;

    constructor(scanId: string, status: string, numberOfSlices: number, width: number, height: number) {
        this.scanId = scanId;
        this.status = status;
        this.numberOfSlices = numberOfSlices;
        this.width = width;
        this.height = height;
    }
}
