# Databricks notebook source
# utilisation du RDD pour creer une jointure entre monument, cities, departements
# creer un ID en aggregation de REF_CODEDEPT_CODEINSEE_DEPT
#
from pyspark.sql import SQLContext, Row
sqlContext = SQLContext(sc)

# COMMAND ----------

#preparation des requêtes
citiesRDD=spark.sql("select c.insee_code, c.slug from cities c where c.insee_code=67529").rdd.map(list)
deptsRDD=spark.sql("select d.code, d.slug from departments d where d.code=67").rdd.map(list)
monumentsRDD=spark.sql("select m.INSEE, concat(m.STAT,'__',m.DPRO,'__',TRIM(m.REF),'__',m.DPT,'__',m.REG ) from monument m where m.INSEE = 67529").rdd.map(list)

# COMMAND ----------

# premiere jointure
monuments_citiesRDD=monumentsRDD.join(citiesRDD)

def splitCities(a):
  ar = a[1][0].split("__")
  result=[ar[3], a[0]+'__'+ar[0]+'__'+ar[1]+'__'+ar[2]+'__'+ar[4]+'__'+a[1][1]]
  return result

# COMMAND ----------

# deuxieme jointure
monuments_cities_deptRDD=monuments_citiesRDD.map(splitCities).join(deptsRDD)

def splitDepts(a):
  ar = a[1][0].split("__")
  result=[ar[3]+"_"+a[0]+"_"+ar[0]+"_"+ar[4], a[0],ar[0],ar[1],ar[2],ar[3],ar[4],ar[5],a[1][1]]
  return(Row(ID=str(result[0]), DEPTCODE=str(result[1]),DEPT=str(result[6]), INSEE=str(result[2]), STAT=str(result[3]),DPRO=str(result[4]),REF=str(result[5]),VILLE=str(result[6]),REG=str(result[6])))

# COMMAND ----------

#conversion du RDD en un RDD DF ready
monuments_cities_dept=monuments_cities_deptRDD.map(splitDepts)

# COMMAND ----------

#creation d'un DF à partir du RDD
myDF = sqlContext.createDataFrame(monuments_cities_dept)
myDF.printSchema()


# COMMAND ----------

display(myDF)

# COMMAND ----------

#enregistrement de la table
permanent_table_name = "newMonuments"
#myDF.write.format("parquet").saveAsTable(permanent_table_name)
