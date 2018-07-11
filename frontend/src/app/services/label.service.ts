import {Injectable} from '@angular/core';

import {environment} from '../../environments/environment';
import {Label} from '../model/Label';
import {HttpClient} from '@angular/common/http';
import {SliceSelection} from '../model/SliceSelection';

interface RandomLabelResponse {
    label_id: string;
    scan_id: string;
    status: string;
    selections: Array<SliceSelection>;
    labeling_time: number;
    comment: string;
}

@Injectable()
export class LabelService {

    constructor(private http: HttpClient) {}

    getRandomLabel(selectionConverter: (selections: any) => Array<SliceSelection>): Promise<Label> {
        return new Promise((resolve, reject) => {
            this.http.get<RandomLabelResponse>(environment.API_URL + '/labels/random').toPromise().then(
                response => {
                    console.log('LabelsService | getRandomLabel | response: ', response);
                    resolve(new Label(response.label_id, response.scan_id, response.status,
                                      selectionConverter(response.selections), response.labeling_time, response.comment));
                },
                error => {
                    console.log('LabelsService | getRandomLabel | error: ', error);
                    reject(error);
                }
            );
        });
    }

    changeStatus(labelId: string, status: string) {
        return new Promise((resolve, reject) => {
            const payload = {'status': status};
            this.http.put(environment.API_URL + '/labels/' + labelId + '/status', payload).toPromise().then(
                response => {
                    resolve();
                },
                error => {
                    reject(error);
                }
            );
        });
    }
}
