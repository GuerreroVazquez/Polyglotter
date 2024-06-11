from GetDBSchema import GetDBSchema
import mysql.connector
import numpy as np
import math
config = {
    'user': '',
    'password': '',
    'host': '',
    'database': '',
    'raise_on_warnings': True,
    'auth_plugin':'mysql_native_password'
}

# Example 1: child class to get the schema of the HumanMine database
class MySQLGetDBSchema(GetDBSchema):
    def __init__(self, name, accessData):
        super().__init__(name, accessData)

        # Initialize MySQL service object
        self.service = mysql.connector.connect(**config)
    # This has to be abstract 
    def getClassWeight(self, className, reference): 
        cursor = self.service.cursor()
        cursor.execute("SELECT TABLE_ROWS FROM INFORMATION_SCHEMA.TABLES WHERE table_name = '" + className + "'")
        classWeight = cursor.fetchone()
        if classWeight[0] == 0:
            return -1
        return math.log(classWeight[0])

    def getDBSchema(self):       
        database_schema = dict()
        # Get classes
        schema = dict()

        cursor = self.service.cursor()
        cursor.execute("SELECT table_name FROM INFORMATION_SCHEMA.TABLES where table_schema = '" + self.accessData["database"] + "'")
        classes = cursor.fetchall()
        for clss in classes:
            if isinstance(clss[0], bytes):
                decoded_clss = clss[0].decode('UTF-8')
            else:
                decoded_clss = clss[0]

            if decoded_clss not in schema:
                schema[decoded_clss] = dict()

        # Table relationships
        cursor = self.service.cursor()
        cursor.execute("SELECT constraint_name, table_name, referenced_table_name FROM INFORMATION_SCHEMA.REFERENTIAL_CONSTRAINTS where UNIQUE_CONSTRAINT_SCHEMA = '" + self.accessData["database"] + "'")
        relationships = cursor.fetchall()
        for rltn in relationships:
            if rltn[2] not in schema[rltn[1]]:
                schema[rltn[1]][rltn[2]] = set()
            if rltn[0] not in schema[rltn[1]][rltn[2]]:
                schema[rltn[1]][rltn[2]].add(rltn[0])
        
        # Use the common format for this framework
        database_schema = dict()

        for element in schema.keys():
            database_schema[element] = {'references':list(),'attributes':list(),'weight':1/len(schema.keys())}
            try:
                database_schema[element]['weight'] = float(math.log(self.getClassWeight(element, "")+1, 10))

                for reference in schema[element]:
                    database_schema[element]['references'].append(reference)

                # Get the properties (attributes) of the node
                nodeProperties = set()
                cursor = self.service.cursor()
                cursor.execute("SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS where TABLE_NAME = '" + element + "'")
                attrs = cursor.fetchall()
                for attr in attrs:
                    if attr[0] not in nodeProperties:
                        nodeProperties.add(attr[0])

                for attribute in nodeProperties:
                    database_schema[element]['attributes'].append(attribute)
            except ValueError as ve:
                database_schema.pop(element)

        self.getGraphFromSchemaEdgeList(database_schema, "MySQLdbSchema.obj")

        print("The schema has " + str(len(database_schema.keys())) + " classes.")   

MySQLSchema = MySQLGetDBSchema('MySQL Example', {"host":config["host"], "user": config["user"], "passwd": config["password"], "database": config["database"], "port": 3360})
MySQLSchema.getDBSchema()