    
import os

class whichsystem(object):
    
    """docstring for whichsystem"""

    def __init__(self):        
        self.filesep = None
        self.osname = None        
        
    def run(self):
        print(os.name)
        self.osname = os.name
        if os.name == "nt": #Windows 
            self.filesep = '\\'
            print (os.name, self.filesep)
        elif os.name == "posix": #Mac and Linux
            self.filesep = '/'
            print (os.name, self.filesep)
        else:
            Exception("Which system are you using?")

if __name__ == '__main__':
    mysys = whichsystem()
    mysys.run()