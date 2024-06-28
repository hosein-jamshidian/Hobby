from collections import Counter
import string
import pandas as pd 
import numpy as np
import functools
import hashlib

class Site:
    def __init__(self, url_address):
        self.url= url_address
        self.register_users= []
        self.active_users= []
        
        
    def show_users(self):
        users= [user.__dict__ for user in self.register_users]
        users_df= pd.DataFrame(users)
        return users_df
    
    def register(self, user):
        if len(self.register_users) == 0 :
            self.register_users.append(user)
            return "register successful"
        else:
            for reg in self.register_users:
                permission= [1 for attr in user.__dict__ if user.__dict__.get(attr) == reg.__dict__.get(attr)]
                if sum(permission) == len(user.__dict__):
                    raise ValueError("user already registered")
                else:
                    self.register_users.append(user)
                    return "register successful"
                
    def login(self, **kwargs):
        temp ={"username": kwargs.get("username"),
               "password": kwargs.get("password"),
               "email": kwargs.get("email")}
        
        if all([temp[k] is not None for k in temp]):
            for user in self.register_users:
                if (user.username == temp['username']) & (user.email == temp['email']):
                    if (user.set_new_password(temp['password']) == user.password):
                        if user not in self.active_users:
                            self.active_users.append(user)
                            return "login successful"
                        else: 
                            return "user already logged in"
                    return "invalid login"
                return "invalid login"
        if all([temp[k] is not None for k in temp if k not in ['email']]):
            for user in self.register_users:
                if (user.username == temp['username']):
                    if (user.set_new_password(temp['password']) == user.password):
                        if user not in self.active_users:
                            self.active_users.append(user)
                            return "login successful"
                        else: 
                            return "user already logged in"
                    return "invalid login"
                return "invalid login"
        if all([temp[k] is not None for k in temp if k not in ['username']]):
            for user in self.register_users:
                if (user.email == temp['email']):
                    if (user.set_new_password(temp['password']) == user.password):
                        if user not in self.active_users:
                            self.active_users.append(user)
                            return "login successful"
                        else: 
                            return "user already logged in"
                    return "invalid login"
                return "invalid login"
        else:
            return "invalid login"
                    

    def logout(self, user):
        if len(self.active_users) == 0:
            return "user is not logged in"
        else:
            for active in self.active_users:
                permission= [1 for attr in user.__dict__ if user.__dict__.get(attr) == active.__dict__.get(attr)]
                if sum(permission) == len(user.__dict__):
                    self.active_users.remove(active)
                    return "logout successful"
                else:
                    return "user is not logged in"
            

    def __repr__(self):
        return "Site url:%s\nregister_users:%s\nactive_users:%s" % (self.url, self.register_users, self.active_users)

    def __str__(self):
        return self.url


class Account:
    def __init__(self, username, password, user_id, phone, email):
        self.username= self.username_validation(username)
        self.password= self.password_validation(password)
        self.user_id= self.id_validation(user_id)
        self.phone= self.phone_validation(phone)
        self.email= self.email_validation(email)

    def set_new_password(self, password):
        new_password= self.password_validation(password)
        return new_password 

    def username_validation(self, username):
        if not isinstance(username, str):
            raise ValueError("invalid username")
        if Counter(list(username))['_'] != 1:
            raise ValueError("invalid username")
        pure_username= username.replace("_","")
        if len(np.setdiff1d(list(pure_username), list(string.ascii_letters))) != 0:
            raise ValueError("invalid username")
        return username

    
    def password_validation(self, password):
        if not isinstance(password, str):
            raise ValueError("invalid password")
        if len(password) < 8 :
            raise ValueError("invalid password")
        if len(np.setdiff1d(list(password), list(string.ascii_lowercase))) == 0:
            raise ValueError("invalid password")
        if len(np.setdiff1d(list(password), list(string.ascii_uppercase))) == 0:
            raise ValueError("invalid password")
        if len(np.setdiff1d(list(password), list(string.digits))) == 0:
            raise ValueError("invalid password")
        hash_password= password.encode("utf8")
        encrypted_password= hashlib.sha256(hash_password).hexdigest()
        return encrypted_password
    
        
    def id_validation(self, id_):
        if not isinstance(id_, str):
            raise ValueError("invalid code melli")
        if len(id_) != 10 :
            raise ValueError("invalid code melli")
        id_digits= list(map(int, str(id_)))
        index= list(range(10,1,-1))
        result= (np.dot(id_digits[:-1], index)) % 11
        if result < 2:
            control_digit= result
        else:
            control_digit= (11 - result)
        if id_digits[-1] != control_digit:
            raise ValueError("invalid code melli")
        return id_
        
    
    def phone_validation(self, phone):
        if not isinstance(phone, str):
            raise ValueError("invalid phone number")
        if len(phone) < 11 : 
            raise ValueError("invalid phone number")
        if not(phone.startswith("+989")) and not(phone.startswith("09")):
            raise ValueError("invalid phone number")
        return phone

    def email_validation(self, email):
        if not isinstance(email, str):
            raise ValueError("invalid email") 
        first_part= email.split("@")[0]
        second_part= email.split("@")[1]
        third_part= second_part.split(".")[1]
        second_part= second_part.split(".")[0]
        allowed_letters= list(string.ascii_letters)
        first_second_permission= allowed_letters + ["_","-","."]
        third_permission= allowed_letters
        if len(np.setdiff1d(list(first_part), first_second_permission)) != 0:
            raise ValueError("invalid email")
        if len(np.setdiff1d(list(second_part), first_second_permission)) != 0:
            raise ValueError("invalid email")
        if (len(third_part) > 5) or (len(third_part) < 2) : 
            raise ValueError("invalid email")
        if len(np.setdiff1d(list(third_part), third_permission)) != 0:
            raise ValueError("invalid email")
        return email


    def __repr__(self):
        return self.username

    def __str__(self):
        return self.username


def show_welcome(func):
    @functools.wraps(func)
    def wrapper(user):
        username= user.username.replace("_", " ").title()
        if len(username) > 15:
            username= username[:15]
            username+="..."
        user.username= username
        result= func(user)
        return result
    return wrapper
        
            
def verify_change_password(func):
    @functools.wraps(func)
    def wrapper(user, old_pass, new_pass):
        encrypted_previous_pass= user.password
        hash_password= old_pass.encode("utf8")
        encrypted_old_pass= hashlib.sha256(hash_password).hexdigest()
        if encrypted_previous_pass == encrypted_old_pass:
            user.password= user.set_new_password(new_pass)
            result= func(user, old_pass, new_pass)
        else: 
            result= "incorrect old password"
        return result
    return wrapper


@show_welcome
def welcome(user):
    return ("welcome to our site %s" % user)

@verify_change_password
def change_password(user, old_pass, new_pass):
    return ("your password is changed successfully.")
