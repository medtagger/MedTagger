FROM python:3.7.1

WORKDIR /medtagger_backend/

COPY Makefile ./Makefile
COPY alembic ./alembic
COPY medtagger ./medtagger
COPY scripts ./scripts
COPY tests ./tests

COPY .flake8 ./.flake8
COPY .pylintrc ./.pylintrc
COPY .test.pylintrc ./.test.pylintrc
COPY alembic.ini ./alembic.ini
COPY logging.conf ./logging.conf
COPY mypy.ini ./mypy.ini
COPY requirements.dev.txt ./requirements.dev.txt
COPY requirements.txt ./requirements.txt

ENV PYTHONPATH /medtagger_backend

ARG CASS_DRIVER_NO_CYTHON
ARG CASS_DRIVER_NO_EXTENSIONS
RUN pip install -r requirements.txt
RUN pip install -r requirements.dev.txt

ARG JUPYTER_NOTEBOOK_PASSWORD
RUN jupyter notebook --generate-config
RUN echo "c.NotebookApp.password='$JUPYTER_NOTEBOOK_PASSWORD'" >> /root/.jupyter/jupyter_notebook_config.py

EXPOSE 52001
CMD ["make", "install_dev_packages"]

