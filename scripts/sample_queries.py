# Similar to a SELECT * FROM ...
# () represents a node
# (label:Node {parameter: "value", ...})
# [] represents relationship


#returns every node and its relationships
query_all_data = '''
    MATCH (n)
    OPTIONAL MATCH (n)-[r]->(m)
    RETURN n, r, m
    ''' 

# query companies that have delinked MIDS -> the mailPieces and the destinations
query_company_delinked_mid = '''
    MATCH (co:company)-[o:owns]->(mid:mailer {delinked: "TRUE"})-[ma:mails]->(mp:mailPiece)-[gt:`goes to`]->(des:destination)
    RETURN co, o, mid, ma, mp, gt, des
    '''

# query companies that have delinked MIDS and firstzip_startzip_diff TRUE
query_company_fraud1 = '''
    MATCH (co:company)-[o:owns]->(mid:mailer)-[ma:mails]->(mp:mailPiece)-[gt:`goes to`]->(des:destination)
    WHERE mid.delinked = "TRUE" AND mp.firstzip_startzip_diff = "TRUE"
    RETURN co, o, mid, ma, mp, gt, des
    '''

# query companies that have delinked MIDS or firstzip_startzip_diff TRUE
query_company_fraud2 = '''
    MATCH (co:company)-[o:owns]->(mid:mailer)-[ma:mails]->(mp:mailPiece)-[gt:`goes to`]->(des:destination)
    WHERE mid.delinked = "TRUE" OR mp.firstzip_startzip_diff = "TRUE"
    RETURN co, o, mid, ma, mp, gt, des
    '''