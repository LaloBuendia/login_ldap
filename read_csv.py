#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv
import string
import random
import ldap
import ldap.modlist
from mail import send_email
from pymongo import MongoClient
import base64

#inicializando el contador para el uid del ldap
i = 0

#creando conexion del ldapserver
conection = ldap.initialize('ldap://$ip_ldap_server')
conection.simple_bind_s("cn=$example,dc=$example,dc=$com","$password_dummy")

#funcion para la creacion de la base en mongodb
def createBase(data):
    client = MongoClient("$ip_mongodb",$port)
    db = client["ldap"]
    collection = db["users"]
    collection.insert(data)
    return

#funcion para ldapsearch del usuario
def get_users_ldap(username):
    ldap_base = "dc=$example,dc=$com"
    query = "(uid="+username+")"
    return conection.search_s(ldap_base,ldap.SCOPE_SUBTREE,query)

#funcion ldapadd
def add_ldap_user(username,mail,name,lastname,password,uid_number):
    dn = "uid=" + username + ",ou=People,dc=$example,dc=$com"
    print(dn)
    modlist = {
           "objectClass": ["inetOrgPerson", "posixAccount", "shadowAccount"],
           "uid": [username],
           "sn": [name],
           "givenName": [name],
           "cn": [name + " " +lastname],
           "displayName": [name + " " +lastname],
           "uidNumber": [uid_number],
           "gidNumber": [uid_number],
           "loginShell": ["/bin/bash"],
           "mail": [mail],
           "UserPassword": [password],
           "homeDirectory": ["/home/" + name],
           "shadowLastChange": "0"
            }
    return conection.add_s(dn,ldap.modlist.addModlist(modlist))

#funcion para el borrado de usarios ldapdelete
def delete_user_ldap(username):
    dn = "uid=" + username + ",ou=People,dc=$example,dc=$com"
    conection.delete_s(dn)


#generador de password random
def id_generator(size=8, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

#lectura del archivo csv
results = []
with open('example1.csv') as File:
    reader = csv.DictReader(File)
    for row in reader:
        results.append(row)
#parseo de datos, creacion ldap db, mongodb y envio de email
data = []
for vari in results:
    i = i + 1
    username = vari["correo"].split("@")
    mail = vari["correo"]
    name = vari["Nombre"]
    lastname = vari["Apellido"]
    password = id_generator()
    print("username = " + username[0] + " password = " + password)
    add_ldap_user(username[0],mail,name,lastname,password,str(i))
    data.append({
                            "username": username[0],
                            "mail": mail,
                            "password": password.encode('base64','strict')
                        })
    send_email(mail,"Hola"+" "+name+"\nTe mando datos de tu cuenta\nusername:"+username[0]+"\npassword:"+password+"\nsaludos!")
try:
   print(" ")
   print(createBase(data))
except:
   print("there is not data!")
