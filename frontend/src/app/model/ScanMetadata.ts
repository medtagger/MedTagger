import {Task} from './Task';

export class ScanCategory {
    key: string;
    name: string;
    imagePath: string;
    tasks: Array<Task>;

    constructor(key: string, name: string, imagePath: string, tasks: Array<Task>) {
        this.key = key;
        this.name = name;
        this.imagePath = imagePath;
        this.tasks = tasks;
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
