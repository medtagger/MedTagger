// The file contents for the current environment will overwrite these during build.
// The build system defaults to the dev environment which uses `environment.ts`, but if you do
// `ng <serve|build> --configuration=prod` or `ng <serve|build> -c prod` then `environment.prod.ts` will be used instead.
// The list of which env maps to which file can be found in `.angular-cli.json`.

export const environment = {
    production: false,
    API_URL: 'http://10.0.0.99:51000/api/v1',
    WEBSOCKET_URL: 'http://10.0.0.99:51001',
    WEBSOCKET_PATH: '/socket.io'
};
