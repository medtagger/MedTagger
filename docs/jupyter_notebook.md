Setting up Jupyter Notebook
---------------------------

At any time, you can use Jupyter Notebooks to analyse data collected with MedTagger.
 You can attach to the MedTagger internal data only if you set it up properly. In this
 tutorial, you will understand how to do so.

## Docker environment

If you have set up you environment with Docker Compose, you're lucky! That's because Jupyter
 Notebooks are already set up for you. A separate Jupyter Notebook server has been set up in
 one of MedTagger's containers. All you need to do is go to your browser at `localhost:52001`
 and `medtagger` as a password to the Jupyter.

**NOTE:** Please change the default password after first use!
 [Here](https://jupyter-notebook.readthedocs.io/en/stable/public_server.html) you can find
 more information about it.

## Vagrant & Native setup

If you've setup your environment using Vagrant or native approach, you can also use Jupyter
 Notebooks very easily. Just follow below instruction:

```bash
# Go to the backend and activate your development environment
$ cd backend/ && . ./devenv.sh

# Go back to the root of the MedTagger project and run Jupyter here
$ cd ../ && jupyter notebook
```

Now, go to the URL that is shown in your terminal.

## Example Notebooks

[Here](/examples/data_analysis) you can find some examples regarding data analysis in
 MedTagger. Feel free to use them as you want and create your own!
