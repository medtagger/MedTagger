const { spawn } = require('child_process');

const NUMBER_OF_CLIENTS = 4;
const MEDTAGGER_INSTANCE_REST_URL = 'http://localhost';
const MEDTAGGER_INSTANCE_WEBSOCKET_URL = 'http://localhost';
const MEDTAGGER_USER = 'admin@medtagger.com';
const MEDTAGGER_PASSWORD = 'medtagger1';
const SCAN_CATEGORY = 'KIDNEYS';
const SCAN_BEGIN = 0;
const SCAN_COUNT = 10;


for (var client = 1; client <= NUMBER_OF_CLIENTS; client++) {
    const CLIENT_ID = client.toString();
    const simulation = spawn('node', [
        './simulation.js',
        CLIENT_ID,
        MEDTAGGER_INSTANCE_REST_URL,
        MEDTAGGER_INSTANCE_WEBSOCKET_URL,
        MEDTAGGER_USER,
        MEDTAGGER_PASSWORD,
        SCAN_CATEGORY,
        SCAN_BEGIN,
        SCAN_COUNT
    ]);
    simulation.stdout.setEncoding('utf8').on('data', function(data) { 
        process.stdout.write(data);
    });
    simulation.stderr.setEncoding('utf8').on('data', function(data) { 
        process.stdout.write(data);
    });
}

