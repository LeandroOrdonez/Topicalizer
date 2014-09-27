# sesamehandler.py: Package of functions for storing RDF data into a
# Sesame Repository by using the HTTP-based communication protocol 
# for Sesame 2.
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

import urllib
import httplib2

class SesameHandler:

    def __init__(self, repository='WebAPIModel', sesame_server='http://localhost:8080/openrdf-sesame/', \
namespace='http://www.topicalizer.org/web_api_model.rdf', resource='statements'):
        """
	Documentation...
        """
        self.endpoint='%srepositories/%s/%s' % (sesame_server, repository, resource)
        self.rdf_wrap="""<rdf:RDF
xmlns=\""""+namespace+"""#"
xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
xml:base=\""""+namespace+"""">
%s
</rdf:RDF>"""

    def post_statements(self, rdf_encoded_data):
        #print 'POSTing statement to %s' % (self.endpoint)
        data = self.rdf_wrap % (rdf_encoded_data)
        headers= {
            'content-type': 'application/rdf+xml;charset=UTF-8'
        }
        (response, content) = httplib2.Http().request(self.endpoint, 'POST', body=data, headers=headers)
        #print 'Response %s' % response.status
        #print content

    def delete_statements(self, subj=None, pred=None, obj=None):
        params = {
            'subj': subj,
            'pred': pred,
            'obj': obj
        }
        (response, content) = httplib2.Http().request(self.endpoint, 'DELETE', urllib.urlencode(params))
        #print 'Response %s' % response.status
        #print content

    def post_rdf_file(self, rdf_file_path):
        data = file(rdf_file_path).read()
        headers= {
            'content-type': 'application/rdf+xml;charset=UTF-8'
        }
        (response, content) = httplib2.Http().request(self.endpoint, 'POST', body=data, headers=headers)
        #print 'Response %s' % response.status
        #print content
