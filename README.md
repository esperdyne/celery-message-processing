Using Celery with RabbitMQ to Process Messages
==============================================

This is a example of how to use celery to process data and deploy to multiple targets. It has been written as part of a presentation for the 2015 NERD Summit, but the source code and tutorial can be useful for anyone who is getting started with celery and data processing and is straight-forward enough for anyone with a background in Python to use. The README file contains instructions how to get started from scratch (from a fresh vagrant virtual box, or any fresh Ubuntu install). I hope that this is helpful. Please send comments and/or questions to jpeck@esperdyne.com.

Introduction
------------

0. You have some data you need to process
0. You need to deploy this data to multiple targets
0. You want to do this efficienty, in parallel, and with control over the various stages

In this demo, I will show how to use celery with RabbitMQ to process the Enron emails (http://www.cs.cmu.edu/~enron/). I will start from scratch, on a fresh vagrant box. You can do this on any machine, but these setup instruction pertain to Ubuntu.

Getting Started
---------------

I used a vagrant box running 32-bit Ubuntu 12:
```
$ vagrant init hashicorp/precise32;
$ vagrant up --provider virtualbox
$ vagrant ssh
```

Inside the vagrant box (or whatever your environment is), I installed the latest updates, as well as pip, curl, and git:
```
$ sudo apt-get update
$ sudo apt-get upgrade
$ sudo apt-get install python-pip
$ sudo apt-get install curl
$ sudo apt-get install git
```

And then I installed RabbitMQ - this is the message broker:
```
sudo apt-get install rabbitmq-server
```

And Redis - the backend:
```
$ sudo apt-get install redis-server
$ sudo pip install redis
```

And, of course, celery:
```
$ sudo pip install celery
```

We will use fabric to interact with celery, so we install that:
```
$ sudo pip install fabric
```

And for the deploy targets in this email, we will need MySQL and ElasticSearch. This will install MySQL and the sqlachmey Python library. (Since I am using a vagrant box on a local machine, I chose no root password. Please adjust accordingly based on your security requirements):
```
$ sudo apt-get install mysql-server
$ sudo apt-get build-dep python-mysqldb
$ sudo pip install MySQL_python
$ sudo pip install sqlalchemy
```

Create the messages table (if you have a MySQL password, you will need to enter it here):
```
$ mysql -u root -e "CREATE DATABASE messages" 
```

To install and start elasticsearch:
```
$ sudo apt-get install openjdk-7-jre
$ wget -qO - https://packages.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -
$ echo "deb http://packages.elastic.co/elasticsearch/1.7/debian stable main" | sudo tee -a /etc/apt/sources.list.d/elasticsearch-1.7.list
$ sudo apt-get update && sudo apt-get install elasticsearch
$ sudo update-rc.d elasticsearch defaults 95 10
$ sudo pip install elasticsearch
$ sudo service elasticsearch start
```

Now, we are ready to set up the actual demo.

Setup Demo
----------

Check out a copy of this repository and enter the directory
```
$ git clone git@github.com:esperdyne/celery-message-processing.git
$ cd celery-message-processing
```

Download and unpack the dataset into the working directory. This contains about .5 million emails that were on Enron's servers and became public some years ago:
```
$ wget http://www.cs.cmu.edu/~enron/enron_mail_20150507.tgz
$ tar -xvf enron_mail_20150507.tgz
```

And that's it. You are now ready to start processing the dataset using Celery and RabbitMQ.

Usage
-----

TODO...

```
$ fab workers:start
$ fab process:maildir
```
