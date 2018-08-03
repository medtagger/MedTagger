import {throwError as observableThrowError, Observable} from 'rxjs';
import {Injectable} from '@angular/core';
import {HttpClient, HttpParams, HttpErrorResponse} from '@angular/common/http';

import {ScanMetadata} from '../model/ScanMetadata';
import {MarkerSlice} from '../model/MarkerSlice';

import {environment} from '../../environments/environment';
import {ScanSelection} from '../model/ScanSelection';
import {SliceSelection} from '../model/SliceSelection';
import {MedTaggerWebSocket} from './websocket.service';
import {concat, delay, flatMap, map, mergeAll, retryWhen, take} from 'rxjs/operators';
import {of} from 'rxjs/internal/observable/of';
import {from} from 'rxjs/internal/observable/from';
import {defer} from 'rxjs/internal/observable/defer';

interface ScanResponse {
    scan_id: string;
    status: string;
    number_of_slices: number;
    width: number;
    height: number;
}

interface NewScanResponse {
    scan_id: string;
}

@Injectable()
export class ScanService {

    websocket: MedTaggerWebSocket;

    constructor(private http: HttpClient, private socket: MedTaggerWebSocket) {
        this.websocket = socket;
    }

    public sendSelection(scanId: string, selection: ScanSelection<SliceSelection>, labelingTime: number): Promise<Response> {
        console.log('ScanService | send3dSelection | sending ROI:',
            selection, `for scanId: ${scanId}`, `with labeling time: ${labelingTime}`);

        const payload = selection.toJSON();
        payload['labeling_time'] = labelingTime;
        const form = new FormData();
        form.append('label', JSON.stringify(payload));
        return new Promise((resolve, reject) => {
            this.http.post(environment.API_URL + `/scans/${scanId}/label`, form).toPromise().then((response: Response) => {
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
            let params = new HttpParams();
            params = params.set('category', category);
            this.http.get<ScanResponse>(environment.API_URL + '/scans/random', {params: params})
                .subscribe(
                    (response: ScanResponse) => {
                        console.log('ScanService | getRandomScan | response: ', response);
                        resolve(new ScanMetadata(response.scan_id, response.status, response.number_of_slices,
                            response.width, response.height));
                    },
                    (error: Error) => {
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
            this.http.get<ScanResponse>(environment.API_URL + '/scans/' + scanId).toPromise().then(
                (response: ScanResponse) => {
                    console.log('ScanService | getScanForScanId | response: ', response);
                    resolve(new ScanMetadata(response.scan_id, response.status, response.number_of_slices,
                        response.width, response.height));
                },
                (error: Error) => {
                    console.log('ScanService | getScanForScanId | error: ', error);
                    reject(error);
                }
            );
        });
    }

    slicesObservable(): Observable<MarkerSlice> {
        return this.websocket.fromEvent<any>('slice').pipe(
            map((slice: { scan_id: string, index: number, last_in_batch: number, image: ArrayBuffer }) => {
                return new MarkerSlice(slice.scan_id, slice.index, slice.last_in_batch, slice.image);
            })
        );
    }

    requestSlices(scanId: string, begin: number, count: number, reversed: boolean) {
        console.log('ScanService | requestSlices | begin:', begin);
        this.websocket.emit('request_slices', {scan_id: scanId, begin: begin, count: count, reversed: reversed});
    }

    createNewScan(category: string, numberOfSlices: number) {
        return new Promise((resolve, reject) => {
            const payload = {
                category: category,
                number_of_slices: numberOfSlices,
            };
            let retryAttempt = 0;
            this.http.post<NewScanResponse>(environment.API_URL + '/scans/', payload)
                .pipe(
                    retryWhen((error: Observable<HttpErrorResponse>) => {
                        return error.pipe(
                            map((scanRequestError: HttpErrorResponse) => {
                                console.warn('Retrying request for creating new Scan (attempt: ' + (++retryAttempt) + ').');
                                return of(scanRequestError.status);
                            }),
                            delay(5000), // Let's give it a try after 5 seconds
                            take(5), // Let's give it 5 retries (each after 5 seconds)
                            concat(observableThrowError({error: 'Cannot create new Scan.'}))
                        );
                    })
                ).toPromise().then(
                (response: NewScanResponse) => {
                    resolve(response.scan_id);
                },
                (error: HttpErrorResponse) => {
                    reject(error);
                }
            );
        });
    }

    uploadSlices(scanId: string, files: File[]) {
        const CONCURRENT_API_CALLS = 5;

        return from(files).pipe(
            map((file: File) => {
                console.log('Uploading file...', file);
                let retryAttempt = 0;
                const form = new FormData();
                form.append('image', file, file.name);
                return defer(
                    () => this.http.post(environment.API_URL + '/scans/' + scanId + '/slices', form)
                        .pipe(
                            retryWhen((error: Observable<HttpErrorResponse>) => {
                                return error.pipe(
                                    map((uploadRequestError: HttpErrorResponse) => {
                                        console.warn('Retrying request for uploading a single Slice ('
                                            + file.name + ', attempt: ' + (++retryAttempt) + ').');
                                        return of(uploadRequestError.status);
                                    }),
                                    delay(5000),  // Let's give it a try after 5 seconds
                                    take(5),  // Let's give it 5 retries (each after 5 seconds)
                                    concat(observableThrowError({error: 'Cannot upload Slice ' + file.name}))
                                );
                            })
                        )
                );
            }),
            mergeAll(CONCURRENT_API_CALLS)
        );
    }

    skipScan(scanId: string): Promise<Response> {
        return new Promise((resolve, reject) => {
            this.http.post(environment.API_URL + `/scans/${scanId}/skip`, {}).toPromise().then((response: Response) => {
                console.log('ScanService | skipScan | response: ', response);
                resolve(response);
            }).catch((error: Response) => {
                console.log('ScanService | skipScan | error: ', error);
                reject(error);
            });
        });
    }
}
