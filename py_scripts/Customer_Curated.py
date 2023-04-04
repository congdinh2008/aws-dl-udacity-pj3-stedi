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
S3CustomerTrusted_node1680597504967 = glueContext.create_dynamic_frame.from_options(
    format_options={"multiline": False},
    connection_type="s3",
    format="json",
    connection_options={
        "paths": ["s3://congdinh2023-stedi-lakehouse/customer/trusted/"],
        "recurse": True,
    },
    transformation_ctx="S3CustomerTrusted_node1680597504967",
)

# Script generated for node Join Accelerometer Landing with Customer Trusted
JoinAccelerometerLandingwithCustomerTrusted_node2 = Join.apply(
    frame1=S3CustomerTrusted_node1680597504967,
    frame2=S3AccelerometerLanding_node1,
    keys1=["email"],
    keys2=["user"],
    transformation_ctx="JoinAccelerometerLandingwithCustomerTrusted_node2",
)

# Script generated for node Drop Fields
DropFields_node1680597675966 = DropFields.apply(
    frame=JoinAccelerometerLandingwithCustomerTrusted_node2,
    paths=["z", "y", "x", "timeStamp", "user"],
    transformation_ctx="DropFields_node1680597675966",
)

# Script generated for node S3 Customers Curated
S3CustomersCurated_node3 = glueContext.write_dynamic_frame.from_options(
    frame=DropFields_node1680597675966,
    connection_type="s3",
    format="json",
    connection_options={
        "path": "s3://congdinh2023-stedi-lakehouse/customer/curated/",
        "partitionKeys": [],
    },
    transformation_ctx="S3CustomersCurated_node3",
)

job.commit()