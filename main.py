import bcrypt


#hashed using bcrypt
def generate_hash(psw):
    byte_psw = psw.encode('utf-8')
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(byte_psw, salt)
    return hash.decode('utf-8')

#validating hash vs psw
def is_valid_hash(psw, hash):
    hash_ =hash.encode('utf-8')
    byte_psw = psw.encode('utf-8')
    is_valid = bcrypt.checkpw(byte_psw, hash_)
    return is_valid  


#user registration
def register_user():
    name = input('Enter your name: > ')
    password = input('Enter your password: > ')
    hashed_password = generate_hash(password)
    with open('users.txt', 'a') as f:
        f.write(f'{name},{hashed_password}\n')
    print('User  successfully registered!')

#user login
def log_in_user():
    name = input('Enter your name: > ')
    password = input('Enter your password: > ')
    with open('users.txt', 'r') as f:
        users = f.readlines()
    for user in users:
        user_name, user_hash = user.strip().split(',')
        if name == user_name and is_valid_hash(password, user_hash):
            return True
    return False

def main():
    while True:
        print('Welcome to the System!')
        print('Choose from the following option:')
        print('1. To Register')
        print('2. To Log in')
        print('3. To Exit')

        choice = input(' > ')

        if choice == '1':
            register_user()
        elif choice == '2':
            if log_in_user():
                print('Login successful!')
            else:
                print('Incorrect log in. Try again.')
        elif choice == '3':
            print('Goodbye!')
            break

if __name__ == '__main__':
    main()