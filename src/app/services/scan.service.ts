import {Injectable} from '@angular/core';
import {Http} from '@angular/http';

import {Socket} from 'ng-socket-io';
import 'rxjs/add/operator/map';
import 'rxjs/add/operator/toPromise';
import {Observable} from 'rxjs/Observable';
import {ScanMetadata} from '../model/ScanMetadata';
import {MarkerSlice} from '../model/MarkerSlice';

import { environment } from '../../environments/environment';


@Injectable()
export class ScanService {

  websocket: Socket;

  constructor(private http: Http) {
    this.websocket = new Socket({url: environment.WEBSOCKET_URL + '/slices', options: {}});
  }

  getRandomScan(): Promise<ScanMetadata> {
    return new Promise((resolve, reject) => {
      this.http.get(environment.API_URL + '/scans/random').toPromise().then(
        response => {
          console.log('ScanService | getRandomScan | response: ', response);
          const json = response.json();
          resolve(new ScanMetadata(json.scan_id, json.number_of_slices));
        },
        error => {
          console.log('ScanService | getRandomScan | error: ', error);
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

  slicesObservable(): Observable<MarkerSlice> {
    return this.websocket.fromEvent<any>('slice').map((slice: { scan_id: string, index: number, image: ArrayBuffer }) => {
      return new MarkerSlice(slice.scan_id, slice.index, slice.image);
    });
  }

  requestSlices(scanId: string, begin: number, count: number) {
    this.websocket.emit('request_slices', {scan_id: scanId, begin: begin, count: count});
  }

  createNewScan() {
    return new Promise((resolve, reject) => {
      const payload = {};
      this.http.post(environment.API_URL + '/scans/', payload).toPromise().then(
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
    if (currentFileUpload === files.length) {
      return;
    }

    // Continue reading files from list
    const fileReader = new FileReader();
    fileReader.onload = () => {
      const image = fileReader.result;
      this.websocket.emit('upload_slice', {scan_id: scanId, image: image}, () => {
        // Let's send another file from the list after completed upload
        this.uploadSlices(scanId, files, currentFileUpload + 1);
      });
    };
    fileReader.readAsArrayBuffer(files[currentFileUpload]);
  }
}
