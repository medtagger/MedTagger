import {async, inject, TestBed} from '@angular/core/testing';
import {HttpClientModule, HttpRequest} from '@angular/common/http';
import {HttpClientTestingModule, HttpTestingController} from '@angular/common/http/testing';
import {TaskService} from './task.service';
import {Task} from '../model/Task';
import {environment} from '../../environments/environment';
import {LabelTag} from '../model/labels/LabelTag';
import {API_URL} from '../utils/ApiUrl';

describe('Service: TaskService', () => {
    const EXAMPLE_DATA = {
        TASK: {
            task_id: 1,
            key: 'EXAMPLE',
            name: 'Example',
            image_path: 'Example image',
            tags: [{
                key: 'example key',
                name: 'example name',
                tools: ['tool1', 'tool2']
            }]
        }
    };

    beforeEach(() => {
        TestBed.configureTestingModule({
            imports: [
                HttpClientModule,
                HttpClientTestingModule
            ],
            providers: [
                TaskService
            ]
        });
    });

    it(`should get task for given task key`, async(inject([TaskService, HttpTestingController],
        (service: TaskService, backend: HttpTestingController) => {
            service.getTask(EXAMPLE_DATA.TASK.key).then((task: Task) => {
                const exampleLabelTagData = EXAMPLE_DATA.TASK.tags[0];
                const exampleLabelTag: LabelTag = new LabelTag(
                    exampleLabelTagData.key,
                    exampleLabelTagData.name,
                    exampleLabelTagData.tools
                );
                expect(task.id).toEqual(EXAMPLE_DATA.TASK.task_id);
                expect(task.imagePath).toEqual(EXAMPLE_DATA.TASK.image_path);
                expect(task.key).toEqual(EXAMPLE_DATA.TASK.key);
                expect(task.name).toEqual(EXAMPLE_DATA.TASK.name);
                expect(task.tags).toEqual([exampleLabelTag]);
            });

            backend.expectOne((req: HttpRequest<any>) => {
                return req.url === environment.API_URL + API_URL.TASK + EXAMPLE_DATA.TASK.key
                    && req.method === 'GET';
            }, `GET from ${API_URL.TASK + EXAMPLE_DATA.TASK.key}`)
                .flush(EXAMPLE_DATA.TASK,
                    {status: 200, statusText: 'Ok'});
        }
    )));

    it(`shouldn't get task for given task key`, async(inject([TaskService, HttpTestingController],
        (service: TaskService, backend: HttpTestingController) => {
            service.getTask(EXAMPLE_DATA.TASK.key).catch((error: Error) => {
                expect(error).toBeTruthy();
            });

            backend.expectOne((req: HttpRequest<any>) => {
                return req.url === environment.API_URL + API_URL.TASK + EXAMPLE_DATA.TASK.key
                    && req.method === 'GET';
            }, `GET from ${API_URL.TASK + EXAMPLE_DATA.TASK.key}`)
                .flush({},
                    {status: 404, statusText: ''});
        }
    )));

    it(`should get tasks`, async(inject([TaskService, HttpTestingController],
        (service: TaskService, backend: HttpTestingController) => {
            service.getTasks().then((tasks: Array<Task>) => {
                const exampleLabelTagData = EXAMPLE_DATA.TASK.tags[0];
                const exampleLabelTag: LabelTag = new LabelTag(
                    exampleLabelTagData.key,
                    exampleLabelTagData.name,
                    exampleLabelTagData.tools
                );

                tasks.forEach((task: Task) => {
                    expect(task.id).toEqual(EXAMPLE_DATA.TASK.task_id);
                    expect(task.imagePath).toEqual(EXAMPLE_DATA.TASK.image_path);
                    expect(task.key).toEqual(EXAMPLE_DATA.TASK.key);
                    expect(task.name).toEqual(EXAMPLE_DATA.TASK.name);
                    expect(task.tags).toEqual([exampleLabelTag]);
                });

            });

            backend.expectOne((req: HttpRequest<any>) => {
                return req.url === environment.API_URL + API_URL.TASKS
                    && req.method === 'GET';
            }, `GET from ${API_URL.TASKS}`)
                .flush([EXAMPLE_DATA.TASK, EXAMPLE_DATA.TASK],
                    {status: 200, statusText: 'Ok'});
        }
    )));

    it(`shouldn't get tasks`, async(inject([TaskService, HttpTestingController],
        (service: TaskService, backend: HttpTestingController) => {
            service.getTasks().catch((error: Error) => {
                expect(error).toBeTruthy();
            });

            backend.expectOne((req: HttpRequest<any>) => {
                return req.url === environment.API_URL + API_URL.TASKS
                    && req.method === 'GET';
            }, `GET from ${API_URL.TASK + EXAMPLE_DATA.TASK.key}`)
                .flush({},
                    {status: 404, statusText: ''});
        }
    )));
});
