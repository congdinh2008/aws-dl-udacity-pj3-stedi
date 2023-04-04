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

# Script generated for node S3 Accelerometer Trusted
S3AccelerometerTrusted_node1 = glueContext.create_dynamic_frame.from_catalog(
    database="stedi",
    table_name="accelerometer_trusted",
    transformation_ctx="S3AccelerometerTrusted_node1",
)

# Script generated for node S3 Step Trainer Trusted
S3StepTrainerTrusted_node1680602663516 = glueContext.create_dynamic_frame.from_catalog(
    database="stedi",
    table_name="step_trainer_trusted",
    transformation_ctx="S3StepTrainerTrusted_node1680602663516",
)

# Script generated for node Join Accelerometer Trusted with Step Trainer Trusted
JoinAccelerometerTrustedwithStepTrainerTrusted_node2 = Join.apply(
    frame1=S3AccelerometerTrusted_node1,
    frame2=S3StepTrainerTrusted_node1680602663516,
    keys1=["timestamp"],
    keys2=["sensorreadingtime"],
    transformation_ctx="JoinAccelerometerTrustedwithStepTrainerTrusted_node2",
)

# Script generated for node Drop Fields
DropFields_node1680602795355 = DropFields.apply(
    frame=JoinAccelerometerTrustedwithStepTrainerTrusted_node2,
    paths=["user"],
    transformation_ctx="DropFields_node1680602795355",
)

# Script generated for node S3 MachineLearningCurated
S3MachineLearningCurated_node3 = glueContext.write_dynamic_frame.from_options(
    frame=DropFields_node1680602795355,
    connection_type="s3",
    format="json",
    connection_options={
        "path": "s3://congdinh2023-stedi-lakehouse/machine_learning/curated/",
        "partitionKeys": [],
    },
    transformation_ctx="S3MachineLearningCurated_node3",
)

job.commit()