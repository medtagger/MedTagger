import {AccountService} from './account.service';
import {TestBed, async, inject} from '@angular/core/testing';
import {HttpClientModule, HttpRequest} from '@angular/common/http';
import {HttpClientTestingModule, HttpTestingController} from '@angular/common/http/testing';
import {environment} from '../../environments/environment';
import {UserInfo} from '../model/UserInfo';
import {UserSettings} from '../model/UserSettings';
import {API_URL} from '../utils/ApiUrl';

describe('Service: AccountService', () => {
    const USER_SETTINGS: UserSettings = {
        skipTutorial: true
    };
    const EXAMPLE_USER = {
         EMAIL: 'foo@bar.com',
         PASSWORD: 'P@sswrd1',
         TOKEN: 'ZiL7Rrryt0edNt8RQ50l0AQkp1peFj6eBcU08p7EfVZBsmXenE5BAkRM7bGxQ6yEitGcNiQPf8LBdsHBilSZc4JXoh0AoX3kYyJ7H',
         INVALID_PASSWORD: 'p@sswrd1',
         FIRST_NAME: 'John',
         LAST_NAME: 'Smith',
         ROLE: 'volunteer',
         SETTINGS: USER_SETTINGS
     };

    beforeEach(() => {
        TestBed.configureTestingModule({
            imports: [
                HttpClientModule,
                HttpClientTestingModule
            ],
            providers: [
                AccountService
            ]
        });
    });

    it('should log in with valid credentials', async(inject([AccountService, HttpTestingController],
        (service: AccountService, backend: HttpTestingController) => {

            service.logIn(EXAMPLE_USER.EMAIL, EXAMPLE_USER.PASSWORD).then((userToken: string) => {
                expect(userToken).toBe(EXAMPLE_USER.TOKEN);
            });

            backend.expectOne((req: HttpRequest<any>) => {
                return req.url === environment.API_URL + API_URL.LOGIN
                    && req.method === 'POST'
                    && req.body.email === EXAMPLE_USER.EMAIL
                    && req.body.password === EXAMPLE_USER.PASSWORD;
            }, `POST to ${API_URL.LOGIN} with email and password`)
                .flush({token: EXAMPLE_USER.TOKEN},
                    {status: 200, statusText: 'Ok'});
        })));

    it('should not log in because of invalid credentials', async(inject([AccountService, HttpTestingController],
        (service: AccountService, backend: HttpTestingController) => {
            service.logIn(EXAMPLE_USER.EMAIL, EXAMPLE_USER.INVALID_PASSWORD).catch((error: Error) => {
                expect(error).toBeTruthy();
            });

            backend.expectOne((req: HttpRequest<any>) => {
                return req.url === environment.API_URL + API_URL.LOGIN
                    && req.method === 'POST'
                    && req.body.email === EXAMPLE_USER.EMAIL
                    && req.body.password !== EXAMPLE_USER.PASSWORD;
            }, `POST to ${API_URL.LOGIN} with email and password`)
                .flush({},
                    {status: 401, statusText: 'Unauthorized'});
        })));

    it('should register new account', async(inject([AccountService, HttpTestingController],
        (service: AccountService, backend: HttpTestingController) => {

            service.register(EXAMPLE_USER.EMAIL, EXAMPLE_USER.PASSWORD,
                EXAMPLE_USER.FIRST_NAME, EXAMPLE_USER.LAST_NAME).then((result: void) => {
                expect(result).toBeUndefined();
            });

            backend.expectOne((req: HttpRequest<any>) => {
                let payload: {
                    email: string,
                    password: string,
                    firstName: string,
                    lastName: string
                };

                payload = req.body;

                return req.url === environment.API_URL + API_URL.REGISTER
                    && req.method === 'POST'
                    && payload.email === EXAMPLE_USER.EMAIL
                    && payload.password === EXAMPLE_USER.PASSWORD
                    && payload.firstName === EXAMPLE_USER.FIRST_NAME
                    && payload.lastName === EXAMPLE_USER.LAST_NAME;
            }, `POST to ${API_URL.REGISTER} with email, password, first and last name`)
                .flush({},
                    {status: 201, statusText: 'Created'});
        })));

    it('should get user info', async(inject([AccountService, HttpTestingController],
        (service: AccountService, backend: HttpTestingController) => {

            service.getCurrentUserInfo().then((userInfo: UserInfo) => {
                expect(userInfo.email).toBe(EXAMPLE_USER.EMAIL);
                expect(userInfo.firstName).toBe(EXAMPLE_USER.FIRST_NAME);
                expect(userInfo.lastName).toBe(EXAMPLE_USER.LAST_NAME);
                expect(userInfo.id).toBeGreaterThan(0);
                expect(userInfo.role).toBeTruthy();
                expect(userInfo.settings).toBeTruthy();
            });

            const responseUserInfo: UserInfo =
                new UserInfo(1,
                    EXAMPLE_USER.EMAIL,
                    EXAMPLE_USER.FIRST_NAME,
                    EXAMPLE_USER.LAST_NAME,
                    EXAMPLE_USER.ROLE,
                    EXAMPLE_USER.SETTINGS);

            backend.expectOne((req: HttpRequest<any>) => {
                return req.url === environment.API_URL + API_URL.USER_INFO
                    && req.method === 'GET';
            }, `GET from ${API_URL.USER_INFO}`)
                .flush(responseUserInfo,
                    {status: 200, statusText: 'Ok'});
        })));
});
