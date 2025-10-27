import psycopg2
from datetime import datetime
class DB_connecter:
    def __init__(self, dbname, user, password, host='localhost', port=5432):
        """PostgreSQL bilan ulanish"""
        try:
            self.connection = psycopg2.connect(
                dbname=dbname,
                user=user,
                password=password,
                host=host,
                port=port
            )
            self.cursor = self.connection.cursor()
            print("✅ PostgreSQL bazasiga muvaffaqiyatli ulandik.")
        except Exception as e:
            print("❌ Ulanishda xatolik:", e)
            self.connection = None
            self.cursor = None
    # === Foydalanuvchilar bo‘limi ===
    def add_user(self, name, phone, address, age):
        if self.cursor is None:
            print("❌ Cursor mavjud emas.")
            return
        try:
            query = """
                INSERT INTO users (name, phone_number, address, age)
                VALUES (%s, %s, %s, %s);
            """
            self.cursor.execute(query, (name, phone, address, age))
            self.connection.commit()
            print("✅ Foydalanuvchi qo‘shildi!")
        except Exception as e:
            print("⚠️ Xatolik:", e)
    def show_users(self):
        if self.cursor is None:
            print("❌ Cursor mavjud emas.")
            return
        try:
            self.cursor.execute("SELECT * FROM users ORDER BY id;")
            rows = self.cursor.fetchall()
            if not rows:
                print("📭 Jadval bo‘sh.")
            else:
                print("\n📋 Foydalanuvchilar ro‘yxati:")
                for row in rows:
                    print(f"ID: {row[0]} | Name: {row[1]} | Phone: {row[2]} | Address: {row[3]} | Age: {row[4]}")
                print("----------------------------")
        except Exception as e:
            print("⚠️ Xatolik:", e)
    def update_user(self, user_id, new_name, new_phone, new_address, new_age):
        if self.cursor is None:
            print("❌ Cursor mavjud emas.")
            return
        try:
            query = """
                UPDATE users
                SET name = %s, phone_number = %s, address = %s, age = %s
                WHERE id = %s;
            """
            self.cursor.execute(query, (new_name, new_phone, new_address, new_age, user_id))
            self.connection.commit()
            if self.cursor.rowcount > 0:
                print("♻️ Ma’lumot yangilandi!")
            else:
                print("❌ Bunday ID topilmadi.")
        except Exception as e:
            print("⚠️ Xatolik:", e)
    def delete_user(self, user_id):
        if self.cursor is None:
            print("❌ Cursor mavjud emas.")
            return
        try:
            query = "DELETE FROM users WHERE id = %s;"
            self.cursor.execute(query, (user_id,))
            self.connection.commit()
            if self.cursor.rowcount > 0:
                print("🗑️ Foydalanuvchi o‘chirildi!")
            else:
                print("❌ Bunday ID topilmadi.")
        except Exception as e:
            print("⚠️ Xatolik:", e)
    # === SMS BO‘LIMI ===
    def add_sms(self, user_id, message):
        """Yangi SMS yuborilganini bazaga qo‘shish"""
        if self.cursor is None:
            print("❌ Cursor mavjud emas.")
            return
        try:
            query = """
                INSERT INTO sms_messages (user_id, message, sent_at)
                VALUES (%s, %s, %s);
            """
            self.cursor.execute(query, (user_id, message, datetime.now()))
            self.connection.commit()
            print("📩 SMS yuborilgan deb qayd etildi!")
        except Exception as e:
            print("⚠️ Xatolik:", e)
    def show_sms(self):
        """Barcha SMS xabarlarni ko‘rish"""
        if self.cursor is None:
            print("❌ Cursor mavjud emas.")
            return
        try:
            self.cursor.execute("""
                SELECT s.id, u.name, s.message, s.sent_at
                FROM sms_messages s
                JOIN users u ON s.user_id = u.id
                ORDER BY s.id;
            """)
            rows = self.cursor.fetchall()
            if not rows:
                print("📭 SMSlar yo‘q.")
            else:
                print("\n📨 SMSlar ro‘yxati:")
                for row in rows:
                    print(f"ID: {row[0]} | Foydalanuvchi: {row[1]} | Xabar: {row[2]} | Sana: {row[3]}")
                print("----------------------------")
        except Exception as e:
            print("⚠️ Xatolik:", e)
    def update_sms(self, sms_id, new_message):
        """SMS xabar matnini tahrirlash"""
        if self.cursor is None:
            print("❌ Cursor mavjud emas.")
            return
        try:
            query = "UPDATE sms_messages SET message = %s WHERE id = %s;"
            self.cursor.execute(query, (new_message, sms_id))
            self.connection.commit()
            if self.cursor.rowcount > 0:
                print("✏️ SMS xabar yangilandi!")
            else:
                print("❌ Bunday SMS ID topilmadi.")
        except Exception as e:
            print("⚠️ Xatolik:", e)
    def delete_sms(self, sms_id):
        """SMS xabarni o‘chirish"""
        if self.cursor is None:
            print("❌ Cursor mavjud emas.")
            return
        try:
            query = "DELETE FROM sms_messages WHERE id = %s;"
            self.cursor.execute(query, (sms_id,))
            self.connection.commit()
            if self.cursor.rowcount > 0:
                print("🗑️ SMS xabar o‘chirildi!")
            else:
                print("❌ Bunday SMS topilmadi.")
        except Exception as e:
            print("⚠️ Xatolik:", e)
    def close_connection(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print("🔒 Ulanish yopildi.")
# === Asosiy boshqaruv menyusi ===
def Manager_users():
    connecter = DB_connecter(
        dbname="n71_baza",
        user="n71_admin",
        password="123",
        host='localhost',
        port=5432
    )
    while True:
        print("\n========= ASOSIY MENYU =========")
        print("1. Foydalanuvchi bo‘limi")
        print("2. SMS bo‘limi")
        print("3. Chiqish")
        print("=================================")
        tanlov = input("Tanlov (1–3): ")
        if tanlov == "1":
            while True:
                print("\n--- FOYDALANUVCHI BO‘LIMI ---")
                print("1. Qo‘shish")
                print("2. Ko‘rish")
                print("3. Yangilash")
                print("4. O‘chirish")
                print("5. Ortga qaytish")
                tanlov_f = input("Tanlov (1–5): ")
                if tanlov_f == "1":
                    name = input("Ism: ")
                    phone = input("Telefon raqami: ")
                    address = input("Manzil: ")
                    age = int(input("Yosh: "))
                    connecter.add_user(name, phone, address, age)
                elif tanlov_f == "2":
                    connecter.show_users()
                elif tanlov_f == "3":
                    user_id = int(input("ID: "))
                    new_name = input("Yangi ism: ")
                    new_phone = input("Yangi telefon: ")
                    new_address = input("Yangi manzil: ")
                    new_age = int(input("Yangi yosh: "))
                    connecter.update_user(user_id, new_name, new_phone, new_address, new_age)
                elif tanlov_f == "4":
                    user_id = int(input("O‘chiriladigan ID: "))
                    connecter.delete_user(user_id)
                elif tanlov_f == "5":
                    break
                else:
                    print("❌ Noto‘g‘ri tanlov.")
        elif tanlov == "2":
            while True:
                print("\n--- SMS BO‘LIMI ---")
                print("1. SMS yuborish (qo‘shish)")
                print("2. SMSlarni ko‘rish")
                print("3. SMSni tahrirlash")
                print("4. SMSni o‘chirish")
                print("5. Ortga qaytish")
                sms_tanlov = input("Tanlov (1–5): ")
                if sms_tanlov == "1":
                    user_id = int(input("Foydalanuvchi ID: "))
                    message = input("Xabar matni: ")
                    connecter.add_sms(user_id, message)
                elif sms_tanlov == "2":
                    connecter.show_sms()
                elif sms_tanlov == "3":
                    sms_id = int(input("SMS ID: "))
                    new_message = input("Yangi xabar matni: ")
                    connecter.update_sms(sms_id, new_message)
                elif sms_tanlov == "4":
                    sms_id = int(input("O‘chiriladigan SMS ID: "))
                    connecter.delete_sms(sms_id)
                elif sms_tanlov == "5":
                    break
                else:
                    print("❌ Noto‘g‘ri tanlov.")
        elif tanlov == "3":
            connecter.close_connection()
            print("👋 Dastur tugatildi.")
            break
        else:
            print("❌ Noto‘g‘ri tanlov.")
if __name__ == "__main__":
    Manager_users()