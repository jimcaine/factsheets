FROM python:3

# set environment variables
ENV FS_MONGO_HOST=factsheets-mongo
ENV FS_MONGO_PORT=27017

# install vim
RUN apt-get update
RUN apt-get install -y vim

# install node / npm
RUN apt-get install -y nodejs
RUN apt-get install -y npm

# install python packages
RUN pip install flask
RUN pip install flask-cors
RUN pip install pymongo
RUN pip install fpdf

# move directory files
COPY . /factsheets

# install node modules and build bundles
# RUN npm --prefix /factsheets/static install
# RUN npm --prefix /factsheets/static run build

# install factsheets
RUN pip install -e /factsheets

# load mongo db
#RUN python -c "import factsheets;factsheets.load_collection('funds', '/factsheets/factsheets/data.json')"