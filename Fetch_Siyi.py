import sqlite3
import pandas as pd

DatabaseName = './Team2_Siyi.db'
connection = sqlite3.connect(DatabaseName)
cur = connection.cursor()


# Fetch a list of whole Gene Name
Genes = """
    SELECT DISTINCT EPIC.GeneName
    FROM EPIC
    WHERE EPIC.GeneName is NOT NULL;
"""

result = cur.execute(Genes).fetchall()
gene_list = []
for i in result:
    gene, = i
    if ';' in gene:
        temp_gene = gene.split(';')
        for each in temp_gene:
            gene_list.append(each)
    else:
        gene_list.append(gene)

print('There are', len(gene_list), 'genes in total!')
# with open("gene_list.txt", "w") as output:
#     output.write(str(gene_list))
print("Save the gene list named gene_list.txt at the current directory!")


# input a gene name and format the Gene Name
GN = 'DDX31'
GN = "'%" + GN + "%'"
print('Gene ', GN, ' is selected.')

probe_query = """
    SELECT EPIC.ProbeName
    FROM EPIC
    WHERE EPIC.GeneName LIKE {};
"""

# query for Jess
# "SELECT EPIC.ProbeName \
#   FROM EPIC \
#   WHERE EPIC.GeneName LIKE ?;"

probe_result = cur.execute(probe_query.format(str(GN))).fetchall()
probe_list = []
for i in probe_result:
    probe_list.append(i[0])
print('There are ', len(probe_list), 'probes corresponding to the Gene', GN)

with open("probe_list.txt", "w") as output:
    output.write(str(probe_list))

print('Please select one of the probe.')
probe = probe_list[1]
probe = "'" + probe + "'"
print('The probe you select is', probe)

# Get the Probe Key for the input Porbe Name
index_CpG = """
    SELECT PROBEINFO.ProbeKey
    FROM PROBEINFO
    WHERE PROBEINFO.ProbeName = {} ;
"""

# query for Jess
# "SELECT PROBEINFO.ProbeKey \
#     FROM PROBEINFO \
#     WHERE PROBEINFO.ProbeName = ?;"

result = cur.execute(index_CpG.format(probe)).fetchall()
index_CpG = result[0][0]
print('Probe', probe, 'is No.', index_CpG)

# Based on the Porbe Key, run the corresponding query
if index_CpG <= 107899:
    print('Go to AAA table')
    data_query = """
        SELECT PROBEINFO.ProbeName, PHENO.Age, PHENO.Sex, AAAVALUE.Value
        FROM PROBEINFO, PHENO, AAAVALUE
        WHERE AAAVALUE.ProbeKey = {}
        AND PROBEINFO.ProbeKey = {}
        AND AAAVALUE.SampleKey = PHENO.SampleKey;
    """
elif 307899 >= index_CpG > 107899:
    print('Go to BBB table')
    data_query = """
        SELECT PROBEINFO.ProbeName, PHENO.Age, PHENO.Sex, BBBVALUE.Value
        FROM PROBEINFO, PHENO, BBBVALUE
        WHERE BBBVALUE.ProbeKey = {}
        AND PROBEINFO.ProbeKey = {}
        AND BBBVALUE.SampleKey = PHENO.SampleKey;
    """
elif 507899 >= index_CpG > 307899:
    print('Go to CCC table')
    data_query = """
        SELECT PROBEINFO.ProbeName, PHENO.Age, PHENO.Sex, CCCVALUE.Value
        FROM PROBEINFO, PHENO, CCCVALUE
        WHERE CCCVALUE.ProbeKey = {}
        AND PROBEINFO.ProbeKey = {}
        AND CCCVALUE.SampleKey = PHENO.SampleKey;
    """
elif 807899 >= index_CpG > 507899:
    print('Go to DDD table')
    data_query = """
        SELECT PROBEINFO.ProbeName, PHENO.Age, PHENO.Sex, DDDVALUE.Value
        FROM PROBEINFO, PHENO, DDDVALUE
        WHERE DDDVALUE.ProbeKey = {}
        AND PROBEINFO.ProbeKey = {}
        AND DDDVALUE.SampleKey = PHENO.SampleKey;
    """

data_result = cur.execute(data_query.format(index_CpG, index_CpG)).fetchall()

# save the result here
CpG_list = []
Age_list = []
Value_list = []
Sex_list = []

for i in data_result:
    CpG, Age, Sex, Value = i
    CpG_list.append(CpG)
    Age_list.append(Age)
    Value_list.append(Value)
    Sex_list.append(Sex)

result_df = pd.DataFrame(list(zip(CpG_list, Age_list, Value_list, Sex_list)))
result_df.columns = ['CpG', 'Age', 'Value', 'Sex']
print(result_df)
# result_df.to_csv('./result_Siyi.csv', index=False)

print("Save the result as csv file at the current directory!")

cur.close()
connection.commit()
connection.close()

