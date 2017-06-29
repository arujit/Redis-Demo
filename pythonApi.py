import sys,os
from redisApi import RedisApi
import threading

"""
python api wrapper for redis api
"""
            

class TokenAdding(threading.Thread):
    """
    TO_DO -
    ---I am not getting importance of init here... May be I can try implementing without init next
    multiple threads of same user cant add at the same time
    ---locking not working well
    Thread safe ----
    
    """
    def __init__(self,user_name,tokens,lock):
        threading.Thread.__init__(self)
        self.user_name = user_name
        self.tokens = tokens
        self.lock = lock
        self.api = RedisApi(6379, 0)
        #print "Thread initialization"

    #def creat_user(self):
        
    def user_add(self):
        """
        first checking if user already exists 
        -----if exists : add tokens
        -----else add userfist
        """
        print self.user_name +" *"
        isUser = self.api.is_user(self.user_name)
        try:
            if isUser == False:
                print "wrong user"
                raise NameError
        except NameError as e :
            print "Given User Not Found !!!"
            #raise
        else:
            self.api.add_tokens(self.user_name,self.tokens)
            print "token added successfully"
        finally:
            pass
            

    def run(self):
        """
        simple multi-threaded running instance
        I will be naming my threads to the name of users only
        """
        self.counter =False
        for thread in threading.enumerate():
            if thread.name == "MainThread":
                continue
            if thread.name is not self.name:
                if thread.user_name == self.user_name:
                    self.counter = True # A counter to check if it's satisfied
                    try:
                        self.lock.acquire()
                        print "locked !!!"
                        TokenAdding.user_add(self)
                    finally:
                        self.lock.release()
                
        if self.counter == False: #That is no active thread of same name
            TokenAdding.user_add(self)
        


    
class CreateUser(threading.Thread):

    """
    class for creating user in the database and pushing it to the set

    TO_DO--
    --- create exception if a user already exist and 
    --- add threading parameters accordingly later
    """
    def __init__(self,user_name):
        threading.Thread.__init__(self)
        self.user_name = user_name
        self.api = RedisApi(6379,0)

    def user_create(self):
        """
        creating a new user
        --- throw an exception if user is already there
        """
        isUser = self.api.is_user(self.user_name)
        try:
            if isUser:
                raise NameError
        except NameError as e:
            print "NameError Exception : User Already exists"
            #raise
        else:
            self.api.creat_user(self.user_name)
            print "user : %s Created" %self.user_name
        finally:
            pass    
        
    def run(self):
        #print "trying to create a new user "
        CreateUser.user_create(self)


            
class DeleteUser(threading.Thread):
    """
    class to delete a user from the database
    """
    def __init__(self,user_name):
        threading.Thread.__init__(self)
        self.user_name = user_name
        self.api = RedisApi(6379,0)

    def user_delete(self):
        """
        delete an existing user
        """
        isUser = self.api.is_user(self.user_name)
        try:
            if not isUser:
                raise NameError
        except NameError as e:
            print "NameError Exception : User Does not exist"
            #raise
        else:
            self.api.delete_user(self.user_name)
            print "user : %s deleted " %self.user_name
        finally:
            pass    
        
    def run(self):
        #print "trying to create a new user "
        DeleteUser.user_delete(self)


if __name__ == "__main__":
    print "hello to python api"        

        

            
