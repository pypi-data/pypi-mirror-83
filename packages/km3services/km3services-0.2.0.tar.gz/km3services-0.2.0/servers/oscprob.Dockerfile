FROM rootproject/root:6.22.02-centos7

ARG OSCPROB_DIR="/OscProb"
ARG ENTRYPOINT="/usr/bin/docker-entrypoint.sh"

ENV LC_ALL=en_US.utf-8
ENV LANG=en_US.utf-8

RUN mkdir $OSCPROB_DIR && \
    cd $OSCPROB_DIR && \
    git clone --recursive https://github.com/joaoabcoelho/OscProb.git . && \
    make

RUN python3 -m pip install "git+https://git.km3net.de/km3py/km3services.git#egg=project[oscprob-server]"

ENV LD_LIBRARY_PATH="${OSCPROB_DIR}:${LD_LIBRARY_PATH}"

CMD ["python3", "-m", "uvicorn", "km3services.oscprob:app", "--reload", "--port=30000", "--host=0.0.0.0"]
