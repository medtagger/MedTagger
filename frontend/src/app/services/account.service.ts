import { Injectable } from "@angular/core";
import { environment } from "../../environments/environment";
import { UserInfo } from "../model/UserInfo";
import { Http, Headers } from "@angular/http";
import { AuthenticationHeader } from "./authentication-header";

@Injectable()
export class AccountService {
    constructor(private http: Http, private authenticationHeader: AuthenticationHeader) {}

    public register(email: string, password: string, firstName: string, lastName: string): Promise<void> {
        let url = environment.API_URL + '/auth/register';
        let payload = {
            email: email,
            password: password,
            firstName: firstName,
            lastName: lastName
        };
        return new Promise<void>((resolve, reject) => {
            this.http.post(url, payload).toPromise()
                .then(response => {
                    console.log("AccountService | register | response: ", response);
                    resolve();
                })
                .catch(error => {
                    console.log("AccountService | register | error: ", error);
                    reject(error);
                });
        })
    }

    public logIn(email: string, password: string): Promise<string> {
        let url = environment.API_URL + '/auth/sign-in';
        let payload = {
            'email': email,
            'password': password
        };
        return new Promise((resolve, reject) => {
            this.http.post(url, payload).toPromise()
                .then(response => {
                    console.log("AccountService | logIn | response: ", response);
                    resolve(response.json().token);
                })
                .catch(error => {
                    console.log("AccountService | logIn | error: ", error);
                    reject(error);
                });
        })
    }

    public getCurrentUserInfo(): Promise<UserInfo> {
        let url = environment.API_URL + '/users/info';
        return new Promise((resolve, reject) => {
            this.http.get(url, {
                headers: this.authenticationHeader.create()
            }).toPromise()
                .then(response => {
                    console.log("AccountService | getCurrentUserInfo | response: ", response);
                    let json = response.json();
                    let userInfo = new UserInfo(json.id, json.email, json.firstName, json.lastName, json.role)
                    resolve(userInfo);
                })
                .catch(error => {
                    console.log("AccountService | getCurrentUserInfo | error: ", error);
                    reject(error);
                });
        })
    }

    public isLoggedIn(): boolean {
      return !!(sessionStorage.getItem('userInfo') && sessionStorage.getItem('authenticationToken'))
    }
}
