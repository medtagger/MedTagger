Running MedTagger Frontend in Vagrant
------------------------------------

Here you can find more information about running MedTagger Frontend in Vagrant.

### Requirements 

Please follow the documentation about setting up Vagrant [here](/docs/development_setup_vagrant.md).
 
**Note:** Keep in mind that Frontend will no work properly without Backend. To set it up follow
 the instructions [here](/backend/docs/development_in_vagrant.md).

### How to run Frontend?

Open one SSH connection to your virtual machine and make sure that you're inside `/vagrant/frontend`
 directory. Then run command below to start the web server:
 
```bash
$ make run_frontend
```
 
And that's all! You should be able to see MedTagger UI on `http://10.0.0.99:4200`. 

### How to log in?

There is default account for development purposes:
 - email: `admin@medtagger.com`,
 - password: `medtagger1`.
