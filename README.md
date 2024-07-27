# USPS Fraud Detection with Louvain Community Detection on a Graph Database

## George Mason University
## Team Members: 
1. Khalil Chughtai
2. Bryan Vega
3. Hunter Walden
4. Matthew Koziol
5. Rosa Prieto

# How to run main_prod.ipynb
**NOTE** This is the primary notebook that shows each step of the research. The vast majority of the code that processes the data, executes community detection and scoring, and creating visualizations is abstracted away in separate python modules in the `scripts` folder. These modules are imported into the main_prod.ipynb file to keep the file cleaner and easier to follow. 

- To run locally do the following:
1. pip install dependencies in the requirements.txt file in a virtual environment
2. set up a file with file name: `.env`
3. copy and paste the following into the `.env` file
NEO4J_URI=neo4j+s://b91ef68f.databases.neo4j.io
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=<emailed separately>
AURA_INSTANCEID=b91ef68f
AURA_INSTANCENAME=Instance01
4. the neo4j password will be emailed out separately and must be included in the `NEO4J_PASSWORD` variable
5. run the notebook with the appropriate kernel environment set

## Assistance:
- Please reach out to hwalden2@gmu.edu or htwalden@gmail.com if assistance is required. 
