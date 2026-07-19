
"""
hashing.py - Secure password hashing using bcrypt
Provide functions to hash passwords and validate them.
"""
import bcrypt

#hashed using bcrypt
def generate_hash(psw):
    """
    Generate a secure bcrypt hash from a plain text password
    A random salt is generated each time so identical passwords produce different hashes 
    to prevents rainbow attacks
    
    Parameters:
    psw:plain text password to hash
    
    Returns:
    str: hashed password as a string or None if hashing fails"""
    try:
        byte_psw = psw.encode('utf-8')#convert string to bytes since bcrypt needs bytes
        salt = bcrypt.gensalt()#generate an unique salt
        hashed = bcrypt.hashpw(byte_psw, salt)#hash the password with salt
        return hashed.decode('utf-8')#decode the bytes back to string for storage
    except Exception as e:
        print(f"Error generating hash: {e}")

#validating hash vs psw
def is_valid_hash(psw, hashed):
    """
    Check if a text password matches a stored bcrypt hash

    Parameters:
    psw: plain text password entered by the user.
    hashed: stored hashed password

    Returns:
    True if the password matches, False if not
    """
    try:
        hashed =hashed.encode('utf-8')#convert stored hash to bytes
        byte_psw = psw.encode('utf-8')#convert entered password to bytes
        is_valid = bcrypt.checkpw(byte_psw, hashed)# timing-safe comparison
        return is_valid  
    except Exception as e:#catch any unexpected errors
        print(f"Error validating hash:{e}")
        return False#return false so login fails safely instead of crashing