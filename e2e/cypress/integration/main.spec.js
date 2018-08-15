function login(email, password) {
    cy.request('POST', Cypress.env('API_URL') + 'auth/sign-in', {
        email: email,
        password: password
    }).then(response => {
        const token = response.body.token;
        window.sessionStorage.setItem('authorizationToken', token);
        cy.request({url: Cypress.env('API_URL') + 'users/info', headers: {Authorization: `Bearer ${token}`}}).then(response => {
            window.sessionStorage.setItem('userInfo', JSON.stringify(response.body));
        });
    });
}

function loginAsAdmin() {
    login('admin@medtagger.com', 'medtagger1');
}

function openSidebar() {
    cy.get('[data-cy=sidebar]').click();
}

function setFilesInInput(filePath, fileCount = 1, selector = 'input[type="file"]') {
    cy.get('input[type="file"]').then(inputs => {
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

function matSelect(selector, option) {
    cy.get(selector).click();
    cy.get(`mat-option span:contains(${option})`).click();
}

describe('Basic flow', () => {

    beforeEach(() => {
        // local session and cookies are cleared automatically before each test so we don't have to do this manually
        // we need to clear only session storage
        window.sessionStorage.clear()
    });

    afterEach(() => {
        // if we refresh site during test, this hook won't execute
        // use beforeEach() instead
    });

    it('Login as admin and logout', () => {
        cy.visit(Cypress.env('HOST_URL'));
        cy.get('[data-cy=login-toggle]').click();
        cy.get('#email').type('admin@medtagger.com');
        cy.get('#password').type('medtagger1');
        cy.get('[data-cy=submit]').click();
        cy.url().should('eq', Cypress.env('HOST_URL') + 'home');
        openSidebar();
        cy.get('[data-cy=sidebar-logout]').click();
        cy.url().should('eq', Cypress.env('HOST_URL') + 'login');
    });

    it('Upload scan', () => {
        loginAsAdmin();
        cy.visit(Cypress.env('HOST_URL'));
        openSidebar();
        cy.get('[data-cy=sidebar-upload]').click();
        matSelect('[data-cy=datasets]', 'Kidneys');
        cy.get('[data-cy=datasets-submit]').click();
        cy.get('[data-cy=single-scan]').click();
        setFilesInInput('scans/scan.dcm', 11);
        cy.get('[data-cy=single-scan-upload]').click();
        cy.contains(/Upload completed sucessfully!/, {timeout: 60000}); // uploading scan is time consuming so we must increase timeout
    });

    it.only('Chain selector', () => {
        loginAsAdmin();
        cy.visit(Cypress.env('HOST_URL'));
        openSidebar();
        cy.get('[data-cy=sidebar-labelling]').click();
        cy.get('[data-cy=next1]').click();
        cy.get('[data-cy=next2]').click();
        cy.get('[data-cy=next3]').click();
        cy.get('[data-cy=not-show]').click(); // unchecked "Do not show this tutorial again", we want execute the same steps every time
        cy.get('[data-cy=next4]').click();
        cy.get('[data-cy=task]:nth-child(1)').click({force: true}); // clicking on svg has bug, https://github.com/cypress-io/cypress/issues/2245
        matSelect('[data-cy=tags]', 'Left Kidney');
        cy.get('[data-cy=chain-tool]').click({force: true});
        cy.get('canvas').click(100, 100);
        cy.get('canvas').click(200, 100);
        cy.get('canvas').click(200, 200);
        cy.get('.action-buttons button:contains(Stop)').click();
        cy.get('canvas').click(300, 300);
        cy.get('canvas').click(200, 300);
        cy.get('canvas').click(300, 200);
        cy.get('.action-buttons button:contains(Loop)').click();
        cy.get('[data-cy=send-label]').click();
    });
});
