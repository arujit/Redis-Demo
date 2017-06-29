import sys,os
import redis
import json

"""
author - james.bondu
TO_DO - Implementing a simple raedis api that is capable of adding, deleting and modify in a hashmap
- I am thinking of a list of hashes
- First try to implement a hash operations
- calling through api
"""



#class  

"""
pool = redis.ConnectionPool(host = 'localhost',port = 6379,db = 0)
r = redis.Redis(connection_pool  = pool)
print redis,r
"""
class RedisApi(object):
    def __init__(self,port,db_no):
        self.host = 'localhost'
        self.port = port
        #print "hello RedisApi"
        self.db = db_no
        self.pool = redis.ConnectionPool(host = self.host,port = self.port,db = self.db )
        self.r = redis.Redis(connection_pool = self.pool)
        

    def creat_user(self,name):
        """
        adding user tokens
        
        options  - either to use a hash-map but then we have to implement a separate redis list of hashmap (hierarchial hashmap) to keep track of user or keep everything in a json and append it
        --- for simplification I am now using hashmap now 
        --- for simplyfication I am maintaining a set of users separately
        """
        self.key = name
        #self.username = name
        self.r.hset(self.key,'created',True)
        #self.r.lpush('user',self.key)
        self.r.sadd('user',self.key)
        return True

    def add_tokens(user,name,tokens):
        """
        token object is a python dictionary containing information about the user
        """
        user.key = user.name
        user.tokens = tokens
        user.r.hmset(user.key,user.tokens)
        print "tokens added of %s" %user.key
        return True

    def is_user(user,name):
        """
        checks if certain name is the user or not
        """
        user.name = name
        #print user.name
        isUser = user.r.sismember('user',user.name)
        return isUser

    def get_query(self,name,field):
        self.name = name
        self.field = field
        return self.r.hget(self.name,self.field)

    def remove_fields(self,name,fields):
        self.name = name
        self.fields = fields
        return self.r.hdel(self.name, *self.fields)

    def delete_user(self,name):
        self.name = name
        self.r.srem("user", self.name)
        return self.r.delete(self.name)

    def findall_users(self):
        self.all_users =  self.r.smembers("user")
        print self.all_users
        
if __name__ == "__main__":
    print "hello api"
