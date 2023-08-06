from atlas_client.entity_source_generation.S3BucketEntityGenerator import S3BucketEntityGenerator
from atlas_client.entity_source_generation.S3ObjectEntityGenerator import S3ObjectEntityGenerator
from atlas_client.entity_source_generation.S3PsDirEntityGenerator import S3PsDirEntityGenerator


# get all supported entity types
def get_all_supported_entity_type():
    return ["aws_s3_bucket", "aws_s3_pseudo_dir", "aws_s3_object"]


def get_entity_supported_attributes(entity_type):
    if entity_type == "aws_s3_bucket":
        return S3BucketEntityGenerator.get_s3_bucket_all_supported_attributes()
    elif entity_type == "aws_s3_pseudo_dir":
        return S3PsDirEntityGenerator.get_s3_ps_dir_all_supported_attributes()
    elif entity_type == "aws_s3_object":
        return S3ObjectEntityGenerator.get_s3_object_all_supported_attributes()
    else:
        return "The entity type you entered is not supported yet."
