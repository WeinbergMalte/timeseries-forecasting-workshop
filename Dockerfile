# Specify the base image
FROM python:3.9

# Install Poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python

# Set up the environment
WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN poetry install

# Install Jupyter Lab
RUN pip install jupyterlab

# Set up Jupyter Lab
RUN jupyter lab --generate-config
COPY jupyter_notebook_config.py /root/.jupyter/

# Expose the port
EXPOSE 8888

# Set the working directory
WORKDIR /app

# Start Jupyter Lab
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--no-browser"]
