import {async, inject, TestBed} from '@angular/core/testing';
import {HttpClientModule, HttpRequest} from '@angular/common/http';
import {HttpClientTestingModule, HttpTestingController} from '@angular/common/http/testing';
import {environment} from '../../environments/environment';
import {API_URL} from '../utils/ApiUrl';
import {Task} from '../model/Task';
import {LabelService, RandomLabelResponse} from './label.service';
import {LabelTag} from '../model/labels/LabelTag';
import {Label} from '../model/labels/Label';
import {RectangleSelection} from '../model/selections/RectangleSelection';

describe('Service: LabelService', () => {
    const EXAMPLE_TASK = new Task(1, 'EXAMPLE_TASK', 'Example Task', 'image.jpg', [
        new LabelTag('LEFT_NODULE', 'Left Nodule', ['RECTANGLE'])
    ], ['LUNGS']);

    const EXAMPLE_RANDOM_LABEL_RESPONSE: RandomLabelResponse = {
        label_id: 'label-hash',
        scan_id: 'scan-hash',
        task_id: 'LUNG_SEGMENTATION',
        status: 'NOT_VERIFIED',
        elements: [{
            id: 1,
            x: 0.5,
            y: 0.5,
            width: 0.5,
            height: 0.5,
            tool: 'RECTANGLE'
        }],
        labeling_time: 1.23,
        comment: 'Test'
    };

    const RANDOM_LABEL_API = API_URL.LABELS + '/random';
    const LABEL_BY_ID_API = API_URL.LABELS + '/' + EXAMPLE_RANDOM_LABEL_RESPONSE.label_id;
    const CHANGE_LABEL_STATUS_API = API_URL.LABELS + '/' + EXAMPLE_RANDOM_LABEL_RESPONSE.label_id + '/status';

    beforeEach(() => {
        TestBed.configureTestingModule({
            imports: [
                HttpClientModule,
                HttpClientTestingModule
            ],
            providers: [
                LabelService
            ]
        });
    });

    it('should get random Label', async(inject([LabelService, HttpTestingController],
        (service: LabelService, backend: HttpTestingController) => {
            service.getRandomLabel(EXAMPLE_TASK).then((label: Label) => {
                expect(label.labelId).toBe(EXAMPLE_RANDOM_LABEL_RESPONSE.label_id);
                expect(label.scanId).toBe(EXAMPLE_RANDOM_LABEL_RESPONSE.scan_id);
                expect(label.labelStatus).toBe(EXAMPLE_RANDOM_LABEL_RESPONSE.status);
                expect(label.labelingTime).toBe(EXAMPLE_RANDOM_LABEL_RESPONSE.labeling_time);
                expect(label.labelComment).toBe(EXAMPLE_RANDOM_LABEL_RESPONSE.comment);
                expect(label.labelSelections.length).toBe(1);

                const rectangleSelection = label.labelSelections[0] as RectangleSelection;
                expect(rectangleSelection.positionX).toBe(0.5);
                expect(rectangleSelection.positionY).toBe(0.5);
                expect(rectangleSelection.width).toBe(0.5);
                expect(rectangleSelection.height).toBe(0.5);
            });

            backend.expectOne((req: HttpRequest<any>) => {
                return req.url === environment.API_URL + RANDOM_LABEL_API
                    && req.method === 'GET';
            }, `GET from ${RANDOM_LABEL_API}`)
                .flush(EXAMPLE_RANDOM_LABEL_RESPONSE,
                    {status: 200, statusText: 'Ok'});
        }
    )));

    it('should get Label by ID', async(inject([LabelService, HttpTestingController],
        (service: LabelService, backend: HttpTestingController) => {
            service.getLabelByID(EXAMPLE_RANDOM_LABEL_RESPONSE.label_id, EXAMPLE_TASK).then((label: Label) => {
                expect(label.labelId).toBe(EXAMPLE_RANDOM_LABEL_RESPONSE.label_id);
                expect(label.scanId).toBe(EXAMPLE_RANDOM_LABEL_RESPONSE.scan_id);
                expect(label.labelStatus).toBe(EXAMPLE_RANDOM_LABEL_RESPONSE.status);
                expect(label.labelingTime).toBe(EXAMPLE_RANDOM_LABEL_RESPONSE.labeling_time);
                expect(label.labelComment).toBe(EXAMPLE_RANDOM_LABEL_RESPONSE.comment);
                expect(label.labelSelections.length).toBe(1);

                const rectangleSelection = label.labelSelections[0] as RectangleSelection;
                expect(rectangleSelection.positionX).toBe(0.5);
                expect(rectangleSelection.positionY).toBe(0.5);
                expect(rectangleSelection.width).toBe(0.5);
                expect(rectangleSelection.height).toBe(0.5);
            });

            backend.expectOne((req: HttpRequest<any>) => {
                return req.url === environment.API_URL + LABEL_BY_ID_API
                    && req.method === 'GET';
            }, `GET from ${LABEL_BY_ID_API}`)
                .flush(EXAMPLE_RANDOM_LABEL_RESPONSE,
                    {status: 200, statusText: 'Ok'});
        }
    )));

    it('should change Label status', async(inject([LabelService, HttpTestingController],
        (service: LabelService, backend: HttpTestingController) => {
            service.changeStatus(EXAMPLE_RANDOM_LABEL_RESPONSE.label_id, 'VERIFIED').then(_ => {});

            backend.expectOne((req: HttpRequest<any>) => {
                return req.url === environment.API_URL + CHANGE_LABEL_STATUS_API
                    && req.method === 'PUT'
                    && req.body.status === 'VERIFIED';
            }, `GET from ${CHANGE_LABEL_STATUS_API}`)
                .flush(EXAMPLE_RANDOM_LABEL_RESPONSE,
                    {status: 200, statusText: 'Ok'});
        }
    )));
});
