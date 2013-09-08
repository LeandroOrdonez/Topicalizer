# model_instantiation.py: Package of functions for creating RDF statements
# according to the model defined in web_api_model.rdf
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

def new_term(term_id, term):
    return """<Term rdf:about="http://www.example.org/terms/%s">
    <has_content rdf:datatype="http://www.w3.org/2001/XMLSchema#string">%s</has_content>
    </Term>\n""" % (term_id, term)

def new_membership_relation(membership_relation_id, membership_probability, category_value):
    return """<Membership_Relation rdf:about="http://www.example.org/membership_relations/%s">
    <membership_probability rdf:datatype="http://www.w3.org/2001/XMLSchema#double">%.4f</membership_probability>
    <category_value rdf:resource="http://www.example.org/categories/%s"/>
    </Membership_Relation>\n""" % (membership_relation_id, membership_probability, category_value)

def new_operation(operation_id, operation_name, service_uri, membership_relations):
    memberships = ''.join(['<is_member_of rdf:resource="http://www.example.org/membership_relations/%s"/>\n' \
% membership for membership in membership_relations])
    return """<Operation rdf:about="http://www.example.org/operations/%s">
    <has_name rdf:datatype="http://www.w3.org/2001/XMLSchema#string">%s</has_name>
    <has_service_uri rdf:datatype="http://www.w3.org/2001/XMLSchema#anyURI">%s</has_service_uri>
    %s  
    </Operation>\n""" % (operation_id, operation_name, service_uri, memberships)

def new_term_relation(term_relation_id, term_probability, term_value):
    return """<Term_Relation rdf:about="http://www.example.org/term_relations/%s">
    <term_probability rdf:datatype="http://www.w3.org/2001/XMLSchema#double">%.4f</term_probability>
    <term_value rdf:resource="http://www.example.org/terms/%s"/>
    </Term_Relation>\n""" % (term_relation_id, term_probability, term_value)

def new_category(category_id, term_relations):
    terms = ''.join(['<has_term rdf:resource="http://www.example.org/term_relations/%s"/>\n' \
% term for term in term_relations])
    return """<Category rdf:about="http://www.example.org/categories/%s">
    %s  
    </Category>\n""" % (category_id, terms)
