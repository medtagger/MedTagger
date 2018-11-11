import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {UserInfo} from '../model/UserInfo';
import {environment} from '../../environments/environment';
import {UserSettings} from '../model/UserSettings';
import {API_URL} from '../utils/ApiUrl';

interface AllUsersResponse {
    users: Array<UserInfo>;
}

@Injectable()
export class UsersService {
    constructor(private http: HttpClient) {
    }

    public getAllUsers(): Promise<Array<UserInfo>> {
        const url = environment.API_URL + API_URL.USERS;
        return new Promise<Array<UserInfo>>((resolve, reject) => {
            this.http.get<AllUsersResponse>(url)
                .toPromise()
                .then(response => {
                    console.log('UsersService | getAllUsers | response: ', response);
                    const users = response.users.map((u: UserInfo) => {
                        return new UserInfo(u.id, u.email, u.firstName, u.lastName, u.role, u.settings);
                    });
                    resolve(users);
                })
                .catch(error => {
                    console.log('UsersService | getAllUsers | response: ', error);
                    reject(error);
                });
        });
    }

    public setRole(userId: number, role: string): Promise<void> {
        const url = environment.API_URL + API_URL.USERS + `/${userId}/role`;
        const payload = {
            role: role
        };
        return new Promise<void>((resolve, reject) => {
            this.http.put(url, payload)
                .toPromise()
                .then(response => {
                    console.log('UsersService | setRole | response: ', response);
                    resolve();
                })
                .catch(error => {
                    console.log('UsersService | setRole | response: ', error);
                    reject(error);
                });
        });
    }

    public setUserDetails(userId: number, userFirstName: string, userLastName: string): Promise<void> {
        const url = environment.API_URL + API_URL.USERS + `/${userId}`;
        const payload = {
            firstName: userFirstName,
            lastName: userLastName
        };
        return new Promise<void>((resolve, reject) => {
            this.http.put(url, payload)
                .toPromise()
                .then(response => {
                    console.log('UsersService | setUserDetails | response: ', response);
                    resolve();
                })
                .catch(error => {
                    console.log('UsersService | setUserDetails | response: ', error);
                    reject(error);
                });
        });
    }

    public setUserSettings(userId: number, settings: UserSettings): Promise<void> {
        const url = environment.API_URL + API_URL.USERS + `/${userId}/settings`;
        return new Promise<void>((resolve, reject) => {
            // properties with the undefined value will not be sent
            // only necessary properties of variable 'settings' should be specified
            this.http.post(url, settings)
                .toPromise()
                .then(response => {
                    console.log('UserService | setUserSettings | response: ', response);
                    resolve();
                })
                .catch(error => {
                    console.log('UserService | setUserSettings | response: ', error);
                    reject(error);
                });
        });
    }
}
