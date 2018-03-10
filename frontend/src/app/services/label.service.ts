import {Injectable} from '@angular/core';

import {environment} from '../../environments/environment';
import {Label} from '../model/Label';
import {Http} from '@angular/http';
import {SliceSelection} from '../model/SliceSelection';

@Injectable()
export class LabelService {

    constructor(private http: Http) {}

    getRandomLabel(selectionConverter: (selections: any) => Array<SliceSelection>): Promise<Label> {
        return new Promise((resolve, reject) => {
            this.http.get(environment.API_URL + '/labels/random').toPromise().then(
                response => {
                    console.log('LabelsService | getRandomLabel | response: ', response);
                    const json = response.json();
                    resolve(new Label(json.label_id, json.scan_id, json.status, selectionConverter(json.selections), json.labeling_time));
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
