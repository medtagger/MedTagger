export class ScanCategory {
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

    constructor(scanId: string, status: string, numberOfSlices: number, width: number, height: number) {
        this.scanId = scanId;
        this.status = status;
        this.numberOfSlices = numberOfSlices;
        this.width = width;
        this.height = height;
    }
}
