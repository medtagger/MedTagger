import {Injectable} from '@angular/core';

@Injectable()
export class MockService {
    imageAssetsDir = '../../assets/img/';
    mockSlices: string[] = ['test_lung1.png', 'test_lung2.png',
        'test_lung3.png', 'test_lung4.png',
        'test_lung5.png'];

    constructor() {
    }

    public getMockSlicesURI(): string[] {
        // TODO: ogarnąć httpservice jakiś do getowania
        console.log('MockService | getMockSlices');

        const mockedSliceURIs: string[] = [];
        this.mockSlices.forEach((sliceURI: string, index: number, sclicesArray: string[]) => {
            mockedSliceURIs.push(this.imageAssetsDir + sliceURI);
        });
        return mockedSliceURIs;
    }
}
