# syntax=docker/dockerfile:1
FROM continuumio/anaconda3
# ADD git@github.com:h-dychko/segmentation.git /home/segmentation
COPY . /home/segmentation

EXPOSE 8501

WORKDIR /home/segmentation

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

## Make RUN commands use `bash --login`:
SHELL ["/bin/bash", "--login", "-c"]

RUN conda init bash
RUN conda env create -f environment.yml
SHELL ["conda", "run", "-n", "segmentation", "/bin/bash", "-c"]


ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "segmentation", "streamlit", "run", "Start.py", "--server.port=8501", "--server.address=0.0.0.0"]
