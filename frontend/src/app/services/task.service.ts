import {Injectable} from '@angular/core';
import {environment} from '../../environments/environment';
import {Task} from '../model/Task';
import {HttpClient} from '@angular/common/http';
import {LabelTag} from '../model/LabelTag';

export interface TaskResponse {
    task_id: number;
    key: string;
    name: string;
    image_path: string;
    tags: Array<LabelTagResponse>;
    categories: Array<string>;
}

interface LabelTagResponse {
    key: string;
    name: string;
    actions_ids: Array<number>;
    tools: Array<string>;
}

@Injectable()
export class TaskService {

    constructor(private http: HttpClient) {}

    getCurrentTask(taskKey: string): Promise<Task> {
        return new Promise((resolve, reject) => {
            this.http.get<TaskResponse>(environment.API_URL + '/tasks/' + taskKey).toPromise().then(
                response => {
                    console.log('ScanService | getCurrentTask | response: ', response);
                    const tags = response.tags.map(tag => new LabelTag(tag.key, tag.name, tag.tools));
                    resolve(new Task(response.task_id, response.key, response.name, response.image_path, tags));
                },
                error => {
                    console.log('ScanService | getCurrentTask | error: ', error);
                    reject(error);
                }
            );
        });
    }

    getTasks(): Promise<Task[]> {
        return new Promise((resolve, reject) => {
            this.http.get<Array<TaskResponse>>(environment.API_URL + '/tasks').toPromise().then(
                response => {
                    console.log('ScanService | getTasks | response: ', response);
                    const tasks: Array<Task> = [];
                    for (const task of response) {
                        const tags = task.tags.map(tag => new LabelTag(tag.key, tag.name, tag.tools));
                        tasks.push(new Task(task.task_id, task.key, task.name, task.image_path, tags));
                    }
                    resolve(tasks);
                },
                error => {
                    console.log('ScanService | getTasks | error: ', error);
                    reject(error);
                }
            );
        });
    }
}
