#coding=utf-8
from django.db import models
import pymongo

class Step(models.Model):
    title = models.CharField(max_length = 60)
    userCount = models.IntegerField()
    problemCount = models.IntegerField()
    allAcCount = models.IntegerField()
    orgId = models.IntegerField()
    source = models.CharField(max_length = 30)

def Step_save(step):
    client = pymongo.MongoClient(host = "127.0.0.1", port = 27017)
    db = client.StepByStepData
    db.stepList.insert(step)

def Step_Update(id, step):
    client = pymongo.MongoClient(host = "127.0.0.1", port = 27017)
    db = client.StepByStepData
    db.stepList.update({"id": id}, step)

def Step_Delete(id):
    client = pymongo.MongoClient(host = "127.0.0.1", port = 27017)
    db = client.StepByStepData
    db.stepList.remove({"id": id})