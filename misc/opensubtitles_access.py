import glob
import os
import struct
import sys
import tkinter
import urllib.request
from tkinter.filedialog import askopenfilenames, askdirectory
from xmlrpc.client import ServerProxy, Error
from zipfile import ZipFile

class SubClient():     
    USER_AGENT = 'OS Test User Agent'
    LANGUAGE = 'en'
    SUB_LANGUAGE = 'eng'
    
    username = ''
    password = ''
    
    server = None
    token = None

    def __enter__(self):
        self.server = ServerProxy('http://api.opensubtitles.org/xml-rpc')
        print('Logging in...')
        response = self.server.LogIn(self.username, self.password, self.LANGUAGE, self.USER_AGENT)        
        print(response)
        self.token = response['token']
        return self

    def __exit__(self, type, value, traceback):
        print('Logging out... Token: ' + self.token)
        response = self.server.LogOut(self.token)        
        print(response)

    # najpierw szukanie z hashem, pierwszy wedlug SubRating
    # potem normalne query, szukamy dokladnego MovieReleaseName, pierwsze po ocenie
    # potem po prostu pierwsze po ocenie
    # o co chodzi z tagami? lepiej niby po nich szukac niz po query
    # moze jakos z imdb wyczajac co to za film i po tym szukac?
    # jesli plik z napisami nie zawiera nazwy filmu, to ja dodac
    def get_subtitles(self, movie_file_path):
        '''Returns a list of found subtitles.'''
        def download_sub(sub_name, sub_zip_address, out_path):
            '''Downloads zip, extracts file, removes zip'''
            zip_path = os.path.join(out_path, 'blabletemp.zip')
            urllib.request.urlretrieve(sub_zip_address, zip_path)
            zip = ZipFile(zip_path)
            zip.extract(sub_name, out_path)
            zip.close()
            os.remove(zip_path)

        output_path = os.path.dirname(movie_file_path)
        
        movie_hash = self.hashFile(movie_file_path)
        movie_size = filesize = os.path.getsize(movie_file_path)
        movie_name = os.path.basename(movie_file_path)
        
        search_opts = {'sublanguageid': self.SUB_LANGUAGE, 'moviehash': movie_hash, 'moviebytesize': movie_size}
        response = self.server.SearchSubtitles(self.token, [search_opts])
        subs = response['data']
        if subs:
            print('Mamy dobrze dobrane: ' + subs[0]['SubFileName'])
            download_sub(subs[0]['SubFileName'], subs[0]['ZipDownloadLink'],output_path)
            return
            
        search_opts = {'sublanguageid': self.SUB_LANGUAGE, 'query': movie_name}
        response = self.server.SearchSubtitles(self.token, [search_opts])
        subs = response['data']
        best_subs = [sub for sub in subs if sub['MovieReleaseName'] == movie_name]
        if best_subs:
            print('Mamy tez dobrze dobrane: ' + subs[0]['SubFileName'])
            download_sub(best_subs[0]['SubFileName'], best_subs[0]['ZipDownloadLink'], output_path)
            return
        if subs:
            print('Mamy jako tako dobrane: ' + subs[0]['SubFileName'])
            download_sub(subs[0]['SubFileName'], subs[0]['ZipDownloadLink'], output_path)
            return

        print('Gowno mamy')

    # http://trac.opensubtitles.org/projects/opensubtitles/wiki/HashSourceCodes
    # had to change division for Python 3
    def hashFile(self, name): 
        try:                 
            longlongformat = 'q'  # long long 
            bytesize = struct.calcsize(longlongformat) 
                
            f = open(name, "rb") 
                
            filesize = os.path.getsize(name) 
            hash = filesize 
                
            if filesize < 65536 * 2: 
                return "SizeError" 
             
            for x in range(65536//bytesize): 
                buffer = f.read(bytesize) 
                (l_value,)= struct.unpack(longlongformat, buffer)  
                hash += l_value 
                hash = hash & 0xFFFFFFFFFFFFFFFF #to remain as 64bit number                

            f.seek(max(0,filesize-65536),0) 
            for x in range(65536//bytesize): 
                buffer = f.read(bytesize) 
                (l_value,)= struct.unpack(longlongformat, buffer)  
                hash += l_value 
                hash = hash & 0xFFFFFFFFFFFFFFFF 
             
            f.close() 
            returnedhash =  "%016x" % hash 
            return returnedhash 
        
        except(IOError): 
            return "IOError"	
			
def main():
    if len(sys.argv) >= 2:        
        with SubClient() as client:
            file_path = os.path.abspath(sys.argv[1])
            client.get_subtitles(file_path)
    else:
        print('Nie podano nazwy pliku, to wybieramy caly folder. Do kazdego .avi z tego folderu beda pobrane napisy.')
        root = tkinter.Tk()
        root.withdraw()
        dir_path = askdirectory()
        root.destroy()
        print(dir_path + '/*.avi')
        
        with SubClient() as client:
            # przerobic na os walka z kilkoma rozszerzeniami avi, mpg, mkv, mp4
            # najpierw dialog czy pliki, czy folder, jak sie wybierze folder, to pyta, czy rekurencyjnie
            for file in glob.glob(dir_path + '/*.avi'):
                client.get_subtitles(os.path.abspath(file))
            for file in glob.glob(dir_path + '/*.mkv'):
                client.get_subtitles(os.path.abspath(file))
            for file in glob.glob(dir_path + '/*.mpg'):
                client.get_subtitles(os.path.abspath(file))
            for file in glob.glob(dir_path + '/*.mp4'):
                client.get_subtitles(os.path.abspath(file))
            

if __name__ == '__main__':
    main()
