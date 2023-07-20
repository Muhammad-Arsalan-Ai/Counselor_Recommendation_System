from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F

from src.etl_service.base_logger import logger
from src.etl_service.extract import get_api_data, urls


def fetch_all_data(spark: SparkSession) -> dict:
    """
    Fetches data from the specified API URLs and returns the corresponding Spark DataFrames.

    Parameters:
    - spark: SparkSession
        The SparkSession object used to create the DataFrames.

    Returns:
    - dict:
        A dictionary containing the fetched DataFrames. The keys represent the data types, such as 'appointment',
        'councillor', 'patient_councillor', and 'rating', and the values are the corresponding Spark DataFrames.

    Preconditions:
    - The `get_api_data()` function should be implemented to fetch data from the API URLs.
    - The `urls` dictionary should contain the appropriate API URLs.
    - The `spark` parameter should be a valid SparkSession object.

    Returns:
    - dict:
        A dictionary containing the fetched DataFrames.
    """
    dataframes = {}
    for key, url in urls.items():
        data = get_api_data(url)
        dataframes[key] = spark.createDataFrame(data)

    logger.info("Data received from endpoints")

    return dataframes


def joined_data(spark: SparkSession) -> DataFrame:
    """
    Performs data joining based on appointment, councillor, patient-councillor, and rating DataFrames.

    Parameters:
    - spark: SparkSession
        The SparkSession object used to access the DataFrames.

    Returns:
    - DataFrame:
        The joined DataFrame containing the following columns:
        - 'councillor_id': The ID of the councillor associated with the appointment.
        - 'specialization': The specialization of the councillor.
        - 'value': The rating value associated with the appointment.

    Preconditions:
    - The `fetch_all_data()` function should be implemented and accessible to retrieve the required DataFrames.
    - The `spark` parameter should be a valid SparkSession object.

    Returns:
    - DataFrame:
        The joined DataFrame containing the desired columns.
    """

    dataframes = fetch_all_data(spark)

    appointment_df = dataframes["appointment"]
    councillor_df = dataframes["councillor"]
    patient_councillor_df = dataframes["patient_councillor"]
    rating_df = dataframes["rating"]
    joined_df = (
        appointment_df.join(
            patient_councillor_df,
            appointment_df["patient_id"] == patient_councillor_df["patient_id"],
        )
        .join(rating_df, appointment_df["id"] == rating_df["appointment_id"])
        .join(
            councillor_df, councillor_df["id"] == patient_councillor_df["councillor_id"]
        )
        .select(
            councillor_df["id"].alias("councillor_id"),
            councillor_df["specialization"],
            rating_df["value"],
        )
    )
    return joined_df


def data_transformations() -> dict:
    """
    Calculates the average rating for each councillor in each specialization based on the joined DataFrame.

    Returns:
    - specialization_tables: dict
        A dictionary where each key represents a specialization, and the corresponding value is a DataFrame
        containing the average rating information for each councillor within that specialization.

    Preconditions:
    - The `joined_data()` function should be called prior to invoking this function to obtain the joined DataFrame.

    Returns:
    - dict:
        A dictionary where each key represents a specialization, and the corresponding value is a DataFrame
        containing the average rating information for each councillor within that specialization.

    Notes:
    - This function creates and stops a SparkSession internally to perform the necessary transformations.
      The SparkSession is not expected to be passed as a parameter.

    Example Usage:
    ```
    result = data_transformations()
    for specialization, dataframe in result.items():
        print(f"Specialization: {specialization}")
        dataframe.show()
    ```
    """

    spark = SparkSession.builder.getOrCreate()

    joined_df = joined_data(spark)

    specializations = joined_df.select("specialization").distinct().collect()

    specialization_tables = {}

    for specialization_row in specializations:
        specialization = specialization_row["specialization"]

        filtered_df = joined_df.filter(joined_df["specialization"] == specialization)

        average_df = (
            (
                filtered_df.groupBy("councillor_id")
                .agg(F.avg("value").alias("average_value"))
                .orderBy(F.desc("average_value"))
                .drop("specialization")
            )
            .toJSON()
            .collect()
        )

        specialization_tables[specialization] = average_df

    spark.stop()
    logger.info("Data has been transformed")
    return specialization_tables


if __name__ == "__main__":
    data_transformations()
