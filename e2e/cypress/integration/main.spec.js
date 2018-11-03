import {goToLabeling, loginAsAdmin, matSelect, openSidebar, uploadScans} from '../support/utils';

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
        cy.get('[data-cy=login-email]').type('admin@medtagger.com');
        cy.get('[data-cy=login-password]').type('medtagger1');
        cy.get('[data-cy=submit]').click();
        cy.url().should('eq', Cypress.env('HOST_URL') + 'home');
        openSidebar();
        cy.get('[data-cy=sidebar-logout]').click();
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
        cy.get('[data-cy=rectangle-tool]').click({force: true});
        cy.get('canvas').trigger('mousedown', 200, 200);
        cy.get('canvas').trigger('mousemove', 300, 300);
        cy.get('canvas').trigger('mouseup');
        cy.get('[data-cy=send-label]').click();
        cy.get('[data-cy=no-labels-added]');
    });

    it('Point selector', () => {
        loginAsAdmin();
        uploadScans('Lungs', 11);
        goToLabeling('Find middle of the Spine');
        matSelect('[data-cy=tags]', 'Middle of the Spine');
        cy.get('[data-cy=point-tool]').click({force: true});
        cy.get('canvas').click(100, 100);
        cy.get('canvas').click(200, 100);
        cy.get('canvas').click(200, 200);
        cy.get('[data-cy=send-label]').click();
        cy.get('[data-cy=no-labels-added]');
    });

    it('Chain selector', () => {
        loginAsAdmin();
        uploadScans('Heart', 11);
        goToLabeling('Find narrowings');
        matSelect('[data-cy=tags]', 'Narrowing (lenghtwise)');
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
        cy.get('[data-cy=no-labels-added]');
    });

    it('Brush selector', () => {
        loginAsAdmin();
        uploadScans('Heart', 11);
        goToLabeling('Find narrowings in Veins');
        matSelect('[data-cy=tags]', 'Narrowing (region)');
        cy.get('[data-cy=brush-tool]').click({force: true});
        cy.get('canvas').trigger('mousedown', 200, 200);
        cy.get('canvas').trigger('mousemove', 220, 200);
        cy.get('canvas').trigger('mousemove', 240, 200);
        cy.get('canvas').trigger('mousemove', 240, 250);
        cy.get('canvas').trigger('mousemove', 300, 250);
        cy.get('canvas').trigger('mouseup');
        cy.get('[data-cy=send-label]').click();
        cy.get('[data-cy=no-labels-added]');
    });
});
