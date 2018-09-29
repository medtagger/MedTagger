import {async, inject, TestBed} from '@angular/core/testing';
import {HttpClientModule, HttpRequest} from '@angular/common/http';
import {HttpClientTestingModule, HttpTestingController} from '@angular/common/http/testing';
import {environment} from '../../environments/environment';
import {DatasetService} from './dataset.service';
import {Dataset} from '../model/ScanMetadata';
import {API_URL} from '../utils/ApiUrl';

describe('Service: DatasetService', () => {
    const EXAMPLE_DATASETS = [
        {
            name: 'DATASET_NAME_1',
            key: 'DATSET_KEY_1'
        },
        {
            name: 'DATASET_NAME_2',
            key: 'DATSET_KEY_2'
        }];


    beforeEach(() => {
        TestBed.configureTestingModule({
            imports: [
                HttpClientModule,
                HttpClientTestingModule
            ],
            providers: [
                DatasetService
            ]
        });
    });

    it('should get available datasets', async(inject([DatasetService, HttpTestingController],
        (service: DatasetService, backend: HttpTestingController) => {

            service.getAvailableDatasets().then((results: Dataset[]) => {
                expect(results.length).toBe(EXAMPLE_DATASETS.length);
                for (let i = 0; i < EXAMPLE_DATASETS.length; i++) {
                    expect(results[i].key).toBe(EXAMPLE_DATASETS[i].key);
                    expect(results[i].name).toBe(EXAMPLE_DATASETS[i].name);
                }
            });

            backend.expectOne((req: HttpRequest<any>) => {
                return req.url === environment.API_URL + API_URL.DATASETS
                    && req.method === 'GET';
            }, `GET from ${API_URL.DATASETS}`)
                .flush(EXAMPLE_DATASETS,
                    {status: 200, statusText: 'Ok'});
        })));

    it(`shouldn't get available datasets`, async(inject([DatasetService, HttpTestingController],
        (service: DatasetService, backend: HttpTestingController) => {

            service.getAvailableDatasets().catch((error: Error) => {
                expect(error).toBeTruthy();
            });

            backend.expectOne((req: HttpRequest<any>) => {
                return req.url === environment.API_URL + API_URL.DATASETS
                    && req.method === 'GET';
            }, `GET from ${API_URL.DATASETS}`)
                .flush(EXAMPLE_DATASETS,
                    {status: 401, statusText: 'Unauthorized'});
        })));
});
