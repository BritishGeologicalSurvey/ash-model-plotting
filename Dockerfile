FROM continuumio/miniconda3

RUN conda install -y -c conda-forge \
  iris iris-sample-data jupyterlab

# Add an iris user so that process doesn't run as root. This also means that
# files created on the host system belong to 1000:1000, not root:root.
# Files owned by root within Docker cannot usually be modified on the host
# system by non-root users.
RUN useradd -m iris
WORKDIR /home/iris
USER iris

# The 'owner' of a single user Linux system is  usually allocated id=1000. They
# will own these files outside the container.  If your id is different
# (run `id -u` to check), you can specify the id and gid by uncommenting the
# following line.
# RUN usermod --uid 1234 iris && groupmod --gid 1234 iris

#  For explanation of parameters, see:
#  https://stackoverflow.com/questions/49024624/how-to-dockerize-jupyter-lab
ENTRYPOINT [ "jupyter-lab", "--port=8888", "--ip=0.0.0.0" ]

