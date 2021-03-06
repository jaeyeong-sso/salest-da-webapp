from __future__ import unicode_literals

from django.db import models

# Create your models here.


class HdfsClusterInfo(models.Model):
    class Meta:
        db_table = 'hdfs_cluster_info'
    
    id = models.IntegerField
    configured_capacity = models.CharField(max_length=200)
    present_capacity = models.CharField(max_length=200)
    dfs_used = models.CharField(max_length=200)
    
    def get_dfs_used(self):
        return self.dfs_used

   
class DailyTrSummary(models.Model):
    class Meta:
        db_table = 'daily_tr_summary'
    
    id = models.IntegerField
    date = models.DateTimeField
    num_of_order = models.IntegerField
    total_amount = models.BigIntegerField

