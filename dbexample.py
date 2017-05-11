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
    
    def do_register(self, line):
        tokens = shlex.split(line)
        print (tokens[0])
        if tokens[0] == "AUTHOR":
          Insert = "INSERT INTO `{0}` (`FirstName`,`LastName`,`MiddleName`,`EmailAddress`,`MailingAddress`, `Affiliation`) VALUES (\"{1}\",\"{2}\",NULL,\"{3}\",\"{4}\",NULL);".format(tokens[0],tokens[1],tokens[2],tokens[3],tokens[4])
        elif tokens[0] == "EDITOR":
          Insert = "INSERT INTO `{0}` (`FirstName`,`LastName`,`MiddleName`) VALUES (\"{1}\",\"{2}\",NULL);".format(tokens[0],tokens[1],tokens[2])
        elif tokens[0] == "REVIEWER":
          lenOfList=len(tokens)
          if lenOfList==3:
            Insert = "INSERT INTO `{0}` (`FirstName`,`EmailId`,`Affiliation`,`RICode1`,`RICode2`,`RICode3`,`LastName`,`MiddleName`) VALUES (\"{1}\",NULL,NULL,\"{2}\",NULL,NULL,\"{3}\",NULL);".format(tokens[0],tokens[1],tokens[3],tokens[2])
          elif lenOfList==4:
            Insert = "INSERT INTO `{0}` (`FirstName`,`EmailId`,`Affiliation`,`RICode1`,`RICode2`,`RICode3`,`LastName`,`MiddleName`) VALUES (\"{1}\",NULL,NULL,\"{2}\",\"{3}\",NULL,\"{4}\",NULL);".format(tokens[0],tokens[1],tokens[3],tokens[4],tokens[2])
          elif lenOfList==5:
            Insert = "INSERT INTO `{0}` (`FirstName`,`EmailId`,`Affiliation`,`RICode1`,`RICode2`,`RICode3`,`LastName`,`MiddleName`) VALUES (\"{1}\",NULL,NULL,\"{2}\",\"{3}\",\"{4}\",\"{5}\",NULL);".format(tokens[0],tokens[1],tokens[3],tokens[4],tokens[5],tokens[2])


        print (Insert)

        self.cursor.execute(Insert)
        self.con.commit()        
        print_table(tokens[0], self.cursor)

    def do_login(self, line):
      print("Welcome "+line)
      print("Here are your details:")

      self.id= line[1:]

      if line[0]=="A":
        self.table="AUTHOR"
        Select = "SELECT FirstName, LastName, MailingAddress FROM AUTHOR WHERE AuthorID = {0};".format(line[1:])
        man_report = "SELECT ManuscriptID, Status FROM MANUSCRIPT where ManuscriptID IN (SELECT ManuscriptID FROM AUTHORSINMANUSCRIPT WHERE AuthorID = {0} AND AuthorPlace = 1);".format(self.id)
        self.cursor.execute(man_report)
        print_table_select(self.cursor)
      elif line[0]=="E":
        self.table="EDITOR"
        Select = "SELECT FirstName, LastName FROM EDITOR WHERE EditorID = {0};".format(line[1:])
        man_report = "SELECT * FROM MANUSCRIPT  where EDITOR_idEDITOR = {0} ORDER BY status, Number;".format(self.id)
        self.cursor.execute(man_report)
        print_table_select(self.cursor)
      elif line[0]=="R":
        self.table="REVIEWER"
        Select = "SELECT FirstName, LastName FROM REVIEWER WHERE ReviewerID = {0};".format(line[1:])
        man_report = "SELECT ManuscriptID, Status FROM MANUSCRIPT where ManuscriptID in (SELECT ManuscriptID FROM REVIEW WHERE REVIEWER_idREVIEWER = {0}) ;".format(self.id)
        self.cursor.execute(man_report)
        print_table_select(self.cursor)
      

      self.cursor.execute(Select) 
      print_table_select(self.cursor)

      print_options(self.table)


    def do_STATUS (self, line):
      if self.table == "AUTHOR":
        man_report = "SELECT * FROM MANUSCRIPT where ManuscriptID IN (SELECT ManuscriptID FROM AUTHORSINMANUSCRIPT WHERE AuthorID = {0} AND AuthorPlace = 1);".format(self.id)
      elif self.table == "EDITOR":
        man_report = "SELECT * FROM MANUSCRIPT  where EDITOR_idEDITOR = {0} ORDER BY status, Number;".format(self.id)
      elif self.table == "REVIEWER":
        man_report = "SELECT ManuscriptID, Status FROM MANUSCRIPT where ManuscriptID in (SELECT ManuscriptID FROM REVIEW WHERE REVIEWER_idREVIEWER = {0}) ;".format(self.id)
      self.cursor.execute(man_report)
      print_table_select(self.cursor)

    def do_exit(self, line):
        self.cursor.close()
        self.con.close()
        return True
      
    def do_EOF(self, line):
        return True

    def extract_cursor(self, cur, con):
      self.cursor = cur
      self.con = con

    def do_RESIGN(self,line):
      print ("Welcome "+line)
      Resign_ReviewerReview="DELETE FROM REVIEW WHERE REVIEWER_idREVIEWER = {0};".format(line[1:])
      Resign_Reviewer="DELETE FROM REVIEWER WHERE ReviewerID ={0};".format(line[1:])
      self.cursor.execute(Resign_ReviewerReview)
      self.con.commit()
      self.cursor.execute(Resign_Reviewer)
      self.con.commit()
      print ("Thank you for your service")

    def do_RETRACT(self,line):
      response = raw_input ("Are you sure? (yes/no) \n")

      print (line)

      if response=="yes":
          Delete_man_in_issue="DELETE FROM Manuscripts_In_Issue WHERE ManuscriptID = {0};".format(line)
          Delete_authorinInManuscript = "DELETE FROM AUTHORSINMANUSCRIPT WHERE ManuscriptID = {0};".format(line)
          Delete_review = "DELETE FROM REVIEW WHERE ManuscriptID = {0};".format(line)
          Delete = "DELETE FROM MANUSCRIPT WHERE ManuscriptID = {0};".format(line)
          print (Delete_man_in_issue, Delete_authorinInManuscript, Delete_review, Delete)
          self.cursor.execute(Delete_man_in_issue)
          self.con.commit()
          self.cursor.execute(Delete_authorinInManuscript)
          self.con.commit()
          self.cursor.execute(Delete_review)
          self.con.commit()
          self.cursor.execute(Delete)
          self.con.commit()
          print("Manuscript "+line+" is deleted from the system!")


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

