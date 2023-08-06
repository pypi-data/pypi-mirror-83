import os
from conf.configuration import *

path_template='/topic-ontologies/argument-inventory/argument-inventory-%s.csv'
path_vectors_template='/topic-ontologies/argument-inventory/document-vectors-%s-%s-argument-inventory-part-%d.csv'

"documents-vectors-wikipedia-esa-ibm-debater-claim-sentence-search-part-5.csv"
def generate_document_parts(dataset,label_template):
    count=get_part_count(dataset)
    path_dataset=get_dataset_conf_path(dataset)

    with open(path_dataset,'a+') as file:

        for i in range(0,count):
            label = label_template %(i)
            line =label+ "=" + path_template%(i)+"\n"
            file.write(line)

def generate_document_vectors_paths(dataset,label_template):
    count=get_part_count(dataset)
    ontologies=get_topic_ontologies()
    path_dataset=get_dataset_conf_path(dataset)
    with open(path_dataset,'a+') as file:
        for ontology in ontologies:
            for i in range(0,count):
                label = label_template %(ontology,'esa',i)
                line =label+ "=" + path_vectors_template%(ontology,'esa',i)+"\n"
                file.write(line)
