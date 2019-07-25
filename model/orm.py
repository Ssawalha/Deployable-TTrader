import sqlite3
from data.schema import DBPATH

class ORM:
    dbpath = DBPATH #<-- can be overwritten in inhereting class if desired. in this case is the same for all tables
    tablename = "" #<-- will be overwritten in inheriting classes
    fields = [] #<-- Column Headers in our tables | will be overwritten in inherting classes

    createsql = """ """ #<-- can be empty since account/position/trader will each have their own createsql (to create a table)

    def __init__(self, **kwargs):
        raise NotImplementedError

    def __repr__(self): #<-- what is printed when the print function is called on the class object (for debugging)
        template = "<{} ORM: pk={}>" 
        return template.format(self.tablename, self.values['pk']) #<-- red underline since ORM cant be instantiated, inhereting classes wont throw error
    
    def __getitem__(self, key):
        return self.values[key] #<-- red underline since ORM cant be instantiated, inhereting classes wont throw error

    def __setitem__(self, key, value):
        self.values[key] = value #<-- red underline since ORM cant be instantiated, inhereting classes wont throw error

    def save(self): 
        """if self.values['pk] exists, update row else
            insert row (class Account/Trade/Position)"""
        if self.values['pk']: #<-- red underline since ORM cant be instantiated, inhereting classes wont throw error
            self.update_row()
        else:
            self.insert_row()

    def insert_row(self):
        """insert the values from this istance into the db as a row,
        then return cursor.lastrowid, 
        \ncursor.lastrowid is id of last selected row (in this case inserted row)"""
        with sqlite3.connect(self.dbpath) as conn:
            curs = conn.cursor() #<-- curs allows to select in db
            fieldlist = ", ".join(self.fields) #<- .join returns a string of "field, " for each field in [fields]
            qmarks = ", ".join(['?' for _ in self.fields]) #<- .join returns a string of "?, " for each field in [fields] <- done to sanitize inputs
            SQL = """ INSERT INTO {} ({}) VALUES ({}); """.format( #<- SQL statement
                                                                  self.tablename, fieldlist, qmarks) #<- SQL statement continued
            values = [self.values[field] for field in self.fields]
            curs.execute(SQL, values) #<-- .execute() applies function to selected row (SQL statement is the SQL function), (values are our sanitized inputs in SQL statement)
            pk = curs.lastrowid #lastrowid --> read-only attribute provides the rowid of the last modified row. 
            self.values['pk'] = pk # ^ It is only set if you issued a INSERT statement using the execute() method.


    def update_row(self):#<-- when we call this function, we have already changed the class (Account/Trade/Position).values[field] and want to save it to db
        """update the row with this instance's pk value to the current
        values of this instance"""
        with sqlite3.connect(self.dbpath) as conn:
            curs = conn.cursor()
            # join a list of "column_name = ?" pairs
            set_equals = ", ".join(["{}=?".format(field) for field in self.fields]) #<-- same as in insert_row but condensed
            SQL = """ UPDATE {} SET {} WHERE pk=?; """.format(self.tablename,set_equals)
            values = [self.values[field] for field in self.fields] + [self.values['pk']]
            curs.execute(SQL, values)

    def delete(self):
        if self.values['pk'] is None:
            raise KeyError(self.__repr__() + " is not a row in " +
                            self.tablename)
        with sqlite3.connect(self.dbpath) as conn:
            curs = conn.cursor()
            SQL = """DELETE FROM {} WHERE pk = ?; """.format(self.tablename)
            curs.execute(SQL, (self.values['pk'],))

    @classmethod
    def create_table(cls):
        """run the cls.createsql SQL command"""
        with sqlite3.connect(cls.dbpath) as conn:
            curs = conn.cursor()
            curs.execute(cls.createsql)

    @classmethod
    def one_from_where_clause(cls, where_clause="", values=tuple()):
        SQL = "SELECT * FROM {} {};".format(cls.tablename, where_clause)
        with sqlite3.connect(cls.dbpath) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute(SQL, values)
            row = cur.fetchone()
            if not row:
                return None
            return cls(**row)

    @classmethod
    def all_from_where_clause(cls, where_clause="", values=tuple()):
        SQL = "SELECT * FROM {} {};".format(cls.tablename, where_clause)
        with sqlite3.connect(cls.dbpath) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute(SQL, values)
            rows = cur.fetchall()
            return [cls(**row) for row in rows]

    @classmethod
    def one_from_pk(cls, pk):
        return cls.one_from_where_clause("WHERE pk=?", (pk,))
