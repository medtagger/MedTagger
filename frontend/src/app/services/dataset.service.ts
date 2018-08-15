import {Injectable} from '@angular/core';
import {Dataset} from '../model/ScanMetadata';
import {environment} from '../../environments/environment';
import {HttpClient} from '@angular/common/http';

interface AvailableDatasetResponse {
    key: string;
    name: string;
}

@Injectable()
export class DatasetService {
    constructor(private http: HttpClient) {
    }

    getAvailableDatasets(): Promise<Dataset[]> {
        return new Promise((resolve, reject) => {
            this.http.get<Array<AvailableDatasetResponse>>(environment.API_URL + '/scans/datasets').toPromise().then(
                response => {
                    console.log('DatasetService | getAvailableDatasets | response: ', response);
                    const datasets = [];
                    for (const dataset of response) {
                        datasets.push(new Dataset(dataset.key, dataset.name));
                    }
                    resolve(datasets);
                },
                error => {
                    console.log('DatasetService | getAvailableDatasets | error: ', error);
                    reject(error);
                }
            );
        });
    }
}

