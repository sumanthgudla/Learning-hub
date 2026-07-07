from langchain_community.document_loaders import PyPDFLoader

loader=PyPDFLoader('Learning docs/RAG Learning.pdf')
document=loader.load()
count=0
for doc in loader.lazy_load():
    if count==0:
        print(doc.metadata)
    count+=1
print(count)
total_count=count
count=0
for doc in loader.lazy_load():
    if count==total_count-1:
        data=doc.page_content
        print(data[:200])
    count+=1



    
