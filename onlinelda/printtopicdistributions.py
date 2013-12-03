#!/usr/bin/python

# printtopicdistributions.py: Prints the per-document topic distributions (based on
# the 'printtopics.py' script by Matthew D. Hoffman)
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

import sys, os, re, random, math, urllib2, time, cPickle
import numpy
import MySQLdb as mysql

import rdf_sesame.model_instantiation as rdfmi
import rdf_sesame.sesamehandler as sesame

def main():
    """
    Displays the per-document topic distribution fitted by onlineldavb.py. The first column gives the
    (expected) most prominent topics in the document, the second column
    gives their (expected) relative prominence.
    """
    #vocab = str.split(file(sys.argv[1]).read())
    gamma = numpy.loadtxt(sys.argv[1])
    if(len(sys.argv) > 2):
        topics_per_document = int(sys.argv[2])
	if(topics_per_document > len(gamma[0])):
            print 'Warning: the maximum number of topics allowed is', len(gamma[0])
            topics_per_document = len(gamma[0])
    else:
        topics_per_document = 10

    topics_file = open('../outcome/per-document-topics.txt', 'w')
    topics_csv = open('../outcome/per-document-topics.csv', 'w')
    topics_csv.write('Operation ID,Operation Name,Topic,Topic Probability,Terms\n')
    words_per_topic = file('../outcome/words_per_topic.txt').readlines()
    # Creating a Sesame repository handler (with default values).
    repo = sesame.SesameHandler()
    # Connecting to MySQL database:
    db = mysql.connect(host='localhost', user='root', passwd='', db='service_registry', unix_socket='/opt/lampp/var/mysql/mysql.sock')
    cursor = db.cursor()
    for d in range(0, len(gamma)):
        thetad = list(gamma[d, :])
        thetad = thetad / sum(thetad)
        temp = zip(thetad, range(0, len(thetad)))
        temp = sorted(temp, key = lambda x: x[0], reverse=True)
        #print 'Operation (Id) %d:' % (d+1)
        sys.stdout.write('\rResolving Per-document topic distributions... (%d/%d)' % ((d+1), len(gamma)))
        sys.stdout.flush()
	topics_file.write('Operation (Id) %d: \n' % (d+1))
        # Storing the documents (operations) and the categories they belong to as RDF statements.
        membership_relations = list()
        rdf_data = ''
        #Querying the database for retrieving the operation name and service uri
        query = 'SELECT SOAP_OPERATION.OPERATIONNAME, SOAP_OPERATION.SOAPSERVICE_SERVICEURI FROM SOAP_OPERATION WHERE SOAP_OPERATION.ID=%s' % `(d+1)`
        id_op = cursor.execute(query)
        results = cursor.fetchall()
        for i in range(0, topics_per_document):
            #print '\t Topic %s  \t---\t  %.4f' % (temp[i][1], temp[i][0])
	    topics_file.write('\t Topic %s  \t---\t  %.4f \n' % (temp[i][1], temp[i][0]))
            topics_csv.write('%s,%s,%s,%.4f,%s\n' % (`(d+1)`, results[0][0], temp[i][1], temp[i][0], words_per_topic[temp[i][1]].rstrip()))
            membership_relation = rdfmi.new_membership_relation(`(d+1)` + ';' + `temp[i][1]`, temp[i][0], `temp[i][1]`)
            membership_relations.append(`(d+1)` + ';' + `temp[i][1]`)
            rdf_data = rdf_data + membership_relation
        operation = rdfmi.new_operation(`(d+1)`, results[0][0], results[0][1], membership_relations)
        rdf_data = rdf_data + operation
        repo.post_statements(rdf_data)
        #print
	topics_file.write('\n')
    print '\n'
    topics_file.close()
    topics_csv.close()
    # For demo purposes
    clean()

def clean():
    os.remove('parameters/gamma-all.dat')
    os.remove('parameters/lambda-all.dat')
    os.chdir('../.doc/')
    filelist = [ f for f in os.listdir('.') if f.endswith('.txt') ]
    for f in filelist:
        os.remove(f)

if __name__ == '__main__':
    main()
