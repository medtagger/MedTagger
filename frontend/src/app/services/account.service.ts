import {Injectable} from '@angular/core';
import {environment} from '../../environments/environment';
import {UserInfo} from '../model/UserInfo';
import {HttpClient} from '@angular/common/http';

interface LogInResponse {
    token: string;
}

interface UserSettingsResponse {
    skipTutorial: boolean;
}

interface UserInfoResponse {
    id: number;
    email: string;
    firstName: string;
    lastName: string;
    role: string;
    settings: UserSettingsResponse;
}

@Injectable()
export class AccountService {
    constructor(private http: HttpClient) {}

    public register(email: string, password: string, firstName: string, lastName: string): Promise<void> {
        const url = environment.API_URL + '/auth/register';
        const payload = {
            email: email,
            password: password,
            firstName: firstName,
            lastName: lastName
        };
        return new Promise<void>((resolve, reject) => {
            this.http.post(url, payload).toPromise()
                .then(response => {
                    console.log('AccountService | register | response: ', response);
                    resolve();
                })
                .catch(error => {
                    console.log('AccountService | register | error: ', error);
                    reject(error);
                });
        });
    }

    public logIn(email: string, password: string): Promise<string> {
        const url = environment.API_URL + '/auth/sign-in';
        const payload = {
            'email': email,
            'password': password
        };
        return new Promise((resolve, reject) => {
            this.http.post<LogInResponse>(url, payload).toPromise()
                .then(response => {
                    console.log('AccountService | logIn | response: ', response);
                    resolve(response.token);
                })
                .catch(error => {
                    console.log('AccountService | logIn | error: ', error);
                    reject(error);
                });
        });
    }

    public getCurrentUserInfo(): Promise<UserInfo> {
        const url = environment.API_URL + '/users/info';
        return new Promise((resolve, reject) => {
            this.http.get<UserInfoResponse>(url).toPromise()
                .then(response => {
                    console.log('AccountService | getCurrentUserInfo | response: ', response);
                    const userInfo = new UserInfo(response.id, response.email, response.firstName, response.lastName,
                        response.role, response.settings);
                    resolve(userInfo);
                })
                .catch(error => {
                    console.log('AccountService | getCurrentUserInfo | error: ', error);
                    reject(error);
                });
        });
    }

    public isLoggedIn(): boolean {
        return !!(sessionStorage.getItem('userInfo') && sessionStorage.getItem('authorizationToken'));
    }
}
