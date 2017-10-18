import { Injectable } from '@angular/core';
import { Http } from '@angular/http';

import { Socket } from 'ng-socket-io';
import 'rxjs/add/operator/map';
import 'rxjs/add/operator/toPromise';


export class Slice {
  scanId: string;
  index: number;
  image: ArrayBuffer;
}


@Injectable()
export class ScanService {

  SCANS_API_URL: string = 'http://localhost:51000/api/v1/scans';
  websocket: Socket;

  constructor(private http: Http) {
    // TODO: Move this URLs somewhere else!
    this.websocket = new Socket({ url: 'http://localhost:51000/slices', options: {} });
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

  uploadSlice(scanId: string, image: ArrayBuffer) {
    this.websocket.emit('upload_slice', {scan_id: scanId, image: image});
  }

}
