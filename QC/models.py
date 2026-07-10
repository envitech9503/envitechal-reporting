from django.db import models

# Create your models here.
class Dw_rds(models.Model):
    sample_id = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now=True)
    rds = models.JSONField(default=dict)
    
    
    def __str__(self):
    
        return f"{self.sample_id} {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
    
    
class Ww_rds(models.Model):
    sample_id = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now=True)
    rds = models.JSONField(default=dict)
    
    
    def __str__(self):
    
        return f"{self.sample_id} {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
    
    
class QCAuditConfig(models.Model):
    use_manual_dw = models.BooleanField(default=False)
    use_manual_ww = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "QC Audit Config"

    def __str__(self):
        return "QC Audit Configuration"
    
    
class TestingResultsOfDWSamples(models.Model):
    sample_id = models.CharField(max_length=500)
    title = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now=True)
    results = models.JSONField(default=dict)
    location = models.CharField(max_length=500,null=True)
    
    
class TestingResultsOfWWSamples(models.Model):
    sample_id = models.CharField(max_length=500)
    title = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now=True)
    results = models.JSONField(default=dict)
    location = models.CharField(max_length=500,null=True)
    