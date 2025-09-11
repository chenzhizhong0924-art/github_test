import os
import glob
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA

def Rag(text):

    base_path = os.path.dirname(os.path.abspath(__file__)) 
    pdf_folder = os.path.join(base_path, "pdfs")
    faiss_folder = os.path.join(base_path, "faiss_index")
    pdf_log_file = os.path.join(base_path, "pdf_log/pdf_log.txt")
    api_key_file = os.path.join(base_path, "api_key/api_key.txt")

    with open(api_key_file, "r", encoding="utf-8") as f:
        api_key = f.read().strip()
    os.environ["OPENAI_API_KEY"] = api_key

    os.makedirs(pdf_folder, exist_ok=True)
    os.makedirs(os.path.dirname(pdf_log_file), exist_ok=True)

    embeddings = OpenAIEmbeddings()
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50)

    db = None

    if os.path.exists(faiss_folder):
        print("載入已存在的 FAISS 向量資料庫...")
        db = FAISS.load_local(faiss_folder, embeddings, allow_dangerous_deserialization=True)

    if os.path.exists(pdf_log_file):
        with open(pdf_log_file, "r", encoding="utf-8") as f:
            added_pdfs = set(line.strip() for line in f)
    else:
        added_pdfs = set()

    pdf_files = set(glob.glob(os.path.join(pdf_folder, "*.pdf")) + \
                    glob.glob(os.path.join(pdf_folder, "*.PDF")))
    pdf_files = list(pdf_files)  


    new_pdfs = [p for p in pdf_files if p not in added_pdfs]

    if new_pdfs:
        print(f"發現新的PDF，加入向量資料庫...")
        all_docs = []
        for pdf_path in new_pdfs:
            loader = PyPDFLoader(pdf_path)
            docs = loader.load()
            all_docs.extend(docs)
            added_pdfs.add(pdf_path)

        chunks = splitter.split_documents(all_docs)

        if db is None:
            db = FAISS.from_documents(chunks, embeddings)
        else:
            db.add_documents(chunks)

        db.save_local(faiss_folder)
        print(f"FAISS 資料庫已更新並存檔到 {faiss_folder}")

        with open(pdf_log_file, "w", encoding="utf-8") as f:
            for p in added_pdfs:
                f.write(p + "\n")

    else:
        if db is None:
            print("沒有 PDF，建立初始 FAISS 向量資料庫（佔位文本）...")
            placeholder_docs = ["這是一個初始化的佔位文本，用於建立 FAISS 向量資料庫。"]
            db = FAISS.from_texts(placeholder_docs, embeddings)
            db.save_local(faiss_folder)
        else:
            print("沒有新 PDF，直接使用現有資料庫。")

#使用內建的Prompt
    qa = RetrievalQA.from_chain_type(
        llm=ChatOpenAI(model_name="gpt-4o-mini", temperature=0.2),
        retriever=db.as_retriever()
    )

    result = qa.run(text)
    return result


#自行加入Prompt的方式
    # prompt_template = """
    # 你是一個知識型助理。請根據提供的文件內容回答問題。
    # 若文件中無法找到相關答案，請回答：「該問題不在回答範疇之內」。
    # 如果文件是目錄，請只列出「章節名稱」，不要輸出頁碼或數字。

    # 問題: {question}
    # =========
    # 文件內容: {context}
    # =========
    # 請用條列方式回答:
    # """

    # PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])

    # qa = RetrievalQA.from_chain_type(
    #     llm=ChatOpenAI(model_name="gpt-4o-mini", temperature=0.2),
    #     retriever=db.as_retriever(),
    #     chain_type="stuff",
    #     chain_type_kwargs={"prompt": PROMPT}
    # )

    # result = qa.run(text)
    # return result

if __name__ == "__main__":
    userquestion = input("請輸入：")
    reply = Rag(userquestion)
    print(reply)