import sys
from django.core.management.base import BaseCommand, CommandError
import re
import json
import urllib.request
import os



cwd=os.getcwd()
loc=os.path.join(cwd,"Downloads")
if not os.path.exists(loc):
    os.makedirs(loc)


class Command(BaseCommand):
    help="Command to scrap"
    missing_args_message = "You must provide filingDatetimeFrom and filingDatetimeTo."

    def add_arguments(self,parser):
        parser.add_argument('filingDatetimeFrom', nargs='+', type=str)
        parser.add_argument('filingDatetimeTo', nargs='+',type=str)

    def handle(self,*args, **options):
        if len(sys.argv)>4:
            raise CommandError('unexpected argument')
        else:
            if not re.match(r'\d{4}-\d{2}-\d{2}',sys.argv[2]) or not re.match(r'\d{4}-\d{2}-\d{2}',sys.argv[3]):
                raise CommandError("dates must be in yyyy-mm-dd format")
            else:
                url='https://ptabdata.uspto.gov/ptab-api/documents/?filingDatetimeFrom='+sys.argv[2]+'&filingDatetimeTo='+sys.argv[3]
                print ("processing")
                req = urllib.request.Request(url)
                data = urllib.request.urlopen(req).read()
                # print (str(data))
                try:
                    js = json.loads(data.decode('utf-8'))
                except: 
                    js = None
                # print(len(js["results"]))
                if js!=None:
                    for i in range(len(js["results"])):
                        link=js["results"][i]["links"][1]["href"]
                        attachment_name=js["results"][i]["trialNumber"]+'-'+js["results"][i]["documentNumber"]+'.pdf'
                        path=os.path.join(loc,attachment_name)
                        urllib.request.urlretrieve(link,path)
                    print ("done")
                else:
                    print("didn't got any data")
                    

