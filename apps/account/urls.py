from django.urls import path


'''
    Register:
        - /register/ -> send code to user via mail
        - /verify/email/ -> verify code -> activate, give token
    
    Login:
        - /login/ -> give token 
        
    Verify Account:
        - /send/email/ -> send code to user via mail
        - /verify/email/ -> verify code -> activate, give token
        
    Change Password:
        - /change/password/ -> change password
    
    Reset Password:
            - /register/ -> send code to user via mail
            - /verify/email/ -> verify code -> activate, give token
        - /reset/password/ -> reset password
'''