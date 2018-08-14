import {Injectable} from '@angular/core';
import {environment} from '../../environments/environment';
import {Task} from '../model/Task';
import {HttpClient} from '@angular/common/http';
import {LabelTag} from '../model/labels/LabelTag';

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

    private tasks: Array<Task> = [];
    constructor(private http: HttpClient) { }

    getTask(taskKey: string): Promise<Task> {
        if (taskKey == null) {
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
                        const tags = response.tags.map(tag => new LabelTag(tag.key, tag.name, tag.tools));
                        resolve(new Task(response.task_id, response.key, response.name, response.image_path, tags));
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
                    for (const task of response) {
                        const tags = task.tags.map(tag => new LabelTag(tag.key, tag.name, tag.tools));
                        this.tasks.push(new Task(task.task_id, task.key, task.name, task.image_path, tags));
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
}
