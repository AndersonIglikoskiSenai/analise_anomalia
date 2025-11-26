from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from analise_rede import analisar_csv

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/analisar-csv")
async def analisar_csv_api(arquivo: UploadFile = File(...)):
    try:
        conteudo = await arquivo.read()
        resultado = analisar_csv(conteudo)
        return JSONResponse(content=resultado)

    except Exception as e:
        return JSONResponse(status_code=500, content={"erro": str(e)})


@app.get("/")
def root():
    return {"status": "API de análise de tráfego ativa!"}
