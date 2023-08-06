def encrypt_the_file_txt(file,password):
    import os
    import pyAesCrypt
    print("---------------------------------------------------------------")
    bufferSize = 64*1024
    try: 
        pyAesCrypt.decryptFile(str(file), str(os.path.splitext(file)[0]), password, bufferSize)
        os.remove(file)
    except FileNotFoundError: 
        print("[x] File not found!")
    except ValueError: 
        print("[x] Password is Fasle!")
    else: 
        print("[+] File '"+str(os.path.splitext(file)[0])+"' successfully saved!")
    finally: 
        print("---------------------------------------------------------------")
def ZAR_encrypt_the_file_txt(file,password):
    import os
    import pyAesCrypt
    print("---------------------------------------------------------------" )
    bufferSize = 64*1024
    try: 
        pyAesCrypt.encryptFile(str(file), str(file)+".crp", password, bufferSize)
        os.remove(file)
    except FileNotFoundError: 
        print("[x] File not found!")
    except OSError:
        print('[x] File not found!')
    else: 
        print("[+] File '"+str(file)+".crp' successfully saved!")
    finally: 
        print("---------------------------------------------------------------")

def to_rasshifrovat_secret(cd_in_the_file,file,secret):
    import pickle
    import os
    os.chdir(cd_in_the_file)
    f = open(file+'.bin', 'wb')
    pickle.dump(login, f)
    f.close()
def encrypt_secret(cd_in_the_file,file,secret):
    import os
    os.chdir(cd_in_the_file)
    import pickle
    f = open(file+'.bin', 'rb')
    L2 = pickle.load(f)
    print(L2)
def kdkdkd(file,text):
    from gtts import gTTS
    tts = gTTS(text)
    tts.save(file+'mp3')