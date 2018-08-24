const io = require('socket.io-client');
const request = require('request');

// Simulation parameters
const CLIENT_ID = ("00" + process.argv[2]).slice(-2);  // Client ID will always use two numbers (leading zeros)
const MEDTAGGER_INSTANCE_REST_URL = process.argv[3];
const MEDTAGGER_INSTANCE_WEBSOCKET_URL = process.argv[4];
const MEDTAGGER_USER = process.argv[5];
const MEDTAGGER_PASSWORD = process.argv[6];
const DATASET = process.argv[7];
const SCAN_BEGIN = parseInt(process.argv[8]);
const SCAN_COUNT = parseInt(process.argv[9]);
const STICKY_SESSION = parseInt(process.argv[10]);

// Global state of this Client
var socket = null;
var authToken = 'AUTH_TOKEN';
var scanID = 'SCAN_ID';
var numberOfSlices = 0;
var receivedSlicesIDs = [];
var requestNextSlicesWhenReceived = SCAN_COUNT;
var batchRequestStartTime = Date.now();


function logIn(handler) {
    request.post({
        url: MEDTAGGER_INSTANCE_REST_URL + '/api/v1/auth/sign-in',
        json: {
            email: MEDTAGGER_USER,
            password: MEDTAGGER_PASSWORD
        }
    }, (err, res, body) => {
        authToken = body['token'];
        handler();  // As this is a wrapper -> let's call main function
    });
}

function getCookieForWebSocketStickness(handler) {
    // Call GET on WebSocket URL to receive COOKIE which should define our stickness to the server
    request.get({
        url: MEDTAGGER_INSTANCE_WEBSOCKET_URL + '/socket.io/',
        headers: { 'Authorization': 'Bearer ' + authToken },
    }, (err, res, body) => {
        // Cookies which should be set will be retuned in headers under `set-cookie` key
        var cookies = res.headers['set-cookie'];

        // There should be a Cookie which will tell us to which server we should stick
        var webSocketNode, webSocketNodeCookie;
        cookies.forEach(function(cookie) {
            if (cookie.startsWith('MEDTAGER_WEBSOCKET_NODE=')) {
                webSocketNode = cookie.split('=')[1].split(';')[0];
                webSocketNodeCookie = 'MEDTAGER_WEBSOCKET_NODE=' + webSocketNode;
            }
        });

        // Now we know that we should stick to one node
        console.log('CLIENT #%s: Node %s', CLIENT_ID, webSocketNode);
        handler(webSocketNodeCookie);  // As this is a wrapper -> let's call main function
    });
}

function getRandomScan(handler) {
    request.get({
        url: MEDTAGGER_INSTANCE_REST_URL + '/api/v1/scans/random?dataset=' + DATASET,
        headers: { 'Authorization': 'Bearer ' + authToken },
        json: true
    }, (err, res, body) => {
        scanID = body['scan_id'];
        numberOfSlices = body['number_of_slices'];

        // Now we know our current ScanID and how many Slices it has
        console.log('CLIENT #%s: Received Scan (%s) with %d Slices.', CLIENT_ID, scanID, numberOfSlices);
        handler();  // As this is a wrapper -> let's call main function
    });
}

function requestSlices(begin, count) {
    // Remember when we started requesting for Slices to measure time!
    batchRequestStartTime = Date.now();
    socket.emit('request_slices', {
        scan_id: scanID,
        begin: begin,
        count: count
    });
};

// This is main logic for this script
// At first, let's log in and remember token which we should use
logIn(() => {

    // Let's stick to one WebSocket server as NodeJS Client does not automatically set Cookies during connection start
    getCookieForWebSocketStickness((cookie) => {

        // Open WebSocket connection to the server with Cookie (important!)
        options = {extraHeaders: { 'Cookie': cookie }} ? STICKY_SESSION : {};
        socket = io(MEDTAGGER_INSTANCE_WEBSOCKET_URL + '/slices', options);

        socket.on('connect', function() {
            // Once we will connect to the server, let's ask backend for random Scan and request first batch of Slices
            getRandomScan(() => {
                requestSlices(SCAN_BEGIN, SCAN_COUNT);
            });
        });

        socket.on('slice', function(data) {
            // We received a single Slice from backend, remember its ID to be able to count how many we've received so far
            receivedSlicesIDs.push(data['index']);

            // Check if we fetched all slices for this Scan
            if (receivedSlicesIDs.length == numberOfSlices) {
                receivedSlicesIDs = [];
                requestNextSlicesWhenReceived = SCAN_COUNT;
                getRandomScan(() => {
                    requestSlices(SCAN_BEGIN, SCAN_COUNT);
                });
            }
            // Check if its the end of current batch
            else if (receivedSlicesIDs.length == requestNextSlicesWhenReceived) {
                console.log('CLIENT #%s: It took %fs to get this batch.', CLIENT_ID, (Date.now() - batchRequestStartTime) / 1000);
                requestNextSlicesWhenReceived += SCAN_COUNT;
                requestSlices(receivedSlicesIDs.length, SCAN_COUNT);
            }
        });

        socket.on('disconnect', function() {
            console.log('CLIENT #%s: Disconnected', CLIENT_ID);
        });

    });

});

