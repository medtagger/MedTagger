const { spawn } = require('child_process');

const NUMBER_OF_CLIENTS = 10;
const MEDTAGGER_INSTANCE_REST_URL = 'http://localhost:51000';
const MEDTAGGER_INSTANCE_WEBSOCKET_URL = 'http://localhost:51001';
const MEDTAGGER_USER = 'admin@medtagger.com';
const MEDTAGGER_PASSWORD = 'medtagger1';
const DATASET = 'LUNGS';
const SCAN_BEGIN = 0;
const SCAN_COUNT = 10;
const STICKY_SESSION = 0;  // 0 - false, 1 - true


for (var client = 1; client <= NUMBER_OF_CLIENTS; client++) {
    const CLIENT_ID = client.toString();
    const simulation = spawn('node', [
        './simulation.js',
        CLIENT_ID,
        MEDTAGGER_INSTANCE_REST_URL,
        MEDTAGGER_INSTANCE_WEBSOCKET_URL,
        MEDTAGGER_USER,
        MEDTAGGER_PASSWORD,
        DATASET,
        SCAN_BEGIN,
        SCAN_COUNT,
        STICKY_SESSION
    ]);
    simulation.stdout.setEncoding('utf8').on('data', function(data) { 
        process.stdout.write(data);
    });
    simulation.stderr.setEncoding('utf8').on('data', function(data) { 
        process.stdout.write(data);
    });
}

