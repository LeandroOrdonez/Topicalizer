#!/usr/bin/python

# jsonify.py: Generates a JSON file from the per-document topic 
# distribution fitted by onlineldavb.py
#
# Copyright (C) 2013 Leandro Ordonez
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import numpy as np
import sys, nltk, re
import MySQLdb as mysql
#from xml.sax.saxutils import escape

"""
Generates a JSON file from the per-document topic distribution fitted by 
onlineldavb.py
"""

def run():
    if(len(sys.argv) > 1):
	csv_path = sys.argv[1]
        json_path = sys.argv[1][:(sys.argv[1].index('.csv'))] + '.json'
    else:
        csv_path = '../../outcome/per-document-topics.csv'
        json_path = '../../outcome/per-document-topics.json'
    pdc = np.loadtxt(csv_path, dtype={'names': \
('Operation ID', 'Operation Name', 'Topic', 'Topic Probability', 'Terms', 'Service URI'),\
'formats': ('i4', 'S100', 'i4', 'f4', 'S400', 'S400')}, delimiter=',', skiprows=1)
    pcd = sorted(pdc, key = lambda x: (x[2], (1-x[3]))) # sorting by topic and topic probability
# print pdt[0:5]
# print ptd[0:5]

    doc_categories = dict()
    for doc in pdc:
        if int(doc[3]*1000) > 150:
            key = (doc[0], doc[1], doc[5])
#    print key
            if (not key in doc_categories):
                doc_categories[key] = [('Category-'+`doc[2]`, int(doc[3]*1000))]
            else:
                doc_categories[key].append(('Category-'+`doc[2]`, int(doc[3]*1000)))
#print doc_topics

    category_docs = dict()
    for category in pcd:
        if int(category[3]*1000) > 150:
            key = 'Category-'+`category[2]`
            if (not key in category_docs):
                category_docs[key] = [(category[0], category[1], category[5])]
            else:
                if (len(category_docs[key]) <= 30):
                    category_docs[key].append((category[0], category[1], category[5]))
#print topic_docs

    json_output = '' + \
"""{
    "name": "categories",
    "children": [
    %s
    ]
   }""" % jsonify_categories(category_docs, doc_categories)
    
    #print json_output
    #np.savetxt('../../outcome/per-document-topics.json', json_output)
    pdc_json_file = open(json_path, 'w')
    pdc_json_file.write(json_output)
    pdc_json_file.close()

def jsonify_categories(category_docs, doc_categories):
    #print 'entro a jsonify_categories'
    result = ''
    for category in category_docs:
        result += \
'{\n    "name": "' + category + \
'", \n    "id": "' + category + \
'", \n    "children": [\n %s\n]\n},' % jsonify_documents(category, category_docs[category], doc_categories)
    #print result[:-1]
    return result[:-1]

def jsonify_documents(category, docs, doc_categories):
    #print 'entro a jsonify_documents'
    # Connecting to MySQL database:
    db = mysql.connect(host='localhost', user='root', passwd='', db='service_registry', unix_socket='/opt/lampp/var/mysql/mysql.sock')
    cursor = db.cursor()
    result = ''
    for doc in docs:
        #Querying the database for retrieving the operation name and service uri
        query = 'SELECT SOAP_OPERATION.OPERATIONDOCUMENTATION FROM SOAP_OPERATION WHERE SOAP_OPERATION.ID=%s' % `(doc[0])`
        id_op = cursor.execute(query)
        db_results = cursor.fetchall()
        op_doc = nltk.clean_html(db_results[0][0])
        op_doc = re.sub('"', "'", re.sub("\t|\n", " ", op_doc))
        result += \
'{\n    "name": "' + doc[1] + \
'", \n  "id": "Operation-' + category[(category.index('-')+1):] + '.' + `doc[0]` + \
'", \n  "service_uri": "' + doc[2] + \
'", \n  "operation_doc": "' + op_doc + \
'", \n    "children": [\n %s\n]\n},' % jsonify_cat_per_doc(doc_categories[doc])
    #print result[:-1]
    return result[:-1]

def jsonify_cat_per_doc(categories):
    #print 'entro a jsonify_cat_per_doc'
    result = ''
    for category in categories:
        result += \
'{"name": "' + category[0] + '", "size": ' + `category[1]` + '},'
    #print result[:-1]    
    return result[:-1]

if __name__ == '__main__':
    run()
