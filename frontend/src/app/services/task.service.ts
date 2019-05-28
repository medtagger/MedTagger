import { Injectable } from '@angular/core';
import { environment } from '../../environments/environment';
import { Task } from '../model/task/Task';
import { HttpClient } from '@angular/common/http';
import { LabelTag } from '../model/labels/LabelTag';
import { isUndefined } from 'util';

export interface TaskResponse {
    task_id: number;
    key: string;
    name: string;
    image_path: string;
    tags: Array<LabelTagResponse>;
    datasets_keys: Array<string>;
    number_of_available_scans: number;
    description: string;
    label_examples: Array<string>;
}

export interface LabelTagResponse {
    key: string;
    name: string;
    actions_ids: Array<number>;
    tools: Array<string>;
}

@Injectable()
export class TaskService {

    private tasks: Array<Task> = [];

    constructor(private http: HttpClient) {}

    getTask(taskKey: string): Promise<Task> {
        if (isUndefined(taskKey)) {
            return Promise.reject('TaskService | getTask | error: Task key was not found as a query parameter.');
        }
        if (this.tasks.length > 0) {
            // When user access labeling page through task page, current task comes from already filled array of tasks
            return Promise.resolve(this.tasks.find(task => task.key === taskKey));
        } else {
            return new Promise((resolve, reject) => {
                // When user does not access labeling page through task page, current task comes from call to API
                this.http.get<TaskResponse>(environment.API_URL + '/tasks/' + taskKey).toPromise().then(
                    response => {
                        console.log('TaskService | getTask | response: ', response);
                        resolve(this.getTaskFromResponse(response));
                    },
                    error => {
                        console.log('TaskService | getTask | error: ', error);
                        reject(error);
                    }
                );
            });
        }
    }

    getTasks(): Promise<Task[]> {
        if (this.tasks.length > 0) {
            this.tasks = [];
        }
        return new Promise((resolve, reject) => {
            this.http.get<Array<TaskResponse>>(environment.API_URL + '/tasks').toPromise().then(
                response => {
                    console.log('TaskService | getTasks | response: ', response);
                    for (const taskResponse of response) {
                       this.tasks.push(this.getTaskFromResponse(taskResponse));
                    }
                    resolve(this.tasks);
                },
                error => {
                    console.log('TaskService | getTasks | error: ', error);
                    reject(error);
                }
            );
        });
    }

    private getTaskFromResponse(response: TaskResponse): Task {
        const tags = response.tags.map(tag => new LabelTag(tag.key, tag.name, tag.tools));

        // Dev only
        response.number_of_available_scans = 5;
        // tslint:disable-next-line: max-line-length
        response.description = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent scelerisque nulla non laoreet eleifend. Quisque gravida sem sit amet quam consequat malesuada. Nunc tellus nisl, euismod et augue efficitur, egestas sollicitudin neque. Etiam convallis, diam quis convallis posuere, dolor mi blandit ante, ut blandit diam orci quis dolor. Morbi tellus felis, blandit et lorem ac, hendrerit luctus risus. Cras sodales urna ultricies est dignissim tempor. Sed at velit ac odio lacinia dignissim sit amet.';
        response.label_examples = ['../../../assets/img/login_pic.jpg', '../../../assets/img/login_pic.jpg'];

        return new Task(response, tags);
    }
}
