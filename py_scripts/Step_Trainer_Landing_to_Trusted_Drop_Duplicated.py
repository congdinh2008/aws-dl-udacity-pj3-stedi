import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrame
from pyspark.sql import functions as SqlFuncs

args = getResolvedOptions(sys.argv, ["JOB_NAME"])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# Script generated for node S3 Step Trainer
S3StepTrainer_node1 = glueContext.create_dynamic_frame.from_options(
    format_options={"multiline": False},
    connection_type="s3",
    format="json",
    connection_options={
        "paths": ["s3://congdinh2023-stedi-lakehouse/step_trainer/landing/"],
        "recurse": True,
    },
    transformation_ctx="S3StepTrainer_node1",
)

# Script generated for node S3 Customer Curated
S3CustomerCurated_node1680598203799 = glueContext.create_dynamic_frame.from_catalog(
    database="stedi",
    table_name="customer_curated",
    transformation_ctx="S3CustomerCurated_node1680598203799",
)

# Script generated for node Join Step Trainer with Customer Curated
JoinStepTrainerwithCustomerCurated_node2 = Join.apply(
    frame1=S3StepTrainer_node1,
    frame2=S3CustomerCurated_node1680598203799,
    keys1=["serialNumber"],
    keys2=["serialnumber"],
    transformation_ctx="JoinStepTrainerwithCustomerCurated_node2",
)

# Script generated for node Drop Fields From Customer
DropFieldsFromCustomer_node1680598443770 = DropFields.apply(
    frame=JoinStepTrainerwithCustomerCurated_node2,
    paths=[
        "customername",
        "email",
        "phone",
        "birthday",
        "serialnumber",
        "registrationdate",
        "lastupdatedate",
        "sharewithresearchasofdate",
        "sharewithpublicasofdate",
    ],
    transformation_ctx="DropFieldsFromCustomer_node1680598443770",
)

# Script generated for node Drop Duplicates Step Trainer
DropDuplicatesStepTrainer_node1680601486201 = DynamicFrame.fromDF(
    DropFieldsFromCustomer_node1680598443770.toDF().dropDuplicates(),
    glueContext,
    "DropDuplicatesStepTrainer_node1680601486201",
)

# Script generated for node S3 Step Trainer Trusted
S3StepTrainerTrusted_node3 = glueContext.write_dynamic_frame.from_options(
    frame=DropDuplicatesStepTrainer_node1680601486201,
    connection_type="s3",
    format="json",
    connection_options={
        "path": "s3://congdinh2023-stedi-lakehouse/step_trainer/trusted/",
        "partitionKeys": [],
    },
    transformation_ctx="S3StepTrainerTrusted_node3",
)

job.commit()
