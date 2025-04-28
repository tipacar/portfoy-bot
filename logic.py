import sqlite3
from config import DATABASE
skills = [ (_,) for _ in (['Python', 'SQL', 'API', 'Discord'])]
statuses = [ (_,) for _ in (['Prototip Oluşturma', 'Geliştirme Aşamasında', 'Tamamlandı, kullanıma hazır', 'Güncellendi', 'Tamamlandı, ancak bakımı yapılmadı'])]
class DB_Manager:
    def __init__(self, database):
        self.database = database # veri tabanının adı
        
    def create_tables(self):
        con= sqlite3.connect(self.database)
        with con:
            con.execute(""" CREATE TABLE IF NOT EXISTS projects(
                                        project_id INTEGER PRIMARY KEY,
                                        user_id INTEGER,
                                        project_name TEXT,
                                        description TEXT,
                                        url TEXT,
                                        status_id INTEGER,
                                        FOREIGN KEY(status_id) REFERENCES status(status_id))""")
            con.execute("""CREATE TABLE IF NOT EXISTS skills(
                        skill_id INTEGER PRIMARY KEY,
                        skill_name TEXT)""")
            con.execute("""CREATE TABLE IF NOT EXISTS project_skills(
                                        project_id INTEGER,
                                        skill_id INTEGER,
                                        FOREIGN KEY(project_id) REFERENCES projects(project_id),
                                        FOREIGN KEY(skill_id) REFERENCES skills(skill_id))""")
            con.execute("""CREATE TABLE IF NOT EXISTS status(
                                        status_id INTEGER PRIMARY KEY,
                                        status_name TEXT)""")
            
            data=[
                (0,"Python"),
                (1,"Discord bot geliştirme"),
                (2,"SQL"),
                (3,"API"),
                (4,"HTML"),
                (5,"CSS"),
                (6,"FLASK"),
                (7,"AI")
            ]
            con.executemany("INSERT INTO skills VALUES(?,?)",data)
            data=[
                (0,"Prototip Oluşturma"),
                (1,"Geliştirme Aşamasınd"),
                (2,"Tamamlanmış"),
                (3,"Güncelleme"),
                (4,"Terk edilmiş/Desteklenmiyor")
                    ]
            con.executemany("INSERT INTO status VALUES(?,?)",data)

            con.commit()
        con.close()
    def __executemany(self, sql, data):
        conn = sqlite3.connect(self.database)
        with conn:
            conn.executemany(sql, data)
            conn.commit()
    
    def __select_data(self, sql, data = tuple()):
        conn = sqlite3.connect(self.database)
        with conn:
            cur = conn.cursor()
            cur.execute(sql, data)
            return cur.fetchall()
        
    def default_insert(self):
        sql = 'INSERT OR IGNORE INTO skills (skill_name) values(?)'
        data = skills
        self.__executemany(sql, data)
        sql = 'INSERT OR IGNORE INTO status (status_name) values(?)'
        data = statuses
        self.__executemany(sql, data)


    def insert_project(self, data):
        sql = """INSERT INTO projects 
                        (user_id, project_name, url, status_id) 
                        values(?, ?, ?, ?)"""
 # Doğru SQL sorgusunu buraya girin
        self.__executemany(sql, data)


    def insert_skill(self, user_id, project_name, skill):
        sql = 'SELECT project_id FROM projects WHERE project_name = ? AND user_id = ?'
        project_id = self.__select_data(sql, (project_name, user_id))[0][0]
        skill_id = self.__select_data('SELECT skill_id FROM skills WHERE skill_name = ?', (skill,))[0][0]
        data = [(project_id, skill_id)]
        sql = 'INSERT OR IGNORE INTO project_skills VALUES(?, ?)'
        self.__executemany(sql, data)


    def get_statuses(self):
        sql="SELECT status_name from status"
        return self.__select_data(sql)
        

    def get_status_id(self, status_name):
        sql = 'SELECT status_id FROM status WHERE status_name = ?'
        res = self.__select_data(sql, (status_name,))
        if res: return res[0][0]
        else: return None

    def get_projects(self, user_id):
        sql="""SELECT * FROM projects 
                WHERE user_id = ?"""
        return self.__select_data(sql, data = (user_id,))
        
    def get_project_id(self, project_name, user_id):
        return self.__select_data(sql='SELECT project_id FROM projects WHERE project_name = ? AND user_id = ?  ', data = (project_name, user_id,))[0][0]
        
    def get_skills(self):
        return self.__select_data(sql='SELECT * FROM skills')
    
    def get_project_skills(self, project_name):
        res = self.__select_data(sql='''SELECT skill_name FROM projects 
                                    JOIN project_skills ON projects.project_id = project_skills.project_id 
                                    JOIN skills ON skills.skill_id = project_skills.skill_id 
                                    WHERE project_name = ?''', data = (project_name,) )
        return ', '.join([x[0] for x in res])
    
    def get_project_info(self, user_id, project_name):
        sql = """
                SELECT project_name, description, url, status_name FROM projects 
                JOIN status ON
                status.status_id = projects.status_id)
                WHERE project_name=? AND user_id=?
                """
        return self.__select_data(sql=sql, data = (project_name, user_id))


    def update_projects(self, param, data):
        sql = f"""UPDATE projects SET {param} = ? 
                WHERE project_name = ? AND user_id = ?"""
        self.__executemany(sql, [data]) 


    def delete_project(self, user_id, project_id):
        sql = """DELETE FROM projects 
                    WHERE user_id = ? AND project_id = ? """
        self.__executemany(sql, [(user_id, project_id)])
    
    def delete_skill(self, project_id, skill_id):
        sql = """DELETE FROM skills 
                WHERE skill_id = ? AND project_id = ? """
        self.__executemany(sql, [(skill_id, project_id)])
if __name__ == '__main__':
    dbmanager = DB_Manager(DATABASE)
    #dbmanager.create_tables()
    #proje ekleme testi
    #data=[("232323232","pokemon","hdhdhd","9")]
    #dbmanager.insert_project(data=data)
    #proje guncelleme
    #data=("description1","pokemon GO!","6636636363")
    #dbmanager.update_projects("description",data=data)B

    




