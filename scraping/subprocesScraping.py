import os
import subprocess

os.environ['EMAIL'] = "email@gmail.com"
os.environ['PASSWORD'] = "senha"
os.environ['SEARCH'] = "Brasilia"
os.environ['FILE_NAME'] = "teste22.txt"
 
def main():
    command = f"scrapy runspider scraping.py -a value_search={os.environ['SEARCH'] } -a email={os.environ['EMAIL']} -a password={os.environ['PASSWORD']} -a output_file={os.environ['FILE_NAME']}" 
    subprocess.Popen(args=command, 
                     shell=True,
                     stdin=subprocess.PIPE,
                     stdout=subprocess.PIPE)
    print("End")
    
if __name__ == "__main__":
    main()