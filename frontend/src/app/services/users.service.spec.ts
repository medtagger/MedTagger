import {async, inject, TestBed} from '@angular/core/testing';
import {HttpClientModule, HttpRequest} from '@angular/common/http';
import {HttpClientTestingModule, HttpTestingController} from '@angular/common/http/testing';
import {UsersService} from './users.service';
import {UserSettings} from '../model/UserSettings';
import {UserInfo} from '../model/UserInfo';
import {environment} from '../../environments/environment';
import {API_URL} from '../utils/ApiUrl';

describe('Service: UsersService', () => {
    const USER_SETTINGS: UserSettings = {
        skipTutorial: true
    };

    const EXAMPLE_USER = {
        id: 1,
        email: 'foo@bar.com',
        password: 'P@sswrd1',
        firstName: 'John',
        lastName: 'Smith',
        role: 'volunteer',
        settings: USER_SETTINGS
    };

    beforeEach(() => {
        TestBed.configureTestingModule({
            imports: [
                HttpClientModule,
                HttpClientTestingModule
            ],
            providers: [
                UsersService
            ]
        });
    });

    it('should get all users', async(inject([UsersService, HttpTestingController],
        (service: UsersService, backend: HttpTestingController) => {

            service.getAllUsers().then((users: Array<UserInfo>) => {
                users.forEach((user: UserInfo) => {
                    expect(user.email).toBe(EXAMPLE_USER.email);
                    expect(user.firstName).toBe(EXAMPLE_USER.firstName);
                    expect(user.lastName).toBe(EXAMPLE_USER.lastName);
                    expect(user.id).toBeGreaterThan(0);
                    expect(user.role).toBe(EXAMPLE_USER.role);
                    expect(user.settings).toBe(EXAMPLE_USER.settings);
                });
            });

            backend.expectOne((req: HttpRequest<any>) => {
                return req.url === environment.API_URL + API_URL.USERS
                    && req.method === 'GET';
            }, `GET from ${environment.API_URL + API_URL.USERS}`)
                .flush({users: [EXAMPLE_USER, EXAMPLE_USER]},
                    {status: 200, statusText: 'Ok'});
        }
    )));

    it(`shouldn't get all users`, async(inject([UsersService, HttpTestingController],
        (service: UsersService, backend: HttpTestingController) => {

            service.getAllUsers().catch((error: Error) => {
                expect(error).toBeTruthy();
            });

            backend.expectOne((req: HttpRequest<any>) => {
                return req.url === environment.API_URL + API_URL.USERS
                    && req.method === 'GET';
            }, `GET from ${environment.API_URL + API_URL.USERS}`)
                .flush({users: [EXAMPLE_USER, EXAMPLE_USER]},
                    {status: 404, statusText: ''});
        }
    )));

    it('should set role', async(inject([UsersService, HttpTestingController],
        (service: UsersService, backend: HttpTestingController) => {

            service.setRole(EXAMPLE_USER.id, EXAMPLE_USER.role).then((response: void) => {
                expect(response).toBeUndefined();
            });

            backend.expectOne((req: HttpRequest<any>) => {
                let payload: {
                    role: string
                };

                payload = req.body;

                return req.url === environment.API_URL + API_URL.USERS + EXAMPLE_USER.id + API_URL.ROLE
                    && req.method === 'PUT'
                    && payload.role === EXAMPLE_USER.role;
            }, `PUT to ${environment.API_URL + API_URL.USERS + EXAMPLE_USER.id + API_URL.ROLE}`)
                .flush({},
                    {status: 200, statusText: 'Ok'});

        }
    )));

    it(`shouldn't set role`, async(inject([UsersService, HttpTestingController],
        (service: UsersService, backend: HttpTestingController) => {

            service.setRole(EXAMPLE_USER.id, EXAMPLE_USER.role).catch((error: Error) => {
                expect(error).toBeTruthy();
            });

            backend.expectOne((req: HttpRequest<any>) => {
                let payload: {
                    role: string
                };

                payload = req.body;

                return req.url === environment.API_URL + API_URL.USERS + EXAMPLE_USER.id + API_URL.ROLE
                    && req.method === 'PUT'
                    && payload.role === EXAMPLE_USER.role;
            }, `PUT to ${environment.API_URL + API_URL.USERS + EXAMPLE_USER.id + API_URL.ROLE}`)
                .flush({},
                    {status: 404, statusText: ''});

        }
    )));

    it('should set user details', async(inject([UsersService, HttpTestingController],
        (service: UsersService, backend: HttpTestingController) => {

            service.setUserDetails(EXAMPLE_USER.id, EXAMPLE_USER.firstName, EXAMPLE_USER.lastName)
                .then((response: void) => {
                    expect(response).toBeUndefined();
                });

            backend.expectOne((req: HttpRequest<any>) => {
                let payload: {
                    firstName: string,
                    lastName: string
                };

                payload = req.body;

                return req.url === environment.API_URL + API_URL.USERS + EXAMPLE_USER.id
                    && req.method === 'PUT'
                    && payload.firstName === EXAMPLE_USER.firstName
                    && payload.lastName === EXAMPLE_USER.lastName;
            }, `PUT to ${environment.API_URL + API_URL.USERS + EXAMPLE_USER.id}`)
                .flush({},
                    {status: 200, statusText: 'Ok'});

        }
    )));

    it(`shouldn't set user details`, async(inject([UsersService, HttpTestingController],
        (service: UsersService, backend: HttpTestingController) => {

            service.setUserDetails(EXAMPLE_USER.id, EXAMPLE_USER.firstName, EXAMPLE_USER.lastName)
                .catch((error: Error) => {
                    expect(error).toBeTruthy();
                });

            backend.expectOne((req: HttpRequest<any>) => {
                let payload: {
                    firstName: string,
                    lastName: string
                };

                payload = req.body;

                return req.url === environment.API_URL + API_URL.USERS + EXAMPLE_USER.id
                    && req.method === 'PUT'
                    && payload.firstName === EXAMPLE_USER.firstName
                    && payload.lastName === EXAMPLE_USER.lastName;
            }, `PUT to ${environment.API_URL + API_URL.USERS + EXAMPLE_USER.id}`)
                .flush({},
                    {status: 404, statusText: ''});

        }
    )));

    it('should set user settings', async(inject([UsersService, HttpTestingController],
        (service: UsersService, backend: HttpTestingController) => {

            service.setUserSettings(EXAMPLE_USER.id, EXAMPLE_USER.settings)
                .then((response: void) => {
                    expect(response).toBeUndefined();
                });

            backend.expectOne((req: HttpRequest<any>) => {
                let payload: UserSettings;

                payload = req.body;

                return req.url === environment.API_URL + API_URL.USERS + EXAMPLE_USER.id + API_URL.SETTINGS
                    && req.method === 'POST'
                    && payload.skipTutorial === EXAMPLE_USER.settings.skipTutorial;
            }, `POST to ${environment.API_URL + API_URL.USERS + EXAMPLE_USER.id + API_URL.SETTINGS}`)
                .flush({},
                    {status: 200, statusText: 'Ok'});
        }
    )));

    it(`shouldn't set user settings`, async(inject([UsersService, HttpTestingController],
        (service: UsersService, backend: HttpTestingController) => {

            service.setUserSettings(EXAMPLE_USER.id, EXAMPLE_USER.settings)
                .catch((error: Error) => {
                    expect(error).toBeTruthy();
                });

            backend.expectOne((req: HttpRequest<any>) => {
                let payload: UserSettings;

                payload = req.body;

                return req.url === environment.API_URL + API_URL.USERS + EXAMPLE_USER.id + API_URL.SETTINGS
                    && req.method === 'POST'
                    && payload.skipTutorial === EXAMPLE_USER.settings.skipTutorial;
            }, `POST to ${environment.API_URL + API_URL.USERS + EXAMPLE_USER.id + API_URL.SETTINGS}`)
                .flush({},
                    {status: 404, statusText: ''});
        }
    )));
});

