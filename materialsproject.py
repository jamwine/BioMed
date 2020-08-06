import pandas as pd
import json
import requests
import time
import datetime
from pymatgen import MPRester
from pymatgen.electronic_structure.plotter import DosPlotter, BSPlotter

def to_dict(obj):
    return json.dumps(obj, default=lambda o: o.__dict__)

API_KEY='XXXXXXXXXXXX'
USER_AGENT='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
df_2d=pd.read_csv('C:/Users/Subrat.Subedi/Downloads/2D.csv')
for index, row in df_2d.iterrows():
    baseurl = 'https://www.materialsproject.org/rest/v2/materials/%s'%(row['mpid'])
    output = {}
    try:
        response = requests.get(baseurl+'/doc',headers={'x-api-key':API_KEY,'User-Agent':USER_AGENT}).json()
        mp_json = response['response']
    except KeyError:
        m = MPRester(API_KEY)
        data = m.get_data(row['mpid'])
        mp_json = to_dict(data)
    try:
        output['name']=mp_json["exp"]["tags"][0]
    except:
        try:
            output['name']=mp_json["pretty_formula"]
        except:
            continue
    with open('C:/Users/Subrat.Subedi/Downloads/Data Collections/rex_stanford_xls/'+row['mpid']+'.json','w',encoding='utf-8') as rex:
        json.dump(mp_json,rex)
    output['authors']=["Materials Project"]
    output['description']=mp_json["pretty_formula"]
    output['resource_type']="Materials"
    output['source_repository']=['https://materialsproject.org']
    try:
        isodate = datetime.datetime.strptime(mp_json['created_at'],'%Y-%m-%d %H:%M:%S')
        output['version']=isodate.isoformat()
    except KeyError:
        output['version']=datetime.datetime.now().isoformat()
    output['link_to_source']=['https://materialsproject.org/materials/'+row['mpid']]
    output['direct_download_link']=['https://materialsproject.org/materials/'+row['mpid']]
    output['tags']=mp_json['exp']['tags']
    output['tags'].append('Materials Project')
    output['tags'].append('2D Materials')
    output['tags'].append('Stanford Collection')
    reduced_json = {key:values for key, values in mp_json.items() if key not in ['snl','snl_final']} 
    output['bulk']=reduced_json
    output['bulk']['formats']={'bibtex':{}}
    try:
        bibtex_format=mp_json['doi_bibtex'].replace("\n", "")
    except:
        time.sleep(1)
        bibtex_format=requests.get('https://materialsproject.org/materials/%s/bibtex'%(row['mpid']),headers={'x-api-key':API_KEY,'User-Agent':USER_AGENT}).content()
    output['bulk']['formats']['bibtex']=bibtex_format
    output['bulk']['Band_Gap']=row['Band_Gap']
    output['bulk']['Bulk_Point']=row['Bulk_Point']
    # output['bulk']['Mono_Point']=row['Mono_Point']
    with open('C:/Users/Subrat.Subedi/Downloads/Data Collections/remap_stanford_xls/'+row['mpid']+'.json','w',encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=4)
    time.sleep(1)