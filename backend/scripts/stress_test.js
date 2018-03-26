const io = require('socket.io-client');
const request = require('request');

// Test definition
const MEDTAGGER_USER = 'test2';
const MEDTAGGER_PASSWORD = 'asdfasdf'
const MEDTAGGER_INSTANCE_REST_URL = 'http://localhost:51000';
const MEDTAGGER_INSTANCE_WEBSOCKET_URL = 'http://localhost:51001';
const SCAN_CATEGORY = 'KIDNEYS';
const SCAN_BEGIN = 0;
const SCAN_COUNT = 10;

// Global state of this Client
var AUTH_TOKEN = '';
var SCAN_ID = '';
var NUMBER_OF_SLICES = 0;
var RECEIVED_SLICES_IDS = [];
var REQUEST_NEXT_SLICES_ON_SIZE = SCAN_COUNT;
var BATCH_REQUEST_STARTED = Date.now();

console.log('Connecting to the WebSocket server...');
const socket = io(MEDTAGGER_INSTANCE_WEBSOCKET_URL + '/slices');

function logIn(handler) {
    console.log('Logging in...');
    request.post({
        url: MEDTAGGER_INSTANCE_REST_URL + '/api/v1/auth/sign-in',
        json: {
            email: MEDTAGGER_USER,
            password: MEDTAGGER_PASSWORD
        }
    }, (err, res, body) => {
        console.log('Successfully logged in!');
        handler(body['token']);
    });
}

function getRandomScan(authToken, handler) {
    console.log('Getting random Scan...');
    request.get({
        url: MEDTAGGER_INSTANCE_REST_URL + '/api/v1/scans/random?category=' + SCAN_CATEGORY,
        headers: {
            'Authorization': 'Bearer ' + authToken
        },
        json: true
    }, (err, res, body) => {
        console.log('Received Scan (', body['scan_id'], ') with', body['number_of_slices'], 'Slices.');
        handler(body['scan_id'], body['number_of_slices']);
    });
}

function requestSlices(scan_id, begin, count) {
    console.log('Requesting', count, 'Slices for', scan_id, 'starting at', begin, '...');
    BATCH_REQUEST_STARTED = Date.now();
    socket.emit('request_slices', {
        scan_id: scan_id,
        begin: begin,
        count: count
    });
};

socket.on('connect', function() {
    console.log('Connected');
    logIn((authToken) => {
        AUTH_TOKEN = authToken;
        getRandomScan(AUTH_TOKEN, (scanID, numberOfSlices) => {
            SCAN_ID = scanID;
            NUMBER_OF_SLICES = numberOfSlices;
            requestSlices(SCAN_ID, SCAN_BEGIN, SCAN_COUNT);
        });
    });
});

socket.on('slice', function(data) {
    RECEIVED_SLICES_IDS.push(data['index']);
    if (RECEIVED_SLICES_IDS.length == NUMBER_OF_SLICES) {
        console.log('This is the end of Slices for this Scan. Requesting new one...');
        RECEIVED_SLICES_IDS = [];
        REQUEST_NEXT_SLICES_ON_SIZE = SCAN_COUNT;

        getRandomScan(AUTH_TOKEN, (scanID, numberOfSlices) => {
            SCAN_ID = scanID;
            NUMBER_OF_SLICES = numberOfSlices;
            requestSlices(SCAN_ID, SCAN_BEGIN, SCAN_COUNT);
        });
        return;
    }
    if (RECEIVED_SLICES_IDS.length == REQUEST_NEXT_SLICES_ON_SIZE) {
        console.log('It took', (Date.now() - BATCH_REQUEST_STARTED) / 1000, 'seconds to get this batch.');
        REQUEST_NEXT_SLICES_ON_SIZE += SCAN_COUNT;
        requestSlices(SCAN_ID, RECEIVED_SLICES_IDS.length, SCAN_COUNT);
    }
});

socket.on('disconnect', function() {
    console.log('Disconnected');
});

