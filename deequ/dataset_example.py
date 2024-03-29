from pyspark.sql import SparkSession, Row

import pydeequ
from pydeequ.analyzers import *
from pydeequ.profiles import *
from pydeequ.checks import *
from pydeequ.verification import *

spark = (
    SparkSession.builder.config("spark.jars.packages", pydeequ.deequ_maven_coord)
    .config("spark.jars.excludes", pydeequ.f2j_maven_coord)
    .getOrCreate()
)

df = spark.sparkContext.parallelize(
    [Row(a="foo", b=1, c=5), Row(a="bar", b=2, c=6), Row(a="baz", b=3, c=None)]
).toDF()


print(df.show())

analysisResult = (
    AnalysisRunner(spark)
    .onData(df)
    .addAnalyzer(Size())
    .addAnalyzer(Completeness("b"))
    .run()
)

analysisResult_df = AnalyzerContext.successMetricsAsDataFrame(spark, analysisResult)
print(analysisResult_df.show())


check = Check(spark, CheckLevel.Warning, "Review Check")

checkResult = (
    VerificationSuite(spark)
    .onData(df)
    .addCheck(
        check.hasSize(lambda x: x >= 3)
        .hasMin("b", lambda x: x == 0)
        .isComplete("c")
        .isUnique("a")
        .isContainedIn("a", ["foo", "bar", "baz"])
        .isNonNegative("b")
    )
    .run()
)

checkResult_df = VerificationResult.checkResultsAsDataFrame(spark, checkResult)
checkResult_df.show()
