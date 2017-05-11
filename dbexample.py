from __future__ import print_function        # make print a function
import mysql.connector                       # mysql functionality
import sys                                   # for misc errors
import cmd                                   # for creating line-oriented command processors
import shlex

SERVER   = "sunapee.cs.dartmouth.edu"        # db server to connect to
USERNAME = "f002bz6"                            # user to connect as
PASSWORD = "quarpiz59."                            # user's password
DATABASE = "f002bz6_db"                              # db to user
QUERY    = "SELECT * FROM AUTHOR;"       # query statement

class command_Line_Interact(cmd.Cmd):
    """Command processor"""
    
    # 
    def do_register(self, line):
        tokens = shlex.split(line)
        print (tokens[0])
        #print (firstname)
        #print (lastname)
        #print (email)
        #print (address)

        if tokens[0] == "AUTHOR":
          Insert = "INSERT INTO `{0}` (`FirstName`,`LastName`,`MiddleName`,`EmailAddress`,`MailingAddress`, `Affiliation`) VALUES (\"{1}\",\"{2}\",NULL,\"{3}\",\"{4}\",NULL);".format(tokens[0],tokens[1],tokens[2],tokens[3],tokens[4])
        elif tokens[0] == "EDITOR":
          Insert = "INSERT INTO `{0}` (`FirstName`,`LastName`,`MiddleName`) VALUES (\"{1}\",\"{2}\",NULL);".format(tokens[0],tokens[1],tokens[2])
        elif tokens[0] == "REVIEWER":
          lenOfList=len(tokens)
          if lenOfList==3:
            Insert = "INSERT INTO `{0}` (FirstName`,`EmailId`,`Affiliation`,`RICode1`,`RICode2`,`RICode3`,`LastName`,`MiddleName`) VALUES (\"{1}\",NULL,NULL,\"{2}\",NULL,NULL,\"{3}\",NULL);".format(tokens[0],tokens[1],tokens[3],tokens[2])
          elif lenOfList==4:
            Insert = "INSERT INTO `{0}` (FirstName`,`EmailId`,`Affiliation`,`RICode1`,`RICode2`,`RICode3`,`LastName`,`MiddleName`) VALUES (\"{1}\",NULL,NULL,\"{2}\",\"{3}\",NULL,\"{4}\",NULL);".format(tokens[0],tokens[1],tokens[3],tokens[4],tokens[2])
          elif lenOfList==5:
            Insert = "INSERT INTO `{0}` (FirstName`,`EmailId`,`Affiliation`,`RICode1`,`RICode2`,`RICode3`,`LastName`,`MiddleName`) VALUES (\"{1}\",NULL,NULL,\"{2}\",\"{3}\",\"{4}\",\"{5}\",NULL);".format(tokens[0],tokens[1],tokens[3],tokens[4],tokens[5],tokens[2])


        print (Insert)
        self.cursor.execute(Insert)
        self.con.commit()
        self.cursor.execute(QUERY)
        print("Query executed: '{0}'\n\nResults:".format(QUERY))

        # print table header
        print("".join(["{:<12}".format(col) for col in cursor.column_names]))
        print("--------------------------------------------")

        # iterate through results
        for row in cursor:
          print("".join(["{:<12}".format(col) for col in row]))
    
    def do_exit(self, line):
        self.cursor.close()
        self.con.close()
        return True
        

    def do_EOF(self, line):
        return True

    def extract_cursor(self, cur, con):
      self.cursor = cur
      self.con = con


if __name__ == "__main__":
    try:
      # initialize db connection
      con = mysql.connector.connect(host=SERVER,user=USERNAME,password=PASSWORD,
                                    database=DATABASE)

      print("Connection established.")
      
      # initialize a cursor
      cursor = con.cursor()

      # query db

      com_intr = command_Line_Interact()
      com_intr.extract_cursor(cursor, con)
      com_intr.cmdloop()
      # cleanup
      con.close()
      cursor.close()

    except mysql.connector.Error as e:        # catch SQL errors
      print("SQL Error: {0}".format(e.msg))
    except:                                   # anything else
      print("Unexpected error: {0}".format(sys.exc_info()[0]))
   
    
      
    print("\nConnection terminated.", end='')
