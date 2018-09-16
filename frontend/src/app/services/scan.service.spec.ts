import {async, fakeAsync, inject, TestBed, tick} from '@angular/core/testing';
import {HttpClient, HttpClientModule, HttpErrorResponse, HttpRequest} from '@angular/common/http';
import {HttpClientTestingModule, HttpTestingController} from '@angular/common/http/testing';
import {ScanService} from './scan.service';
import {environment} from '../../environments/environment';
import {SliceSelection} from '../model/selections/SliceSelection';
import {Selection3D} from '../model/selections/Selection3D';
import {MedTaggerWebSocket} from './websocket.service';
import {ScanMetadata} from '../model/ScanMetadata';
import {MarkerSlice} from '../model/MarkerSlice';
import {of} from 'rxjs';
import {WrappedSocket} from 'ng-socket-io/dist/src/socket-io.service';
import {SelectedScan} from '../components/upload-scans-selector/upload-scans-selector.component';

class MockSelection extends SliceSelection {
    constructor(sliceIndex: number,
                label_tool: string,
                label_tag: string) {
        super();

        this.sliceIndex = sliceIndex;
        this.label_tag = label_tag;
        this.label_tool = label_tool;

        this.pinned = false;
        this.hidden = false;
    }

    getAdditionalData(): Object {
        return {
            EXAMPLE_PARAM_1: 1337,
            EXAMPLE_PARAM_2: this.label_tool + this.label_tag,
            EXAMPLE_PARAM_3: {
                EXAMPLE_PARAM_3_1: 'Example'
            }
        };
    }

    toJSON(): Object {
        return {
            'width': 1,
            'height': 1,
            'slice_index': this.sliceIndex,
            'tag': this.label_tag,
            'tool': this.label_tool
        };
    }
}

const fakeMedTaggerSocket: WrappedSocket = new WrappedSocket({url: environment.WEBSOCKET_URL + '/slices'});

