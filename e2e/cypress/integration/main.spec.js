import {goToLabeling, loginAsAdmin, matSelect, uploadScans} from '../support/utils';

describe('Basic flow', () => {

    beforeEach(() => {
        // local session and cookies are cleared automatically before each test so we don't have to do this manually
        // we need to clear only session storage
        window.sessionStorage.clear();
    });

    afterEach(() => {
        // if we refresh site during test, this hook won't execute
        // use beforeEach() instead
    });

    it('Login as admin and logout', () => {
        cy.visit(Cypress.env('HOST_URL'));
        cy.get('[data-cy=login-email]').type('admin@medtagger');
        cy.get('[data-cy=login-password]').type('medtagger');
        cy.get('[data-cy=submit]').click();
        cy.url().should('eq', Cypress.env('HOST_URL') + 'tutorial');
        cy.get('[data-cy=not-show]').click(); // unchecked "Do not show this tutorial again", we want execute the same steps every time
        cy.get('[data-cy=end-tutorial').click();
        cy.get('[data-cy=navbar-user-dropdown]').click();
        cy.get('[data-cy=navbar-user-dropdown-logout-button]').click();
        cy.url().should('eq', Cypress.env('HOST_URL') + 'login');
    });

    it('Upload scan', () => {
        loginAsAdmin();
        uploadScans('Kidneys', 1);
    });

    it('Rectangle selector', () => {
        loginAsAdmin();
        uploadScans('Kidneys', 11);
        goToLabeling('Kidneys segmentation');
        matSelect('[data-cy=tags]', 'Left Kidney');
        cy.get('[data-cy=rectangle-tool]').click();
        cy.get('canvas').trigger('mousedown', 200, 200, {timeout: 15000});
        cy.get('canvas').trigger('mousemove', 300, 300);
        cy.get('canvas').trigger('mouseup', {force: true});
        cy.get('[data-cy=send-label]').click();
        cy.get('[data-cy=no-labels-added]');
    });

    it('Point selector', () => {
        loginAsAdmin();
        uploadScans('Lungs', 11);
        goToLabeling('Find middle of the Spine');
        matSelect('[data-cy=tags]', 'Middle of the Spine');
        cy.get('[data-cy=point-tool]').click();
        cy.get('canvas').click(100, 100, {timeout: 15000});
        cy.get('canvas').click(200, 100);
        cy.get('canvas').click(200, 200);
        cy.get('[data-cy=send-label]').click();
        cy.get('[data-cy=no-labels-added]');
    });

    it('Chain selector', () => {
        // Watch on Label endpoint
        cy.server();
        cy.route('POST', '/api/v1/scans/*/*/label').as('addLabel');

        // Prepare for labeling
        loginAsAdmin();
        uploadScans('Heart', 11);
        goToLabeling('Find narrowings');
        matSelect('[data-cy=tags]', 'Narrowing (lenghtwise)');
        cy.get('[data-cy=chain-tool]').click();

        cy.get('[data-cy=spinner]').should('not.exist', {timeout: 15000});
 
        // Enter first Chain element
        cy.get('canvas').moveAndClick(300, 300);
        cy.get('canvas').moveAndClick(200, 300);
        cy.get('canvas').moveAndClick(300, 200);
        // Click on first point makes loop and completes chain
        cy.get('canvas').moveAndClick(300, 300);
 
        // Enter second Chain element
        cy.get('canvas').moveAndClick(100, 100);
        cy.get('canvas').moveAndClick(200, 100);
        cy.get('canvas').moveAndClick(200, 200);
        // NOTE: cannot simulate right click to stop drawing chain but sending label will have the same effect

        // Send and check Label in backend
        cy.get('[data-cy=send-label]').click();
        // TODO: While drawing first chain, second invokation of function moveAndClick(300, 300) doesn't guarantee that click will take place on the first point
        //       and chain will be ended. In result there is a chance that we will draw one long chain instead of two short chains. We need more trusted way
        //       to end chain (e.g. right click simulation that isn't supported by Cypress now) 
        // cy.wait('@addLabel').then(function(xhr) {
        //     let labelId = xhr.response.body.label_id;
        //     let token = window.sessionStorage.getItem('authorizationToken');
        //     cy.request({url: Cypress.env('API_URL') + `labels/${labelId}`, headers: {Authorization: `Bearer ${token}`}}).then(function(response) {
        //         let labelElements = response.body.elements;
        //         expect(labelElements.length).equals(2);
        //     });
        // });
 
        // UI should be empty once again
        cy.get('[data-cy=no-labels-added]');
    });

    it('Brush selector', () => {
        loginAsAdmin();
        uploadScans('Heart', 11);
        goToLabeling('Find narrowings in Veins');
        matSelect('[data-cy=tags]', 'Narrowing (region)');
        cy.get('[data-cy=brush-tool]').click();
        cy.get('canvas').trigger('mousedown', 200, 200, {timeout: 15000});
        cy.get('canvas').trigger('mousemove', 220, 200);
        cy.get('canvas').trigger('mousemove', 240, 200);
        cy.get('canvas').trigger('mousemove', 240, 250);
        cy.get('canvas').trigger('mousemove', 300, 250);
        cy.get('canvas').trigger('mouseup');
        cy.get('[data-cy=send-label]').click();
        cy.get('[data-cy=no-labels-added]');
    });
});
