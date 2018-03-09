import {Injectable} from "@angular/core";
import {Headers} from "@angular/http";

@Injectable()
export class AuthenticationHeader {
  public create(): Headers {
    let headers = new Headers();
    let token = sessionStorage.getItem('authenticationToken');
    headers.append('Authentication-Token', token);
    return headers;
  }
}
