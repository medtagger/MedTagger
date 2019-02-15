export function login(email, password) {
    cy.request('POST', Cypress.env('API_URL') + 'auth/sign-in', {
        email: email,
        password: password
    }).then(response => {
        const token = response.body.token;
        window.sessionStorage.setItem('authorizationToken', token);
        cy.request({
            url: Cypress.env('API_URL') + 'users/info',
            headers: {Authorization: `Bearer ${token}`}
        }).then(response => {
            window.sessionStorage.setItem('userInfo', JSON.stringify(response.body));
        });
    });
}

export function loginAsAdmin() {
    login('admin@medtagger.com', 'medtagger1');
}

export function setFilesInInput(filePath, fileCount = 1, selector = 'input[type="file"]') {
    cy.get(selector).then(inputs => {
        cy.fixture(filePath, 'binary').then(fileContent => {
            let byteNumbers = new Array(fileContent.length);
            for (let i = 0; i < fileContent.length; i++) {
                byteNumbers[i] = fileContent.charCodeAt(i);
            }
            let byteArray = new Uint8Array(byteNumbers);

            const fileName = filePath.replace(/^.*\//);
            const file = new File([byteArray], fileName);
            let dataTransfer = new DataTransfer();

            for (let i = 0; i < fileCount; i++) {
                dataTransfer.items.add(file);
            }
            inputs[0].files = dataTransfer.files;
        });
    });
}

export function matSelect(selector, option) {
    cy.get(selector).click();
    cy.get(`mat-option span:contains(${option})`).click();
}

export function uploadScans(datasets, scansCount) {
    // Watch on Label endpoint
    cy.server();
    cy.route('GET', '/api/v1/datasets').as('fetchDatasets');

    // Upload Scans
    cy.visit(Cypress.env('HOST_URL'));
    cy.get('[data-cy=home-upload-button]').click();
    cy.wait('@fetchDatasets');
    matSelect('[data-cy=datasets]', datasets);
    cy.get('[data-cy=datasets-submit]').click();
    cy.get('[data-cy=single-scan]').click();
    setFilesInInput('scans/scan.dcm', scansCount);
    cy.get('[data-cy=single-scan-upload]').click();
    cy.contains(/Upload completed sucessfully!/, {timeout: 60000}); // uploading scan is time consuming so we must increase timeout
}

export function goToLabeling(task) {
    cy.visit(Cypress.env('HOST_URL'));
    cy.get(`[data-cy=task]:contains(${task})`).click({force: true}); // clicking on svg has bug, https://github.com/cypress-io/cypress/issues/2245
    cy.get('[data-cy=next1]').click();
    cy.get('[data-cy=next2]').click();
    cy.get('[data-cy=next3]').click();
    cy.get('[data-cy=not-show]').click(); // unchecked "Do not show this tutorial again", we want execute the same steps every time
    cy.get('[data-cy=next4]').click();
}
