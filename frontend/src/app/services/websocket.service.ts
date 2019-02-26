import {Injectable} from '@angular/core';
import {Socket} from 'ngx-socket-io';

import {environment} from '../../environments/environment';


@Injectable()
export class MedTaggerWebSocket extends Socket {

    constructor() {
        super({
            url: environment.WEBSOCKET_URL + '/slices',
            options: {
                path: environment.WEBSOCKET_PATH,
                timeout: 5000,  // 5 seconds (default: 20 seconds)
                reconnectionDelayMax: 1000  // 1 second (default: 5 seconds)
            }
        });

        // By default SocketIO tries to set up a "better" transport layer which may
        // break sometimes. In case of issues while setting it up, let's also give
        // the browser a chance to setup polling mechanism (slower but will increase
        // stability of WebSocket in case of troubles).
        this.on('reconnect_attempt', () => {
            this.ioSocket.io.opts.transports = ['polling', 'websocket'];
        });
    }

}