def print_table_select(cursor):
      print("".join(["{:<12}".format(col) for col in cursor.column_names]))
      print("--------------------------------------------")

      # iterate through results
      for row in cursor:
        print("".join(["{:<12}".format(col) for col in row]))

def print_options(table):
      print("\n*****************************")
      print ("What do you wish to to today?")
      print("\n*****************************")

      if table=="AUTHOR":
        print ("\n 1. submit\n 2. STATUS\n 3. RETRACT")
      elif table=="EDITOR":
        print ("\n 1. status\n 2. assign\n 3. reject\n 4. accept\n 5. typeset\n 6. schedule\n 7. publish")
      elif table=="REVIEWER":
        print ("\n 1. REVIEW-REJECT\n 2. REVIEW-REJECT")


if __name__ == "__main__":
    try:
      # initialize db connection
      con = mysql.connector.connect(host=SERVER,user=USERNAME,password=PASSWORD,
                                    database=DATABASE)

      print("Connection established.")
      
      # initialize a cursor
      cursor = con.cursor(buffered=True)
      com_intr = command_Line_Interact()
      com_intr.extract_cursor(cursor, con)
      com_intr.cmdloop()
      
      # cleanup
      con.close()
      cursor.close()

    except mysql.connector.Error as e:        # catch SQL errors
      print("SQL Error: {0}".format(e.msg))
   
    
      
    print("\nConnection terminated.", end='')
