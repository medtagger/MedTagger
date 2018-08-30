import {AccountService} from './account.service';
import {TestBed, async, inject} from '@angular/core/testing';
import {HttpClientModule, HttpParams, HttpRequest} from '@angular/common/http';
import {HttpClientTestingModule, HttpTestingController} from '@angular/common/http/testing';
import {environment} from '../../environments/environment';

describe('Service: AccountService', () => {
    const EXAMPLE_USER_EMAIL = 'foo@bar.com';
    const EXAMPLE_USER_PASSWORD = 'P@sswrd1';
    const EXAMPLE_VALID_TOKEN =
        'ZiL7Rrryt0edNt8RQ50l0AQkp1peFj6eBcU08p7EfVZBsmXenE5BAkRM7bGxQ6yEitGcNiQPf8LBdsHBilSZc4JXoh0AoX3kYyJ7H';

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

    it(`should log in with valid credentials`, async(inject([AccountService, HttpTestingController],
        (service: AccountService, backend: HttpTestingController) => {

            service.logIn(EXAMPLE_USER_EMAIL, EXAMPLE_USER_PASSWORD).then((userToken: string) => {
                expect(userToken).toBe(EXAMPLE_VALID_TOKEN);
            });

            backend.expectOne((req: HttpRequest<any>) => {
                return req.url === environment.API_URL + '/auth/sign-in'
                    && req.method === 'POST'
                    && req.body.email === EXAMPLE_USER_EMAIL
                    && req.body.password === EXAMPLE_USER_PASSWORD;
            }, `POST to '/auth/sign-in' with email and password`)
                .flush({token: EXAMPLE_VALID_TOKEN},
                    {status: 200, statusText: 'Ok'});
        })));
});
