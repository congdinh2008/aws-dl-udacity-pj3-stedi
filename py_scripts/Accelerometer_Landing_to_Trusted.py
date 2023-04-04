import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

args = getResolvedOptions(sys.argv, ["JOB_NAME"])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# Script generated for node S3 Accelerometer Landing
S3AccelerometerLanding_node1 = glueContext.create_dynamic_frame.from_options(
    format_options={"multiline": False},
    connection_type="s3",
    format="json",
    connection_options={
        "paths": ["s3://congdinh2023-stedi-lakehouse/accelerometer/landing/"],
        "recurse": True,
    },
    transformation_ctx="S3AccelerometerLanding_node1",
)

# Script generated for node S3 Customer Trusted
S3CustomerTrusted_node1680596513396 = glueContext.create_dynamic_frame.from_options(
    format_options={"multiline": False},
    connection_type="s3",
    format="json",
    connection_options={
        "paths": ["s3://congdinh2023-stedi-lakehouse/customer/trusted/"],
        "recurse": True,
    },
    transformation_ctx="S3CustomerTrusted_node1680596513396",
)

# Script generated for node Join Accelerometer and Trusted Customer
JoinAccelerometerandTrustedCustomer_node2 = Join.apply(
    frame1=S3CustomerTrusted_node1680596513396,
    frame2=S3AccelerometerLanding_node1,
    keys1=["email"],
    keys2=["user"],
    transformation_ctx="JoinAccelerometerandTrustedCustomer_node2",
)

# Script generated for node Drop Fields from Trusted Customer
DropFieldsfromTrustedCustomer_node1680596775090 = DropFields.apply(
    frame=JoinAccelerometerandTrustedCustomer_node2,
    paths=[
        "serialNumber",
        "shareWithPublicAsOfDate",
        "birthDay",
        "registrationDate",
        "shareWithResearchAsOfDate",
        "customerName",
        "email",
        "lastUpdateDate",
        "phone",
        "shareWithFriendsAsOfDate",
    ],
    transformation_ctx="DropFieldsfromTrustedCustomer_node1680596775090",
)

# Script generated for node S3 bucket
S3bucket_node3 = glueContext.write_dynamic_frame.from_options(
    frame=DropFieldsfromTrustedCustomer_node1680596775090,
    connection_type="s3",
    format="json",
    connection_options={
        "path": "s3://congdinh2023-stedi-lakehouse/accelerometer/trusted/",
        "partitionKeys": [],
    },
    transformation_ctx="S3bucket_node3",
)

job.commit()