export class ScanMetadata {
  scanId: string;
  numberOfSlices: number;

  constructor(scanId: string, numberOfSlices: number) {
    this.scanId = scanId;
    this.numberOfSlices = numberOfSlices;
  }
}
