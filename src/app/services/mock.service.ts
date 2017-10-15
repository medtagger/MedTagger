import { Injectable } from '@angular/core';

@Injectable()
export class MockService {

  constructor() { }

  public getMockSlices(): Promise<any> {
    // TODO: ogarnąć httpservice jakiś do getowania
    console.log('MockService | getMockSlices');
    const mockSlices: ArrayBuffer[] = [];
    const mockImages: string[] = ['test_lung1.png', 'test_lung2.png',
                                'test_lung3.png', 'test_lung4.png',
                                'test_lung5.png'];

    return this.getLocalResource(mockImages[0], 'image/png').then((result) => {
      console.log('Resource result: ', result);
    }
    ).catch((error) => {
      console.log('Resource error: ', error);
    });
  }

  private getLocalResource(resourcePath: string, mimeType: string): Promise<any> {
    return new Promise((resolve, reject) => {
      const request = new XMLHttpRequest();
      request.overrideMimeType(mimeType);
      request.open('GET', resourcePath, true);
      request.onreadystatechange = () => {
        if (request.readyState === 4) {
          if (request.status === 200) {
            resolve(JSON.parse(request.responseText));
          } else {
            reject(`Could not load resource '${resourcePath}':${request.status}`);
          }
        }
      };
    });
  }

}
