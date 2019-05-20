import { of } from 'rxjs';

export class TranslateServiceStub {

    public get(key: any): any {
        return of(key);
    }

    public setDefaultLang(lang: string): void {}

    public use(lang: string): void {}
}
