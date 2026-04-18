import os
import chromadb

paths = ['/tmp/chroma_db', '/tmp/chromadb_vad', '/tmp/chromadb', '/tmp/chroma']
for p in paths:
    if os.path.exists(p):
        try:
            c = chromadb.PersistentClient(path=p)
            cols = [col.name for col in c.list_collections()]
            print(f'{p}: {cols}')
            for col_name in cols:
                col = c.get_collection(col_name)
                print(f'  {col_name}: {col.count()} entries')
        except Exception as e:
            print(f'{p}: ERROR {e}')
    else:
        print(f'{p}: does not exist')
