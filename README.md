Topicalizer
=================

Topicalizer is a tool that allow you to process a bunch of SOAP API descriptors
in order to group the technical information they contain, in semantic related
categories, and specifying this categorization as RDF statements stored in a Sesame
triple-store. As a first step in the process of categorization, this tool applies 
text processing procedures over the service descriptors for extracting some relevant
technical information (operations, documentation and datatypes). Once such information
is available, the tool fits a probabilistic topic model, known as Online LDA, for
infering a set of relevant categories (topics--distributions over terms in a fixed 
vocabulary), and associate a probability distribution over such topics for each one 
of the service operations processed by the tool.

The Online LDA processing is based on the implementation of `ONLINE VARIATIONAL 
BAYES FOR LATENT DIRICHLET ALLOCATION` by Matthew D. Hoffman, which uses the online 
Variational Bayes (VB) algorithm presented in the paper "Online Learning for Latent 
Dirichlet Allocation" by Matthew D. Hoffman, David M. Blei, and Francis Bach.

The algorithm uses stochastic optimization to maximize the variational
objective function for the Latent Dirichlet Allocation (LDA) topic model.
It only looks at a subset of the total corpus of documents (namely, text files
whose content has been extracted from Web APIs documentation archives) 
each iteration, and thereby is able to find a locally optimal setting of
the variational posterior over the topics more quickly than a batch
VB algorithm could for large corpora.


##Files/Directories provided:
* `lib/`: Java Dependencies.
* `onlinelda/`: Folder containing the Python scripts which uses online VB for LDA to analyze 
  the information that has been extracted from SOAP API descriptors.
* `outcome/`: This folder holds the .txt and .csv files containing the results of
   applying Online LDA (`topics.<txt/csv>` and `per-document-topics.<txt/csv>`).
* `sesame_war/`: Folder containing deployable distribution of the `Sesame Framework`
  Server (`openrdf-sesame.war` and `openrdf-workbench.war`). 
* `run.sh`: Execution script.
* `sample-service-uris.txt`: File containing a list of 80 service descriptors available online
  (used as a sample input for the tool).
* `WebAPIDocProcessing.jar` Java App for performing parsing and text processing operations
  on the service descriptors.
* `README.md`: This file.

You will need to have the numpy and scipy packages installed somewhere
that Python can find them to use these scripts.


##System Requirements:
* `Java 1.6.x` or greater.
* `MySQL 5.5.x`
* `Apache Tomcat 7.x` (or any available servlet container, listening at 8080 port).

##Initial Settings
1. In MySQL create a Database with name `service_registry`.
2. Deploy both of the Sesame Framework .war files on your servlet container.
   After you have deployed the Sesame Server webapp, you should be able to access it, by
   default, at path `/openrdf-sesame` (`/openrdf-sesame/home/overview.view` for
   Apache Tomcat 7).
3. Create a new `Native Java Store` with ID `WebAPIModel` in the Sesame Server, by 
   accessing http://localhost:8080/openrdf-workbench/ -> `New repository`.
4. Give execution permissions on the `run.sh` script. Open a terminal and type:

   ```
   $chmod u+x run.sh
   ```
##Running
* Open a terminal and type `./run.sh` followed by the path of a text file containing the
  list of service descriptor URIs. You could use the `sample-service-uris.txt` provided
  with the tool.

  ```
  $./run.sh sample-service-uris.txt
  ```
  
* After running the whole process, you could verify that the Sesame store you have created
  has been populated with RDF statements corresponding to the categorization extracted by 
  running the Online LDA algorithm. These RDF statements instantiate the Classes and
  Properties defined in the RDF Schema model available at `onlinelda/rdf_sesame/web_api_model.rdf`.
  Additionally, the categorization results are also available as .txt and .csv files 
  at the `outcome/` foder:
  
  - `per-document-topics.<txt/csv>`: distribution over topics for each one of the processed 
  operations.

  - `topics.<txt/csv>`: distributions over terms for each one of the topics extracted.
  
  
