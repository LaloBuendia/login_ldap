import sys
import ldap
from pymongo import MongoClient
import ldap.modlist
#conexion ldap server
conection = ldap.initialize('ldap://$ip_ldap_server')
conection.simple_bind_s("cn=$example,dc=$exampĺe,dc=$com","$password_ldap")
#conexion mongodb server
client = MongoClient("$ip_mongodb_server",$port)
db = client["ldap"]
collection = db["users"]

#guardado de variables de entrada
username = sys.argv[1]
old_pass = sys.argv[2]
new_pass = sys.argv[3]

#modificación en ldap y mongodb
def mod_users_ldap(username,old_pass,new_pass):
    dn = "uid="+username+",ou=People,dc=$example,dc=$com"
    old_value = {"userPassword":[old_pass]}
    new_value = {"userPassword":[new_pass]}
    modlist = ldap.modlist.modifyModlist(old_value,new_value)
    collection.update_one({"username":username},{"$set":{"password":new_pass}})
    return conection.modify_s(dn,modlist)


print(mod_users_ldap(username,old_pass,new_pass))



