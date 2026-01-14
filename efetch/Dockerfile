# Use the official Ubuntu base image
FROM ubuntu:20.04

# Install Dependencies
RUN apt-get update
RUN apt-get -y install software-properties-common
RUN add-apt-repository -y ppa:gift/stable
RUN add-apt-repository -y ppa:sift/stable
RUN apt-get update
RUN apt -y install  python-dev python-setuptools unoconv zlib1g-dev libjpeg-dev libtiff5-dev
RUN apt-get install python3-pip -y
RUN apt-get -y install ffmpeg poppler-utils unzip libxml2-utils foremost wget
RUN apt-get -y install imagemagick ssdeep 
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install wkhtmltopdf
RUN apt-get -y install p7zip-full rar unace-nonfree cabextract
RUN apt-get -y install libevtx-tools
RUN pip install setuptools -U
RUN pip install --upgrade pip setuptools wheel packaging
RUN pip install plaso
RUN apt-get -y install pst-utils
RUN apt -y install  libpff1
RUN pip install libpff-python
RUN apt-get update && apt-get install -y \
    procps \
    wget \
    bzip2 \
    build-essential \
    libssl-dev \
    libffi-dev \
    build-essential \
    git \
    make \
    parallel \
    jq \
    && apt-get clean

# JD-CLI
RUN apt-get -y install default-jre
RUN mkdir /opt/jd-cli
RUN wget https://github.com/kwart/jd-cmd/releases/download/jd-cmd-0.9.2.Final/jd-cli-0.9.2-dist.tar.gz -O /opt/jd-cli/jd-cli.tar.gz
RUN tar xvzf /opt/jd-cli/jd-cli.tar.gz -C /opt/jd-cli/

# Scalpel
RUN apt-get -y install scalpel
RUN sed -i '/\spdf\s/s/^#//g' /etc/scalpel/scalpel.conf
RUN sed -i '/\sjpg\s/s/^#//g' /etc/scalpel/scalpel.conf
RUN sed -i '/\spng\s/s/^#//g' /etc/scalpel/scalpel.conf
RUN sed -i '/\sgif\s/s/^#//g' /etc/scalpel/scalpel.conf
RUN sed -i '/\szip\s/s/^#//g' /etc/scalpel/scalpel.conf
RUN sed -i '/\smpg\s/s/^#//g' /etc/scalpel/scalpel.conf
RUN sed -i '/\sdoc\s/s/^#//g' /etc/scalpel/scalpel.conf

# Fix wkhtmltopdf bug, see https://github.com/wkhtmltopdf/wkhtmltopdf/issues/2037
RUN wget https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.3/wkhtmltox-0.12.3_linux-generic-amd64.tar.xz -O /opt/wkhtmltox.tar.xz
RUN tar vxf /opt/wkhtmltox.tar.xz -C /opt/
RUN cp /opt/wkhtmltox/bin/wk* /usr/local/bin/
RUN rm -rf /opt/wkhtmltox

# PyLnker
RUN wget https://raw.githubusercontent.com/HarmJ0y/pylnker/master/pylnker.py -O /opt/pylnker.py

# Ole Tools
RUN pip install -U oletools

# Office Parser
RUN wget https://github.com/unixfreak0037/officeparser/archive/master.zip -O /opt/officeparser.zip
RUN unzip /opt/officeparser.zip -d /opt/
RUN rm /opt/officeparser.zip
RUN mv /opt/officeparser* /opt/officeparser
RUN python /opt/officeparser/setup.py install

# Floss - SKIP these if not needed for efetch
# RUN pip install https://github.com/williballenthin/vivisect/zipball/master
# RUN pip install https://github.com/fireeye/flare-floss/zipball/master

# PyPowerShellXray (needs vivisect) - SKIP this too
# RUN wget https://github.com/JohnLaTwC/PyPowerShellXray/archive/master.zip -O /opt/psxray.zip
# RUN unzip /opt/psxray.zip -d /opt/
# RUN rm /opt/psxray.zip
# RUN mv /opt/PyPowerShellXray* /opt/psxray

# BMC Tools
RUN wget https://github.com/ANSSI-FR/bmc-tools/archive/master.zip -O /opt/bmc-tools.zip
RUN unzip /opt/bmc-tools.zip -d /opt/
RUN rm /opt/bmc-tools.zip
RUN mv /opt/bmc-tools* /opt/bmc-tools
# Ent
RUN apt-get -y install ent

# Viper Monkey
RUN pip install -U https://github.com/decalage2/ViperMonkey/archive/master.zip

# Origami (PDF Parse)
RUN apt-get -y install rubygems
RUN apt-get -y install ruby-dev
RUN gem install therubyracer
RUN gem install origami

# Sflock 
RUN pip install sflock

# Change ImageMagic Policy to allow convert
RUN sed -i 's/none/read|write/' /etc/ImageMagick-6/policy.xml 

RUN pip install Jinja2

# Install NCBI E-utilities (efetch)
RUN wget -qO- https://ftp.ncbi.nlm.nih.gov/entrez/entrezdirect/install-edirect.sh | bash
ENV PATH="/root/edirect:${PATH}"

WORKDIR /usr/local/src/