import { Injectable } from '@angular/core';
import { Http } from '@angular/http';

import { Socket } from 'ng-socket-io';
import 'rxjs/add/operator/map';
import 'rxjs/add/operator/toPromise';


export class Scan {
  scanId: string;
  numberOfSlices: number;
}

export class Slice {
  scanId: string;
  index: number;
  image: ArrayBuffer;
}


@Injectable()
export class ScanService {

  // TODO: Move this URLs somewhere else!
  SCANS_API_URL: string = 'http://localhost:51000/api/v1/scans';
  SLICES_WEBSOCKET: string = 'http://localhost:51000/slices';
  websocket: Socket;

  constructor(private http: Http) {
    this.websocket = new Socket({url: this.SLICES_WEBSOCKET, options: {}});
  }

  getRandomScan() {
    return new Promise((resolve, reject) => {
      this.http.get(this.SCANS_API_URL + '/random').toPromise().then(
        response => {
          let json = response.json();
          resolve({scanId: json.scan_id, numberOfSlices: json.number_of_slices});
        },
        error => {
          reject(error);
        }
      );
    });
  }

  acknowledgeObservable() {
    return this.websocket.fromEvent<any>('ack').map(() => {
      return true;
    });
  }

  slicesObservable() {
    return this.websocket.fromEvent<any>('slice').map(slice => {
      return {scanId: slice.scan_id, index: slice.index, image: slice.image};
    });
  }

  requestSlices(scanId: string, begin: number, count: number) {
    this.websocket.emit('request_slices', {scan_id: scanId, begin: begin, count: count});
  }

  createNewScan() {
    return new Promise((resolve, reject) => {
      let payload = {};
      this.http.post(this.SCANS_API_URL + '/', payload).toPromise().then(
        response => {
          resolve(response.json().scan_id);
        },
        error => {
          reject(error);
        }
      );
    });
  }

  uploadSlices(scanId: string, files: File[], currentFileUpload: number = 0) {
    // Upload completed
    if (currentFileUpload == files.length) {
      return;
    }

    // Continue reading files from list
    let fileReader = new FileReader();
    fileReader.onload = () => {
      let image = fileReader.result;
      this.websocket.emit('upload_slice', {scan_id: scanId, image: image}, () => {
        // Let's send another file from the list after completed upload
        this.uploadSlices(scanId, files, currentFileUpload + 1);
      });
    };
    fileReader.readAsArrayBuffer(files[currentFileUpload]);
  }

}
