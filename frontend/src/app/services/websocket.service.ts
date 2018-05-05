import {Injectable} from '@angular/core';
import {Socket} from 'ng-socket-io';

import {environment} from '../../environments/environment';


@Injectable()
export class MedTaggerWebSocket extends Socket {

    constructor() {
        super({url: environment.WEBSOCKET_URL + '/slices', options: {path: environment.WEBSOCKET_PATH}});
    }

}
