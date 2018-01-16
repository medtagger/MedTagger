Running MedTagger Frontend in Vagrant
------------------------------------

Here you can find more information about running MedTagger Frontend in Vagrant.

### Requirements 

Please follow the documentation about setting up Vagrant [here](/docs/development_setup_vagrant.md) and setting up 
backend [here](/backend/docs/development_in_vagrant.md).


### How to run frontend?

Open one SSH connections to your virtual machine and make sure that you're inside `/vagrant/frontend`
 directory. Then run command below to start the web server:
 
 ```bash
 $ make run_frontend
```
 
And that's all! You should be able to see MedTagger frontend on:
 `http://10.0.0.99:4200`. 
