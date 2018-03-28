import {Injectable} from '@angular/core';
import {Response} from '@angular/http';
import {HttpClient, HttpParams} from '@angular/common/http';

import {Socket} from 'ng-socket-io';
import 'rxjs/add/operator/map';
import 'rxjs/add/operator/toPromise';
import {Observable} from 'rxjs/Observable';
import {ScanCategory, ScanMetadata} from '../model/ScanMetadata';
import {MarkerSlice} from '../model/MarkerSlice';

import {environment} from '../../environments/environment';
import {ScanSelection} from "../model/ScanSelection";
import {SliceSelection} from "../model/SliceSelection";

interface RandomScanResponse {
    scan_id: string;
    number_of_slices: number;
}

interface ScanForScanIDResponse {
    scan_id: string;
    number_of_slices: number;
}

interface AvailableCategoryResponse {
    key: string;
    name: string;
    image_path: string;
}

interface NewScanResponse {
    scan_id: string;
}

@Injectable()
export class ScanService {

    websocket: Socket;

    constructor(private http: HttpClient) {
        this.websocket = new Socket({url: environment.WEBSOCKET_URL + '/slices', options: {}});
    }

    public sendSelection(scanId: string, selection: ScanSelection<SliceSelection>, labelingTime: number): Promise<Response> {
        console.log('ScanService | send3dSelection | sending ROI:', selection, `for scanId: ${scanId}`, `with labeling time: ${labelingTime}`);
        const payload = selection.toJSON();
        payload['labeling_time'] = labelingTime;
        return new Promise((resolve, reject) => {
            this.http.post(environment.API_URL + `/scans/${scanId}/label`, payload).toPromise().then((response: Response) => {
                console.log('ScanService | send3dSelection | response: ', response);
                resolve(response);
            }).catch((error: Response) => {
                console.log('ScanService | send3dSelection | error: ', error);
                reject(error);
            });
        });
    }

    public getRandomScan(category: string): Promise<ScanMetadata> {
        return new Promise((resolve, reject) => {
            var params = new HttpParams();
            params = params.set('category', category);
            this.http.get<RandomScanResponse>(environment.API_URL + '/scans/random', {params: params})
                .subscribe(
                    (response) => {
                        console.log('ScanService | getRandomScan | response: ', response);
                        resolve(new ScanMetadata(response.scan_id, response.number_of_slices));
                    },
                    (error) => {
                        console.log('ScanService | getRandomScan | error: ', error);
                        reject(error);
                    },
                    () => {
                        console.log('ScanService | getRandomScan | done');
                    });
        });
    }

    getScanForScanId(scanId: string): Promise<ScanMetadata> {
        return new Promise((resolve, reject) => {
            this.http.get<ScanForScanIDResponse>(environment.API_URL + '/scans/' + scanId).toPromise().then(
                response => {
                    console.log('ScanService | getScanForScanId | response: ', response);
                    resolve(new ScanMetadata(response.scan_id, response.number_of_slices));
                },
                error => {
                    console.log('ScanService | getRandomScan | error: ', error);
                    reject(error);
                }
            );
        });
    }

    getAvailableCategories(): Promise<ScanCategory[]> {
        return new Promise((resolve, reject) => {
            this.http.get<Array<AvailableCategoryResponse>>(environment.API_URL + '/scans/categories').toPromise().then(
                response => {
                    console.log('ScanService | getAvailableCategories | response: ', response);
                    const categories = [];
                    for (let category of response) {
                        categories.push(new ScanCategory(category.key, category.name, category.image_path))
                    }
                    resolve(categories);
                },
                error => {
                    console.log('ScanService | getAvailableCategories | error: ', error);
                    reject(error);
                }
            );
        });
    }

    slicesObservable(): Observable<MarkerSlice> {
        return this.websocket.fromEvent<any>('slice').map((slice: { scan_id: string, index: number, image: ArrayBuffer }) => {
            return new MarkerSlice(slice.scan_id, slice.index, slice.image);
        });
    }

    requestSlices(scanId: string, begin: number, count: number) {
        console.log('ScanService | requestSlices | begin:', begin);
        this.websocket.emit('request_slices', {scan_id: scanId, begin: begin, count: count});
    }

    createNewScan(category: string, numberOfSlices: number) {
        return new Promise((resolve, reject) => {
            const payload = {
                category: category,
                number_of_slices: numberOfSlices,
            };
            this.http.post<NewScanResponse>(environment.API_URL + '/scans/', payload).toPromise().then(
                response => {
                    resolve(response.scan_id);
                },
                error => {
                    reject(error);
                }
            );
        });
    }

    uploadSlices(scanId: string, files: File[]) {
        let CONCURRENT_API_CALLS = 5;

        return Observable.from(files)
            .map((file) => {
                let form = new FormData();
                form.append('image', file, file.name);
                return Observable.defer(
                    () => this.http.post(environment.API_URL + '/scans/' + scanId + '/slices', form)
                );
            })
            .mergeAll(CONCURRENT_API_CALLS);
    }
}
