from django.db import models


class Region(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True)

    class Meta:
        verbose_name = "Viloyat"
        verbose_name_plural = "Viloyatlar"
        ordering = ["name"]

    def __str__(self):
        return self.name


class District(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name="districts")
    name = models.CharField(max_length=100, db_index=True)

    class Meta:
        verbose_name = "Tuman"
        verbose_name_plural = "Tumanlar"
        unique_together = ("region", "name")
        ordering = ["region__name", "name"]

    def __str__(self):
        return f"{self.name} ({self.region.name})"
