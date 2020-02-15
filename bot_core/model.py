import sqlite3


class Model:


    # def make_connection(func):
    #     def wrapper(*args, **kwargs):
    #         conn = sqlite3.connect('F:/python/Vk_Feed_Bot/app.db')
    #         cursor = conn.cursor()
    #         result = func(*args, **kwargs)
    #         conn.commit()
    #         cursor.close()
    #         conn.close()
    #         return result
    #     return wrapper

    # make db
    adres = 'W:/vk_feed_bot/app.db'

    def make_DB(self,):
        conn = sqlite3.connect(self.adres)
        cursor = conn.cursor()
        cursor.execute(
            'CREATE TABLE IF NOT EXISTS `users`('
            '`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL ,'
            '`telegram_id` INTEGER,'
            '`name` VARCHAR(50),'  
            '`Users_Token` VARCHAR(120) NOT NULL,'
            '`group_amount` INT DEFAULT 0 ,'
            '`is_searching` BIT DEFAULT 0);'
        )

        cursor.execute(
            'CREATE TABLE IF NOT EXISTS `groups`('
            '`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL ,'
            'group_id VARCHAR(100),'
            '`group_name` VARCHAR(100),'
            '`last_pub_time` INT DEFAULT 0,'
            "`emoji` CHARACTER DEFAULT '.',"
            '`user_id` INT NOT NULL);'
        )




    def set_user(self, tg_id, name,token):
        conn = sqlite3.connect(self.adres)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users(`telegram_id`, `name`, `Users_Token`) VALUES(?);", (tg_id, name, token,))
        conn.commit()
        cursor.close()
        conn.close()

    def get_user(self, user_id):
        conn = sqlite3.connect(self.adres)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM `users` WHERE `id`=?',(user_id,))
        user_data = cursor.fetchall();
        conn.commit()
        cursor.close()
        conn.close()
        return user_data['from_user']


    def update_amount(self, plus_minus, user_id):
        conn = sqlite3.connect(self.adres)
        cursor = conn.cursor()
        cursor.execute('SELECT group_amount FROM users WHERE id=?', (user_id,))
        db_response = cursor.fetchall()[0][0]
        db_response += plus_minus
        cursor.execute("UPDATE users SET group_amount=? WHERE id=? ", ( db_response, user_id, ))
        conn.commit()
        cursor.close()
        conn.close()

    # groups
    def add_group(self, group_id, group_name, emoji, user_id):
        conn = sqlite3.connect(self.adres)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO groups(`group_id`, `group_name`, `emoji`, `user_id`) VALUES(?, ?, ?, ?)", (group_id, group_name, emoji, user_id,)
        )
        conn.commit()
        cursor.close()
        conn.close()

    def delete_group(self,  group_id , user_id):
        conn = sqlite3.connect(self.adres)
        cursor = conn.cursor()
        cursor.execute( "DELETE FROM groups WHERE group_id=? AND User_id=? ",( group_id, user_id,) )
        conn.commit()
        cursor.close()
        conn.close()

    def get_sub_list(self, user_id):
        conn = sqlite3.connect(self.adres)
        cursor = conn.cursor()
        cursor.execute('SELECT group_id FROM groups WHERE user_id=?',(user_id,) )
        sub_list =  cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()

        return  sub_list



    def get_last_pub_time(self,group_id):
        conn = sqlite3.connect(self.adres)
        cursor = conn.cursor()
        cursor.execute('SELECT last_pub_time FROM groups WHERE group_id=?', (group_id,))
        time = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()

        return  time


    def get_emoji_n_name(self, group_id, user_id):
        conn = sqlite3.connect(self.adres)
        cursor = conn.cursor()
        cursor.execute('SELECT group_name FROM groups WHERE group_id=? AND user_id=?', (group_id, user_id,))
        name = cursor.fetchall()[0][0]
        cursor.execute('SELECT emoji FROM groups WHERE group_id=? AND user_id=?', (group_id, user_id,))
        emoji = cursor.fetchall()[0][0]
        conn.commit()
        cursor.close()
        conn.close()

        return name, emoji


    def update_last_pub_time(self, time, group_id, user_id):
        conn = sqlite3.connect(self.adres)
        cursor = conn.cursor()
        cursor.execute("UPDATE groups SET last_pub_time=? WHERE User_id=? AND group_id=? ", (time, user_id, group_id,))
        conn.commit()
        cursor.close()
        conn.close()


m = Model()

# m.reg_user('1095597354:AAFdxv1QCmdTMw3emW5Iy3frcZ_v7rIpnbQ')
# {'content_type': 'text', 'message_id': 1813, 'from_user': {'id': 419356001, 'is_bot': False, 'first_name': 'Misha', 'username': 'Misha_40in', 'last_name': 'Sorokin', 'language_code': 'ru'}, 'date': 1581672169, 'c
