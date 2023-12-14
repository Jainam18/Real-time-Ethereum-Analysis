FROM datamechanics/spark:2.4.5-hadoop-3.1.0-java-8-scala-2.11-python-3.7-dm18

ENV PYSPARK_MAJOR_PYTHON_VERSION=3

WORKDIR /opt/application

COPY requirements.txt .

USER root
RUN apt-get update --allow-insecure-repositories
RUN apt-get install build-essential manpages-dev -y

# RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
# RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
# RUN apt-get -y update --allow-insecure-repositories
# RUN apt-get install -y google-chrome-stable

# RUN apt-get install -yqq unzip
# RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
# RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

RUN pip3 install --upgrade pip 
RUN pip3 install -r requirements.txt
# RUN pip3 install pandas pyarrow 
# RUN pip3 install -U --upgrade pyspark
# RUN apt-get -y update --allow-insecure-repositories
# RUN apt-get install --fix-missing -y xvfb  
# RUN apt-get -y install libxfont2 
# RUN apt-get -y install gnome
# RUN apt-get -y install xorg
# RUN apt-get -y install "X Window System" "Desktop" "Fonts" "General Purpose Desktop"
# RUN Xvfb :99 -screen 0 1024x768x24 &
# ENV DISPLAY=:1

COPY . .

CMD ./run.sh