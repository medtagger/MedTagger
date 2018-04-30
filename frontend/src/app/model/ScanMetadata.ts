export class ScanCategory {
    key: string;
    name: string;
    imagePath: string;

    constructor(key: string, name: string, imagePath: string) {
        this.key = key;
        this.name = name;
        this.imagePath = imagePath;
    }
}

export class ScanMetadata {
    scanId: string;
    status: string;
    numberOfSlices: number;

    constructor(scanId: string, status: string, numberOfSlices: number) {
        this.scanId = scanId;
        this.status = status;
        this.numberOfSlices = numberOfSlices;
    }
}
