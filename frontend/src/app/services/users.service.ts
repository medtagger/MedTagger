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
                        return new UserInfo(u.id, u.email, u.firstName, u.lastName, u.role);
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

    public setUserDetails(userId: number, userName: string, userSurname: string): Promise<void> {
      let url = environment.API_URL + `/users/${userId}/`;
      let payload = {
        firstName: userName,
        lastName: userSurname
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
}