describe('Service: ScanService', () => {
    const MOCK_SELECTION: MockSelection = new MockSelection(1, 'MOCK', 'MOCK');

    const EXAMPLE_DATA = {
        SCAN_ID: '1',
        TASK_KEY: 'NODULE',
        LABELING_TIME: 1337,
        COMMENT: 'Example comment',
        ADDITIONAL_DATA: MOCK_SELECTION.getAdditionalData(),
        LABEL_ID: '36026be2-b475-4f68-9b2f-295afcee2460',
        OWNER_ID: '1',
        STATUS: 'LabelVerificationStatus.NOT_VERIFIED',
        DATASET: 'Example dataset',
        NUM_SLICES: 1337
    };

    const MOCK_SCAN_METADATA: ScanMetadata = new ScanMetadata(EXAMPLE_DATA.SCAN_ID,
        EXAMPLE_DATA.STATUS, 50, 512, 512);

    const MOCK_MARKER_SLICE_RAW = {
        scan_id: '1',
        index: 1,
        last_in_batch: 50,
        image: new ArrayBuffer(256)
    };
    const MOCK_MARKER_SLICE: MarkerSlice =
        new MarkerSlice(
            MOCK_MARKER_SLICE_RAW.scan_id,
            MOCK_MARKER_SLICE_RAW.index,
            MOCK_MARKER_SLICE_RAW.last_in_batch,
            MOCK_MARKER_SLICE_RAW.image);

    const MOCK_UPLOAD_SCAN: SelectedScan = {
        directory: 'Example',
        files: [
            new File(['Example file 1'], 'file1'),
            new File(['Example file 2'], 'file2'),
            new File(['Example file 3'], 'file3'),
            new File(['Example file 4'], 'file4'),
            new File(['Example file 5'], 'file5')
        ]
    };

    const MOCK_FUNCTIONS = {
        onSubscribe: function (response: any) {
        },
        onSubscribeError: function (error: Error) {
        }
    };

    const API_URL = {
        SEND_SCAN: `/scans/${EXAMPLE_DATA.SCAN_ID}/${EXAMPLE_DATA.TASK_KEY}/label`,
        GET_RANDOM_SCAN: '/scans/random',
        SCANS: '/scans/',
        SLICES: '/slices',
        SKIP: '/skip'
    };

    let http: HttpClient;

    beforeEach(() => {
        TestBed.configureTestingModule({
            imports: [
                HttpClientModule,
                HttpClientTestingModule,
            ],
            providers: [
                ScanService, {provide: MedTaggerWebSocket, useValue: fakeMedTaggerSocket}
            ]
        });

        http = TestBed.get(HttpClient);
    });

    it(`should send selection`, async(inject([ScanService, HttpTestingController],
        (service: ScanService, backend: HttpTestingController) => {

            service.sendSelection(EXAMPLE_DATA.SCAN_ID,
                EXAMPLE_DATA.TASK_KEY,
                new Selection3D([MOCK_SELECTION]),
                EXAMPLE_DATA.LABELING_TIME,
                EXAMPLE_DATA.COMMENT)
                .then((response: Response) => {
                    expect(response).toBeTruthy();
                });

            backend.expectOne((req: HttpRequest<any>) => {
                let additionalDataValid = true;
                const formData: FormData = req.body;

                for (const key of Object.keys(EXAMPLE_DATA.ADDITIONAL_DATA)) {
                    additionalDataValid = formData.has(key);
                }

                return req.url === environment.API_URL + API_URL.SEND_SCAN
                    && req.method === 'POST'
                    && formData.has('label')
                    && additionalDataValid;
            }, `POST to ${API_URL.SEND_SCAN}`)
                .flush({
                        comment: EXAMPLE_DATA.COMMENT,
                        label_id: EXAMPLE_DATA.LABEL_ID,
                        labeling_time: EXAMPLE_DATA.LABELING_TIME,
                        owner_id: EXAMPLE_DATA.OWNER_ID
                    },
                    {status: 201, statusText: 'Created'});
        }
    )));

    it(`shouldn't send selection`, async(inject([ScanService, HttpTestingController],
        (service: ScanService, backend: HttpTestingController) => {

            service.sendSelection(EXAMPLE_DATA.SCAN_ID,
                EXAMPLE_DATA.TASK_KEY,
                new Selection3D([MOCK_SELECTION]),
                EXAMPLE_DATA.LABELING_TIME,
                EXAMPLE_DATA.COMMENT)
                .catch((error: Error) => {
                    expect(error).toBeTruthy();
                });

            backend.expectOne((req: HttpRequest<any>) => {
                return req.url === environment.API_URL + API_URL.SEND_SCAN
                    && req.method === 'POST';
            }, `POST to ${API_URL.SEND_SCAN}`)
                .flush({},
                    {status: 404, statusText: 'Could not find scan or tag'});
        }
    )));

    it(`should get random scan`, async(inject([ScanService, HttpTestingController],
        (service: ScanService, backend: HttpTestingController) => {
            service.getRandomScan(EXAMPLE_DATA.TASK_KEY).then((scanMetadata: ScanMetadata) => {
                expect(scanMetadata.scanId).toBe(MOCK_SCAN_METADATA.scanId);
                expect(scanMetadata.status).toBe(MOCK_SCAN_METADATA.status);
                expect(scanMetadata.numberOfSlices).toBe(MOCK_SCAN_METADATA.numberOfSlices);
                expect(scanMetadata.width).toBe(MOCK_SCAN_METADATA.width);
                expect(scanMetadata.height).toBe(MOCK_SCAN_METADATA.height);
            });

            const response = {
                scan_id: EXAMPLE_DATA.SCAN_ID,
                status: EXAMPLE_DATA.STATUS,
                number_of_slices: MOCK_SCAN_METADATA.numberOfSlices,
                width: MOCK_SCAN_METADATA.width,
                height: MOCK_SCAN_METADATA.height
            };

            backend.expectOne((req: HttpRequest<any>) => {
                return req.url === environment.API_URL + API_URL.GET_RANDOM_SCAN
                    && req.method === 'GET';
            }, `GET from ${API_URL.GET_RANDOM_SCAN}`)
                .flush(response,
                    {status: 200, statusText: 'Ok'});
        }
    )));

    it(`shouldn't get random scan (undefined task)`, async(inject([ScanService, HttpTestingController],
        (service: ScanService) => {
            service.getRandomScan(undefined).catch((error: Error) => {
                expect(error).toBeTruthy();
            });
        }
    )));

    it(`shouldn't get random scan (backend rejection)`, async(inject([ScanService, HttpTestingController],
        (service: ScanService, backend: HttpTestingController) => {
            service.getRandomScan(EXAMPLE_DATA.TASK_KEY).catch((error: Error) => {
                expect(error).toBeTruthy();
            });

            backend.expectOne((req: HttpRequest<any>) => {
                return req.url === environment.API_URL + API_URL.GET_RANDOM_SCAN
                    && req.method === 'GET';
            }, `GET from ${API_URL.GET_RANDOM_SCAN}`)
                .flush({},
                    {status: 404, statusText: 'No Scans available'});
        }
    )));

    it(`should get scan for given id`, async(inject([ScanService, HttpTestingController],
        (service: ScanService, backend: HttpTestingController) => {
            service.getScanForScanId(EXAMPLE_DATA.SCAN_ID).then((scanMetadata: ScanMetadata) => {
                expect(scanMetadata.scanId).toBe(MOCK_SCAN_METADATA.scanId);
                expect(scanMetadata.status).toBe(MOCK_SCAN_METADATA.status);
                expect(scanMetadata.numberOfSlices).toBe(MOCK_SCAN_METADATA.numberOfSlices);
                expect(scanMetadata.width).toBe(MOCK_SCAN_METADATA.width);
                expect(scanMetadata.height).toBe(MOCK_SCAN_METADATA.height);
            });

            const response = {
                scan_id: EXAMPLE_DATA.SCAN_ID,
                status: EXAMPLE_DATA.STATUS,
                number_of_slices: MOCK_SCAN_METADATA.numberOfSlices,
                width: MOCK_SCAN_METADATA.width,
                height: MOCK_SCAN_METADATA.height
            };

            backend.expectOne((req: HttpRequest<any>) => {
                return req.url === environment.API_URL + API_URL.SCANS + EXAMPLE_DATA.SCAN_ID
                    && req.method === 'GET';
            }, `GET from ${API_URL.SCANS + EXAMPLE_DATA.SCAN_ID}`)
                .flush(response,
                    {status: 200, statusText: 'Ok'});
        }
    )));

    it(`shouldn't get scan for given id (backend rejection)`, async(inject([ScanService, HttpTestingController],
        (service: ScanService, backend: HttpTestingController) => {
            service.getScanForScanId(EXAMPLE_DATA.SCAN_ID).catch((error: Error) => {
                expect(error).toBeTruthy();
            });

            backend.expectOne((req: HttpRequest<any>) => {
                return req.url === environment.API_URL + API_URL.SCANS + EXAMPLE_DATA.SCAN_ID
                    && req.method === 'GET';
            }, `GET from ${API_URL.SCANS + EXAMPLE_DATA.SCAN_ID}`)
                .flush({},
                    {status: 404, statusText: 'No Scans available'});
        }
    )));

    it(`should create websocket event channel for incoming slices`, async(inject([ScanService, HttpTestingController],
        (service: ScanService) => {
            const spy = spyOn(fakeMedTaggerSocket, 'fromEvent').and.returnValue(of(MOCK_MARKER_SLICE_RAW));

            service.slicesObservable().subscribe((markerSlice: MarkerSlice) => {
                expect(spy).toHaveBeenCalled();
                expect(markerSlice).toEqual(MOCK_MARKER_SLICE);
            });
        }
    )));

    it('should request slices via websocket', async(inject([ScanService, HttpTestingController],
        (service: ScanService) => {
            const spy = spyOn(fakeMedTaggerSocket, 'emit');

            service.requestSlices(MOCK_MARKER_SLICE_RAW.scan_id,
                MOCK_MARKER_SLICE_RAW.index,
                MOCK_MARKER_SLICE_RAW.last_in_batch,
                false);

            expect(spy).toHaveBeenCalledWith('request_slices', {
                scan_id: MOCK_MARKER_SLICE_RAW.scan_id,
                begin: MOCK_MARKER_SLICE_RAW.index,
                count: MOCK_MARKER_SLICE_RAW.last_in_batch,
                reversed: false
            });

            console.log('Closing fakeMedTaggerSocket in ScanService tests');
            fakeMedTaggerSocket.disconnect();
        }
    )));

    it('should create new scan', async(inject([ScanService, HttpTestingController],
        (service: ScanService, backend: HttpTestingController) => {
            service.createNewScan(EXAMPLE_DATA.DATASET, EXAMPLE_DATA.NUM_SLICES).then((scan_id: string) => {
                expect(scan_id).toEqual(EXAMPLE_DATA.SCAN_ID);
            });

            backend.expectOne((req: HttpRequest<any>) => {
                let payload: {
                    dataset: string,
                    number_of_slices: number,
                };

                payload = req.body;

                return req.url === environment.API_URL + API_URL.SCANS
                    && req.method === 'POST'
                    && payload.dataset === EXAMPLE_DATA.DATASET
                    && payload.number_of_slices === EXAMPLE_DATA.NUM_SLICES;
            }, `POST to ${API_URL.SCANS}`)
                .flush({scan_id: EXAMPLE_DATA.SCAN_ID},
                    {status: 201, statusText: 'Created'});
        }
    )));

    it('should create new scan after retry', async(inject([ScanService, HttpTestingController],
        (service: ScanService, backend: HttpTestingController) => {

            const retriesNeeded = 1;

            service.delay = 500;

            service.createNewScan(EXAMPLE_DATA.DATASET, EXAMPLE_DATA.NUM_SLICES).then((scan_id: string) => {
                expect(scan_id).toEqual(EXAMPLE_DATA.SCAN_ID);
            });

            for (let i = 0; i < retriesNeeded; i++) {
                const request = backend.expectOne((req: HttpRequest<any>) => {
                    return req.url === environment.API_URL + API_URL.SCANS
                        && req.method === 'POST';
                }, `POST to ${API_URL.SCANS}`);

                const responeBody = i === 0 ? {} : {scan_id: EXAMPLE_DATA.SCAN_ID};
                const responsOpts = i === 0 ? {status: 404, statusText: ''} : {status: 201, statusText: 'Created'};

                request.flush(responeBody, responsOpts);
                setTimeout(() => {
                }, service.delay);
            }
        }
    )));

    it(`shouldn't creaty new scan after retries`, async(inject([ScanService, HttpTestingController],
        (service: ScanService, backend: HttpTestingController) => {

            service.delay = 500;
            service.retries = 1;

            service.createNewScan(EXAMPLE_DATA.DATASET, EXAMPLE_DATA.NUM_SLICES).catch((error: Error) => {
                expect(error).toBeTruthy();
            });

            for (let i = 0; i < service.retries; i++) {
                const request = backend.expectOne((req: HttpRequest<any>) => {
                    return req.url === environment.API_URL + API_URL.SCANS
                        && req.method === 'POST';
                }, `POST to ${API_URL.SCANS}`);

                const responeBody = {};
                const responsOpts = {status: 404, statusText: ''};

                request.flush(responeBody, responsOpts);
                setTimeout(() => {
                }, service.delay);
            }
        }
    )));

    it('should upload slices', async(inject([ScanService],
        (service: ScanService) => {
            const apiUrl = environment.API_URL + API_URL.SCANS + EXAMPLE_DATA.SCAN_ID + API_URL.SLICES;

            spyOn(http, 'post').and.callFake((api: string, form: FormData) => {
                if (api === apiUrl && form.has('image')) {
                    return of({status: 200, statusText: 'Ok'});
                }
            });

            const spy = spyOn(MOCK_FUNCTIONS, 'onSubscribe');
            service.uploadSlices(EXAMPLE_DATA.SCAN_ID, MOCK_UPLOAD_SCAN.files).subscribe(MOCK_FUNCTIONS.onSubscribe);

            expect(spy).toHaveBeenCalledTimes(MOCK_UPLOAD_SCAN.files.length);
        }
    )));

    it('should skip scan', async(inject([ScanService, HttpTestingController],
        (service: ScanService, backend: HttpTestingController) => {

            service.skipScan(EXAMPLE_DATA.SCAN_ID).then((response: Response) => {
                expect(response.status).toBe(200);
            });

            backend.expectOne((req: HttpRequest<any>) => {
                return req.url === environment.API_URL + API_URL.SCANS + EXAMPLE_DATA.SCAN_ID + API_URL.SKIP
                    && req.method === 'POST';
            }, `POST to ${API_URL.SCANS}`)
                .flush({status: 200, statusText: ''});
        }
    )));

    it(`shouldn't skip scan (error received)`, async(inject([ScanService, HttpTestingController],
        (service: ScanService, backend: HttpTestingController) => {

            service.skipScan(EXAMPLE_DATA.SCAN_ID).catch((error: Response) => {
                expect(error.status).toBe(404);
            });

            backend.expectOne((req: HttpRequest<any>) => {
                return req.url === environment.API_URL + API_URL.SCANS + EXAMPLE_DATA.SCAN_ID + API_URL.SKIP
                    && req.method === 'POST';
            }, `POST to ${API_URL.SCANS}`)
                .flush({status: 404, statusText: 'Could not find scan'});
        }
    )));
});

