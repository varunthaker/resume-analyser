from .models import UploadedCvData
from rest_framework import serializers

class UploadedCvDataSerializer(serializers.ModelSerializer):
    class Meta:
        model=UploadedCvData
        fields= ['resumeFile', 'language', 'aiModel']

    def validate_file(self, value):
        if not value.name.endswith('.pdf'):
            raise serializers.ValidationError("Only PDF files are allowed.")
        if value.size > 5 * 1024 * 1024:  
            raise serializers.ValidationError("File size must be under 5MB.")
        return value