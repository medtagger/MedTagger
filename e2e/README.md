E2E Tests
---------

End-to-End Tests are designed to test whole application from the user perspective.
 To run them on your local machine, it is required to run both Backend and Frontend
 at the same time. We automated this process to keep it simple once your setup was
 properly prepared.

## How to run E2E?

To run E2E on your machine from scratch please set up your backend natively or inside
 of the Vagrant VM. Then execute below commands:

```bash
$ cd backend && . ./devenv.sh && cd ..
(venv) $ make e2e
```

Also, you can run them inside of the Docker containers in the same way as it is done
 in Travis CI. This setup also reflects full Production setup!

```bash
$ make e2e_docker
```

## Manual run

There is also a classic way to run Cypress tests. Before first execution fetch all
 needed packages by `npm install` command. Then to run tests type `npm start` and
 wait until Cypress window appears. Choose Specification file with defined tests
 from list.

## How to add new test?

To add new test create specification file in `e2e/cypress/integration` directory.

## Reference

To learn how to overwrite default configuration visit:

[https://docs.cypress.io/guides/guides/environment-variables.html](https://docs.cypress.io/guides/guides/environment-variables.html)

To learn about best practices read:

[https://docs.cypress.io/guides/references/best-practices.html](https://docs.cypress.io/guides/references/best-practices.html)
