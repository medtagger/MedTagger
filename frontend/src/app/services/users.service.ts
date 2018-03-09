import {Injectable} from "@angular/core";
import {Http} from "@angular/http";
import {AuthenticationHeader} from "./authentication-header";
import {UserInfo} from "../model/UserInfo";
import {environment} from "../../environments/environment";

@Injectable()
export class UsersService {
    constructor(private http: Http, private authenticationHeader: AuthenticationHeader) {
    }

    public getAllUsers(): Promise<Array<UserInfo>> {
        let url = environment.API_URL + '/users/';
        return new Promise<Array<UserInfo>>((resolve, reject) => {
            this.http.get(url, {
                headers: this.authenticationHeader.create()
            })
                .toPromise()
                .then(response => {
                    console.log("UsersService | getAllUsers | response: ", response);
                    let json = response.json();
                    let users = json.users.map((u: UserInfo) => {
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
            this.http.put(url, payload, {headers: this.authenticationHeader.create()})
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
}
