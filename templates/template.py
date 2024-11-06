import os, sys

sys.path.append(os.path.abspath(os.curdir))

from model.password import Password
from views.views import Hasher
action = input('Digite 1 para salvar uma senha e 2 para ver uma senha salva: ')

if action == '1':
    if len(Password.get()) == 0:
        key, path = Hasher.create_key(archive=True)
        print('Sua chave foi criada')
        print(f'Chave {key.decode("utf-8")}')
        if path:
            print('Chave salva no arquivo')
            print(f'Caminho: {path}')
    else:
        key = input('Digite a sua chave: ')

    domain = input('Dominio: ')
    password = input('Senha: ')
    fernet_user = Hasher(key)
    p1 = Password(domain=domain, password=fernet_user.encrypt(password).decode('utf-8'))
    p1.save()

elif action == '2':
    domain = input('Dominio: ')
    key = input('Chave: ')
    fernet_user = Hasher(key)
    data = Password.get()

    for i in data:
        if domain in i['domain']:
            password = fernet_user.decrypt(i['password'])
    if password:
        print(f'Senha: {password}')
    else:
        print('Nenhuma senha salva nesse dominio')