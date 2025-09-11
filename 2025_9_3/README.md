# RAG 使用說明

本專案分為兩個部分：
1. **單純 RAG**：在終端機中輸入問題並獲得回答。
2. **RAG + Flask**：透過網頁介面讓使用者輸入問題，並獲得回應。

---

## 環境設定

1. 建立虛擬環境並啟動：
```bash
conda create -n rag python=3.9 --yes
conda activate rag
```

2. 安裝必要套件：
```bash
pip install -r requirement.txt
conda install -c pytorch faiss-cpu
```

---

## API Key 設定

本專案使用 OpenAI 生成模型，請將 API Key 寫入：
```
Rag/api_key/api_key.txt
```

---

## 資料準備

將需要作為資料庫的 PDF 檔放入：
```
Rag/pdfs/
```

---

## 紀錄檔案
所有的聊天紀錄在logs/(按照時間)，加入pdf的路徑記錄在Rag/pdf_log/ 。
要刪除記錄檔可以呼叫下方兩個指令。
```
python .\tool\clear_logs.py
python .\tool\clear_rag_pdflog.py
```

## 使用方式

### 1. 單純 RAG
執行以下指令：
```bash
python .\Rag\rag.py
```
使用者可在終端機輸入問題，呼叫 RAG 函數後即可獲得回答。

### 2. RAG + Flask
執行以下指令：
```bash
python server_rag.py
```
啟動 Flask 網頁介面後，使用者可在網頁中輸入問題，並即時獲得回答。