import sqlite3


class Model:

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


    def set_user(self, tg_id, name, token):
        conn = sqlite3.connect(self.adres)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users(`telegram_id`, `name`, `Users_Token`) VALUES(?,?,?);", (tg_id, name, token,))
        conn.commit()
        cursor.close()
        conn.close()

    def get_user(self, tg_id):
        conn = sqlite3.connect(self.adres)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM `users` WHERE `telegram_id`=?',(tg_id,))
        user_data = cursor.fetchall();
        conn.commit()
        cursor.close()
        conn.close()
        return user_data

    def get_all_users(self):
        conn = sqlite3.connect(self.adres)
        cursor = conn.cursor()
        cursor.execute('SELECT `telegram_id` FROM `users`')
        users = cursor.fetchall();
        conn.commit()
        cursor.close()
        conn.close()
        return users

    def set_isSearching(self, tg_id, bool):
        conn = sqlite3.connect(self.adres)
        cursor = conn.cursor()
        cursor.execute('UPDATE `users` SET `is_searching`=? WHERE `telegram_id`=?', (bool, tg_id))
        conn.commit()
        cursor.close()
        conn.close()


    def update_amount(self, plus_minus, user_id):
        conn = sqlite3.connect(self.adres)
        cursor = conn.cursor()
        cursor.execute('SELECT `group_amount` FROM `users` WHERE `id`=?', (user_id,))
        db_response = cursor.fetchall()[0][0]
        db_response += plus_minus
        cursor.execute("UPDATE `users` SET `group_amount`=? WHERE id=? ", ( db_response, user_id, ))
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

    def get_sub_list(self, tg_id):
        conn = sqlite3.connect(self.adres)
        cursor = conn.cursor()
        user_id = self.get_user(tg_id)[0][0]
        print(user_id)
        cursor.execute('SELECT group_id FROM groups WHERE user_id=?',(user_id,))
        sub_list = cursor.fetchall()
        if len(sub_list) == 0:
            return []
        else:
            return sub_list
        conn.commit()
        cursor.close()
        conn.close()


    def get_last_pub_time(self, group_id, tg_id):
        conn = sqlite3.connect(self.adres)
        cursor = conn.cursor()
        user_id = self.get_user(tg_id)[0][0]
        cursor.execute('SELECT last_pub_time FROM groups WHERE group_id=? AND user_id=?', (group_id, user_id))
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

    def update_last_pub_time(self, time, group_id, tg_id):
        conn = sqlite3.connect(self.adres)
        cursor = conn.cursor()
        user_id = self.get_user(tg_id)[0][0]
        cursor.execute("UPDATE groups SET last_pub_time=? WHERE User_id=? AND group_id=? ", (time, user_id, group_id,))
        conn.commit()
        cursor.close()
        conn.close()


m = Model()
# m.set_isSearching(419356001, 1)
# print(m.get_user(419356001)[0][5])
# a = m.get_last_pub_time('konturgusya', 419356001)
# print(a)
print(m.get_all_users())
# m.reg_user('1095597354:AAFdxv1QCmdTMw3emW5Iy3frcZ_v7rIpnbQ')
# {'content_type': 'text', 'message_id': 1813, 'from_user': {'id': 419356001, 'is_bot': False, 'first_name': 'Misha', 'username': 'Misha_40in', 'last_name': 'Sorokin', 'language_code': 'ru'}, 'date': 1581672169, 'c
