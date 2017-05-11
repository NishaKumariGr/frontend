from __future__ import print_function        # make print a function
import mysql.connector                       # mysql functionality
import sys                                   # for misc errors
import cmd                                   # for creating line-oriented command processors
import shlex

SERVER   = "sunapee.cs.dartmouth.edu"        # db server to connect to
USERNAME = "f002bz6"                            # user to connect as
PASSWORD = "quarpiz59."                            # user's password
DATABASE = "f002bz6_db"                              # db to user
      # query statement

class command_Line_Interact(cmd.Cmd):
    """Command processor"""
    
    # 
    def do_register(self, line):
        table, firstname,lastname,email, address = shlex.split(line)
        print_table(table, self.cursor)
        Insert = "INSERT INTO `{0}` (`FirstName`,`LastName`,`MiddleName`,`EmailAddress`,`MailingAddress`, `Affiliation`) VALUES (\"{1}\",\"{2}\",NULL,\"{3}\",\"{4}\",NULL);".format(table,firstname,lastname,email,address)
        self.cursor.execute(Insert)
        self.con.commit()        
        print_table(table, self.cursor)

    def do_exit(self, line):
        self.cursor.close()
        self.con.close()
        return True
        

    def do_EOF(self, line):
        return True

    def extract_cursor(self, cur, con):
      self.cursor = cur
      self.con = con

# printing the table
def print_table(table_name, cursor):
      QUERY = "SELECT * FROM " + table_name + ";"
      cursor.execute(QUERY)
      print("Query executed: '{0}'\n\nResults:".format(QUERY))

      # print table header
      print("".join(["{:<12}".format(col) for col in cursor.column_names]))
      print("--------------------------------------------")

      # iterate through results
      for row in cursor:
        print("".join(["{:<12}".format(col) for col in row]))



if __name__ == "__main__":
    try:
      # initialize db connection
      con = mysql.connector.connect(host=SERVER,user=USERNAME,password=PASSWORD,
                                    database=DATABASE)

      print("Connection established.")
      
      # initialize a cursor
      cursor = con.cursor()
      com_intr = command_Line_Interact()
      com_intr.extract_cursor(cursor, con)
      com_intr.cmdloop()
      
      # cleanup
      con.close()
      cursor.close()

    except mysql.connector.Error as e:        # catch SQL errors
      print("SQL Error: {0}".format(e.msg))
   
    
      
    print("\nConnection terminated.", end='')
