# MySpider
A scarpy project to collect apartment information from '[otodom](https://www.otodom.pl)' website in Warsaw - Motokow and Wola areas.

The information will be saved in ./result.csv for furture analyze.

### Run the project
use start.py to start the spider

#### 1 Run in local PC
1.install the related library
```
pip install -r requirements.txt
```
2.Run the code
```
python start.py
```


#### (option) 2  create a lambda image in local PC
build the image
```
docker build -t myspider .
```
test from local pc
```
docker run -idt -p 9000:8080 --name=myspidercontainer myspider
```
send http to test
```
curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{"payload":"hello world!"}'\n
```
#### (option) 3 delopy it in AWS Lambda


if want to deploy the image into the AWS Lambda, must rename the image, begin with address of AWS ECR
```
docker tag myspider:latest 058264127206.dkr.ecr.eu-west-1.amazonaws.com/myspider:latest
```
or
```
docker build -t 058264127206.dkr.ecr.eu-west-1.amazonaws.com/myspider:latest .

#### 2
download in the mytest.csv