import {throwError as observableThrowError, Observable} from 'rxjs';
import {Injectable} from '@angular/core';
import {HttpClient, HttpParams, HttpErrorResponse} from '@angular/common/http';

import {ScanMetadata} from '../model/ScanMetadata';
import {MarkerSlice} from '../model/MarkerSlice';

import {API_URL} from '../utils/ApiUrl';
import {environment} from '../../environments/environment';
import {ScanSelection} from '../model/selections/ScanSelection';
import {SliceSelection} from '../model/selections/SliceSelection';
import {MedTaggerWebSocket} from './websocket.service';
import {concat, delay, map, mergeAll, retryWhen, take} from 'rxjs/operators';
import {of} from 'rxjs/internal/observable/of';
import {from} from 'rxjs/internal/observable/from';
import {defer} from 'rxjs/internal/observable/defer';
import {TaskResponse} from './task.service';
import {isUndefined} from 'util';
import {PredefinedBrushLabelElement} from '../model/PredefinedBrushLabelElement';

interface ScanResponse {
    scan_id: string;
    status: string;
    number_of_slices: number;
    width: number;
    height: number;
    predefined_label_id: string;
}

interface AvailableDatasetResponse {
    key: string;
    name: string;
    tasks: Array<TaskResponse>;
}

interface LabelTagResponse {
    key: string;
    name: string;
    actions_id: Array<number>;
}

interface NewScanResponse {
    scan_id: string;
}

@Injectable()
export class ScanService {

    websocket: MedTaggerWebSocket;

    delay = 5000;
    retries = 5;

    constructor(private http: HttpClient, private socket: MedTaggerWebSocket) {
        this.websocket = socket;
    }

    sendSelection(scanId: string, taskKey: string, selection: ScanSelection<SliceSelection>, labelingTime: number,
                         comment: string): Promise<Response> {
        console.log('ScanService | send3dSelection | sending 3D selection:',
            selection, `for scanId: ${scanId}`, `with labeling time: ${labelingTime}`);

        const payload = selection.toJSON();
        payload['labeling_time'] = labelingTime;
        payload['comment'] = comment;

        const form = new FormData();
        form.append('label', JSON.stringify(payload));

        const additionalData = selection.getAdditionalData();
        for (const key of Object.keys(additionalData)) {
            const value = additionalData[key];
            form.append(key, value, key);
        }

        return new Promise((resolve, reject) => {
            this.http.post(environment.API_URL + API_URL.SCANS + `/${scanId}/${taskKey}/label`, form).toPromise().then((response: Response) => {
                console.log('ScanService | send3dSelection | response: ', response);
                resolve(response);
            }).catch((error: Response) => {
                console.log('ScanService | send3dSelection | error: ', error);
                reject(error);
            });
        });
    }

    public sendPredefinedLabel(scanId: string, taskKey: string, label: Object, additionalData: Object): Promise<Response> {
        const form = new FormData();
        form.append('label', JSON.stringify(label));

        for (const key of Object.keys(additionalData)) {
            const value = additionalData[key];
            form.append(key, value, key);
        }

        return new Promise((resolve, reject) => {
            this.http.post(environment.API_URL + API_URL.SCANS + `/${scanId}/${taskKey}/label?is_predefined=true`, form).toPromise()
                .then((response: Response) => {
                    console.log('ScanService | sendPredefinedLabel | response: ', response);
                    resolve(response);
                }).catch((error: Response) => {
                    console.log('ScanService | sendPredefinedLabel | error: ', error);
                    reject(error);
                });
        });
    }

    public getRandomScan(taskKey: string): Promise<ScanMetadata> {
        if (isUndefined(taskKey)) {
            return Promise.reject('ScanService | getRandomScan | error: Task key is undefined!');
        }
        return new Promise((resolve, reject) => {
            let params = new HttpParams();
            params = params.set('task', taskKey);
            this.http.get<ScanResponse>(environment.API_URL + API_URL.SCANS + '/random', {params: params})
                .subscribe(
                    (response: ScanResponse) => {
                        console.log('ScanService | getRandomScan | response: ', response);
                        resolve(new ScanMetadata(response.scan_id, response.status, response.number_of_slices,
                            response.width, response.height, response.predefined_label_id));
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
            this.http.get<ScanResponse>(environment.API_URL + API_URL.SCANS + '/' + scanId).toPromise().then(
                (response: ScanResponse) => {
                    console.log('ScanService | getScanForScanId | response: ', response);
                    resolve(new ScanMetadata(response.scan_id, response.status, response.number_of_slices,
                        response.width, response.height, undefined));
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

    predefinedBrushLabelElementsObservable(): Observable<PredefinedBrushLabelElement> {
        return this.websocket.fromEvent<any>('brush_labels').pipe(
            map((label: { scan_id: string, tag_key: string, index: number, image: ArrayBuffer }) => {
                return new PredefinedBrushLabelElement(label.scan_id, label.tag_key, label.index, label.image);
            })
        );
    }

    requestSlices(scanId: string, taskKey: string, begin: number, count: number, reversed: boolean = false): void {
        console.log('ScanService | requestSlices | begin:', begin);
        this.websocket.emit('request_slices', {
            scan_id: scanId,
            task_key: taskKey,
            begin: begin,
            count: count,
            reversed: reversed,
        });
    }

    createNewScan(dataset: string, numberOfSlices: number): Promise<string> {
        return new Promise((resolve, reject) => {
            const payload = {
                dataset: dataset,
                number_of_slices: numberOfSlices,
            };
            let retryAttempt = 0;
            this.http.post<NewScanResponse>(environment.API_URL + API_URL.SCANS, payload)
                .pipe(
                    retryWhen((error: Observable<HttpErrorResponse>) => {
                        return error.pipe(
                            map((scanRequestError: HttpErrorResponse) => {
                                console.warn('Retrying request for creating new Scan (attempt: ' + (++retryAttempt) + ').');
                                return of(scanRequestError.status);
                            }),
                            delay(this.delay), // Let's give it a try after 5 seconds
                            take(this.retries), // Let's give it 5 retries (each after 5 seconds)
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

    uploadSlices(scanId: string, files: File[]): Observable<any> {
        const CONCURRENT_API_CALLS = 5;

        return from(files).pipe(
            map((file: File) => {
                console.log('Uploading file...', file.name);
                let retryAttempt = 0;
                const form = new FormData();
                form.append('image', file, file.name);
                return defer(
                    () => this.http.post(environment.API_URL + API_URL.SCANS + '/' + scanId + '/slices', form)
                        .pipe(
                            retryWhen((error: Observable<HttpErrorResponse>) => {
                                return error.pipe(
                                    map((uploadRequestError: HttpErrorResponse) => {
                                        console.warn('Retrying request for uploading a single Slice ('
                                            + file.name + ', attempt: ' + (++retryAttempt) + ').');
                                        return of(uploadRequestError.status);
                                    }),
                                    delay(this.delay),  // Let's give it a try after 5 seconds
                                    take(this.retries),  // Let's give it 5 retries (each after 5 seconds)
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
            this.http.post(environment.API_URL + API_URL.SCANS + `/${scanId}/skip`, {}).toPromise().then((response: Response) => {
                console.log('ScanService | skipScan | response: ', response);
                resolve(response);
            }).catch((error: Response) => {
                console.log('ScanService | skipScan | error: ', error);
                reject(error);
            });
        });
    }
}
