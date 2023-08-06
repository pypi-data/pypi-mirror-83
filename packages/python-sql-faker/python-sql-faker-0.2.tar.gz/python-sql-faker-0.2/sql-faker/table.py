from sql-faker.database_types.idatabase import IDatabase
from sql-faker.foreign_key import ForeignKey
from sql-faker.primary_key import PrimaryKey
from sql-faker.column import Column
from numpy import array


class Table:
    """The table class lets you add column families to a database.
    
    A table is a collection of columns of which some are primary keys,
    others are foreign keys and some might be regular columns. For the
    sake of fake data creation, you have to select a number of rows
    that should be created for this table.

    :param table_name: Name of the table to be created
    :param db_object: The database, the table belongs to
    :param n_rows: The number of rows that should be created for DML
    :type table_name: String
    :type db_object: Python sql-faker Database object
    :type n_rows: Integer
    """

    def __init__(self, table_name: str, db_object, engine: IDatabase, n_rows: int = 100):
        # Store parameters in object
        self._table_name = table_name
        self._n_rows = n_rows

        self._engine = engine

        # store own database object
        self._db_object = db_object

        # Add room for all columns of this table
        self.columns = {}

    def add_column(self, column_name: str, data_target: str = "name", data_type: str = "int", not_null=False, **kwargs):
        """This method adds a new column to a table.
        
        :param column_name: The column's name
        :type column_name: String
        :param data_type: The sql data type that should be used in DDL
        :type data_type: String
        :param not_null: Flag indicating if column is NOT NULL
        :type not_null: Boolean
        :param data_target: The type of data that should be created by faker
        :type data_target: String
        """

        self.columns[column_name] = Column(
            # add column properties
            column_name=column_name,
            data_type=data_type,
            ai=False,
            not_null=not_null,
            data_target=data_target,
            engine=self._engine,
            kwargs=kwargs,

            # auto add table properties
            n_rows=self._n_rows,
            table_object=self
        )

    def add_foreign_key(self, column_name: str, target_table, target_column):
        """This method adds a foreign key column to a table.

        :param column_name: Name of the foreign key to add
        :param target_table: Name of referenced table
        :param target_column: Name of referenced column
        :type column_name: String
        :type target_table: String
        :type target_column: String
        """

        self.columns[column_name] = ForeignKey(

            # add foreign key properties
            column_name=column_name,
            target_table=target_table,
            target_column=target_column,

            # auto add table properties
            n_rows=self._n_rows,
            target_db=self._db_object,
            table_object=self,

            engine=self._engine
        )

    def add_primary_key(self, column_name: str):
        """This method adds a primary key column to a table.
        
        :param column_name: Name of the foreign key to add
        """

        self.columns[column_name] = PrimaryKey(
            # add foreign key properties
            column_name=column_name,

            # auto add table properties
            n_rows=self._n_rows,
            table_object=self,

            engine=self._engine
        )

    def generate_data(self, recursive, lang):
        """This method iterates all columns and calls their data generation method.
        
        :param recursive: Whether data generation is done for recursive data
        :type recursive: Boolean
        :returns: None
        """
        for key in self.columns.keys():
            self.columns[key].generate_data(recursive=recursive, lang=lang)

    def return_ddl(self):
        """This method returns the DDL script of a table.
        
        :returns: DDL statement as String
        """
        ddl_output = self._engine.create_table(self._db_object._db_name, self._table_name)

        for key in self.columns:
            if type(self.columns[key]) is not ForeignKey and type(self.columns[key]) is not PrimaryKey:
                ddl_output += self.columns[key].return_ddl()
            elif type(self.columns[key]) is PrimaryKey:
                ddl_output += self.columns[key].return_primary_column()
            else:
                ddl_output += self.columns[key].return_foreign_column()

        # remove the comma at the end of the last line
        ddl_output = ddl_output[:-2]

        # add closing bracket
        ddl_output += "\n);\n\n"

        return ddl_output

    def return_dml(self):
        """This method returns a table's DML script.

        :returns: DML statement as String
        """
        data = []
        attributes = []
        datatype = []

        # get all data into one place
        for key in self.columns:
            datatype.append(self.columns[key]._data_type)
            data.append(self.columns[key].data)
            attributes.append(key)

        # transpose the data
        data = array(data).transpose()

        return self._engine.insert_data(self._db_object._db_name, self._table_name, self._n_rows, attributes, data,
                                        datatype)
