# Web Scrapy in Python

A scrapy project to collect apartment information from [otodom](https://www.otodom.pl) website in Warsaw - Motokow and Wola areas.

The information will be saved in ./result.csv for furture analyze.


### Run in local PC
1.install the related library
```
pip install -r requirements.txt
```
2.Run the code
```
python start.py
```


### (option) create a lambda image in local PC
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

### (option) delopy it in AWS Lambda
1. Choose the created registry, you can check 'push command'

2. If create and push the image from windows OS, need to install AWS Tools in advance, open powershell with administrator role.
```
Install-Module -Name AWS.Tools.ECR
Set-ExecutionPolicy RemoteSigned
```
![image](https://github.com/user-attachments/assets/617403a0-45f8-4e87-a6f6-537378644db6)

3. Create the access token for local PC to push image by AWS CLI, use properly strategy
![image](https://github.com/user-attachments/assets/f2ec3bee-b620-4757-9a3e-1d4f21a114b6)
```
{
        "Version": "2012-10-17",
        "Statement": [
                {
                        "Sid": "ListImagesInRepository",
                        "Effect": "Allow",
                        "Action": [
                                "ecr:ListImages"
                        ],
                        "Resource": "*"
                },
                {
                        "Sid": "ManageRepositoryContents",
                        "Effect": "Allow",
                        "Action": [
                                "ecr:BatchCheckLayerAvailability",
                                "ecr:GetDownloadUrlForLayer",
                                "ecr:GetRepositoryPolicy",
                                "ecr:DescribeRepositories",
                                "ecr:ListImages",
                                "ecr:DescribeImages",
                                "ecr:BatchGetImage",
                                "ecr:InitiateLayerUpload",
                                "ecr:UploadLayerPart",
                                "ecr:CompleteLayerUpload",
                                "ecr:PutImage"
                        ],
                        "Resource": "*"
                },
                {
                        "Sid": "GetAuthorizationToken",
                        "Effect": "Allow",
                        "Action": [
                                "ecr:GetAuthorizationToken"
                        ],
                        "Resource": "*"
                }
        ]
}
```

4. Configure the token in the local PC
```
aws configure
```

5. Create a private registry in ECR in AWS webservice
![image](https://github.com/user-attachments/assets/cbe50d71-16c3-41b5-8e5e-59c44fddfc70)

if want to deploy the image into the AWS Lambda, must rename the image, begin with address of AWS ECR
```
docker tag myspider:latest 058264127206.dkr.ecr.eu-west-1.amazonaws.com/myspider:latest
```
or
```
docker build -t 058264127206.dkr.ecr.eu-west-1.amazonaws.com/myspider:latest .
```
then push the image to the ECR
```
docker push 058264127206.dkr.ecr.eu-west-1.amazonaws.com/myspider:latest
```

### deploy the image in lambda
1. Go to AWS Lambda, create a function, choose create from the container, you will find the image we uploaded before.
2. Get in the created function, create a trigger, you can use API Gateway to trigger this function.
![image](https://github.com/user-attachments/assets/dee99f38-a2a5-4fd0-86e0-32baec740d5e)

3. You can check logs from AWS CloudWatch

