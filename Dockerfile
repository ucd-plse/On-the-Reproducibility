FROM ubuntu:20.04
ENV TZ=America/Los_Angeles

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN \
	apt-get update && \
  	apt-get install \
  		apt-utils \
    	apt-transport-https \
	    ca-certificates \
	    curl \
	    gnupg-agent \
	    software-properties-common \
		sudo \
	  	git-core \	  	
	  	vim \
	  	locales locales-all \
	  	lsb-release \
	  	ufw -y \
	  	apt-transport-https -y \
		gnupg \
		wget

RUN \
    apt-get -y install  openjdk-11-jdk\
                        openjdk-8-jdk\
                        maven\
                        virtualenv\
                        git\
                        subversion\
                        libapache2-mod-svn\
						build-essential\
						perl\
						unzip\
						cpanminus\
						make\
						python2

RUN \
	mkdir -p /etc/apt/keyrings &&\
	curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg && \
	echo \
	"deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
	$(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null &&\
	apt-get update &&\
  	apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin -y


RUN curl -L http://xrl.us/installperlnix | bash

RUN yes | cpan DBI

ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64

RUN update-java-alternatives -s java-1.8.0-openjdk-amd64 

RUN apt install python3.8 python3.8-dev python3.8-distutils python3.8-venv -y && \
	apt install python3-pip -y

RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.8 1 && \
	update-alternatives --set python /usr/bin/python3.8

RUN pip install docker==2.5.1 && \
	pip install requests==2.28.1 && \
	pip install pandas==1.4.3

RUN mkdir -p /root/.ssh && \
    ssh-keyscan -t rsa github.com >> ~/.ssh/known_hosts

ADD . /On-the-Reproducibility

RUN rm -rf /On-the-Reproducibility/section-2/reproducibility-scanner && \
	git clone --recurse-submodules -j5 https://github.com/ucd-plse/reproducibility-scanner.git /On-the-Reproducibility/section-2/reproducibility-scanner || :

RUN cp -r /On-the-Reproducibility/section-2/first-run/* /On-the-Reproducibility/section-2/reproducibility-scanner/outputs/

WORKDIR /On-the-Reproducibility/section-2/reproducibility-scanner   

RUN python init.py