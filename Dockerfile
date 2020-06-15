# Derived from https://github.com/jbindinga/java-notebook/blob/master/Dockerfile

FROM jupyter/minimal-notebook

USER root

# Install dependencies
RUN apt-get update && apt-get install -y \
  software-properties-common \
  curl

# Install Zulu OpenJdk 11 (LTS)
RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 0xB1998361219BD9C9 \
  && apt-add-repository 'deb http://repos.azulsystems.com/ubuntu stable main' \
  && apt install -y zulu-11

# Unpack and install the kernel
RUN curl -L https://github.com/SpencerPark/IJava/releases/download/v1.3.0/ijava-1.3.0.zip > ijava-kernel.zip
RUN unzip ijava-kernel.zip -d ijava-kernel \
  && cd ijava-kernel \
  && python3 install.py --sys-prefix

# Cleanup
RUN rm ijava-kernel.zip

# Add README.md
ADD "README.md" $HOME

# Set user back to priviledged user.
USER $NB_USER
