import {Injectable} from "@angular/core";
import {HttpClient} from '@angular/common/http';
import {UserInfo} from "../model/UserInfo";
import {environment} from "../../environments/environment";

interface AllUsersResponse {
    users: Array<UserInfo>;
}

@Injectable()
export class UsersService {
    constructor(private http: HttpClient) {
    }

    public getAllUsers(): Promise<Array<UserInfo>> {
        let url = environment.API_URL + '/users/';
        return new Promise<Array<UserInfo>>((resolve, reject) => {
            this.http.get<AllUsersResponse>(url)
                .toPromise()
                .then(response => {
                    console.log("UsersService | getAllUsers | response: ", response);
                    let users = response.users.map((u: UserInfo) => {
                        return new UserInfo(u.id, u.email, u.firstName, u.lastName, u.role, u.skipTutorial);
                    });
                    resolve(users);
                })
                .catch(error => {
                    console.log("UsersService | getAllUsers | response: ", error);
                    reject(error);
                })
        })
    }

    public setRole(userId: number, role: string): Promise<void> {
        let url = environment.API_URL + `/users/${userId}/role`;
        let payload = {
            role: role
        };
        return new Promise<void>((resolve, reject) => {
            this.http.put(url, payload)
                .toPromise()
                .then(response => {
                    console.log("UsersService | setRole | response: ", response);
                    resolve();
                })
                .catch(error => {
                    console.log("UsersService | setRole | response: ", error);
                    reject(error);
                })
        })
    }

    public setUserDetails(userId: number, userFirstName: string, userLastName: string): Promise<void> {
      let url = environment.API_URL + `/users/${userId}`;
      let payload = {
        firstName: userFirstName,
        lastName: userLastName
      };
      return new Promise<void>((resolve, reject) => {
        this.http.put(url, payload)
            .toPromise()
            .then(response => {
                console.log("UsersService | setUserDetails | response: ", response);
                resolve();
            })
            .catch(error => {
                console.log("UsersService | setUserDetails | response: ", error);
                reject(error);
            })
      })
    }

    public setSkipTutorial(userId: number, skipTutorial: boolean): Promise<void> {
        let url = environment.API_URL + `/users/${userId}/skip-tutorial`;
        let payload = {
            skipTutorial: true
        };
        return new Promise<void>((resolve, reject) => {
            this.http.post(url, payload)
                .toPromise()
                .then(response => {
                    console.log("UserService | setSkipTutorial | response: ", response);
                    resolve();
                })
                .catch(error => {
                    console.log("UserService | setSkipTutorial | response: ", error);
                    reject(error);
                })
        })
    }
}
