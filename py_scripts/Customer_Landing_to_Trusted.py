import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
import re

args = getResolvedOptions(sys.argv, ["JOB_NAME"])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# Script generated for node S3 Customer Landing
S3CustomerLanding_node1 = glueContext.create_dynamic_frame.from_options(
    format_options={"multiline": False},
    connection_type="s3",
    format="json",
    connection_options={
        "paths": ["s3://congdinh2023-stedi-lakehouse/customer/landing/"],
        "recurse": True,
    },
    transformation_ctx="S3CustomerLanding_node1",
)

# Script generated for node Filter Customer Agreed
FilterCustomerAgreed_node2 = Filter.apply(
    frame=S3CustomerLanding_node1,
    f=lambda row: (not (row["shareWithResearchAsOfDate"] == 0)),
    transformation_ctx="FilterCustomerAgreed_node2",
)

# Script generated for node S3 Customer Trusted
S3CustomerTrusted_node3 = glueContext.write_dynamic_frame.from_options(
    frame=FilterCustomerAgreed_node2,
    connection_type="s3",
    format="json",
    connection_options={
        "path": "s3://congdinh2023-stedi-lakehouse/customer/trusted/",
        "partitionKeys": [],
    },
    transformation_ctx="S3CustomerTrusted_node3",
)

job.commit()