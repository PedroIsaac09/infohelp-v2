import sqlite3
conn = sqlite3.connect('db.sqlite3')
c = conn.cursor()
print('auth_user rows:')
for row in c.execute('SELECT id, username FROM auth_user ORDER BY id'):
    print(row)
print('\ninfohelp_curso table info:')
for row in c.execute("PRAGMA table_info('infohelp_curso')"):
    print(row)
print('\nSample cursos rows:')
for row in c.execute('SELECT * FROM infohelp_curso LIMIT 10'):
    print(row)
print('\nAulas with usuario_id=0:')
print('\ninfohelp_aula table info:')
for row in c.execute("PRAGMA table_info('infohelp_aula')"):
    print(row)
print('\nSample aulas rows:')
for row in c.execute('SELECT * FROM infohelp_aula LIMIT 10'):
    print(row)
print('\nBiblioteca rows with usuario_id=0:')
print('\ninfohelp_biblioteca table info:')
for row in c.execute("PRAGMA table_info('infohelp_biblioteca')"):
    print(row)
print('\nSample biblioteca rows:')
for row in c.execute('SELECT * FROM infohelp_biblioteca LIMIT 10'):
    print(row)
conn.close()
