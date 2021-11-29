from datetime import date
import datetime
import sqlite3
class Database():
    def __init__(self, name):
        self.conn=sqlite3.connect(name)
    def getProfile(self,id):
        cmd="SELECT ID, name FROM STUDENT WHERE ID="+str(id)
        cursor=self.conn.execute(cmd)
        for row in cursor.fetchall():
            id=row[0]
            name=row[1]
        # self.conn.close()
        return (id,name)
    def getClassName(self, classID):
        cmd ="SELECT name FROM CLASS_INFO WHERE ID="+str(classID)
        cursor=self.conn.execute(cmd)
        data = ""
        for row in cursor.fetchall():
            data = str(row[0])
        # self.conn.close()
        return data
    def getClassTable(self, classId):
        cmd ="SELECT ID, name, phone_number FROM STUDENT WHERE class_id="+str(classId)
        cursor=self.conn.execute(cmd)
        data = []
        for row in cursor.fetchall():
            data.append([str(row[0]),row[1],row[2]])
        # self.conn.close()
        return data
    def getAttendanceList(self, dateDelay):
        date = datetime.datetime.today() + datetime.timedelta(days=dateDelay)
        date = date.strftime ('%Y-%m-%d')
        cmd ="SELECT student_id FROM ATTENDANCE WHERE date_time='"+str(date)+"'"
        cursor=self.conn.execute(cmd)
        data=[]
        for row in cursor.fetchall():
            data.append(str(row[0]))
        # self.conn.close()
        return data
    def insertAttendance(self,id):
        cmd ="INSERT INTO ATTENDANCE(student_id,date_time) VALUES("+str(id)+",'"+str(date.today())+"')"
        cursor=self.conn.execute(cmd)
        data=[]
        for row in cursor.fetchall():
            data.append(str(row[0]))
        self.conn.commit()

