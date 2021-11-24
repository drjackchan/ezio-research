from fastapi import FastAPI, Request
from fastapi.params import Body
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import random

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")
sentenses = [
    'While the mother dressed the baby shat on the floor. Funny innit? Please refresh the page!', 
    'Sentense number two is great!', 
    'Keep up your good work, programming is fun!', 
    'The world is so big!', 
]

@app.get('/',response_class = HTMLResponse)
async def home(request: Request):
    sent = 'Press Enter to read.'
    return templates.TemplateResponse('home.html', {'request':request, 'sent':sent})
@app.get("/items/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str):
    return templates.TemplateResponse("item.html", {"request": request, "id": id})

@app.post('/go/{i}')
async def go(request: Request, i:str):
    json_data = await request.json()
    _sentense_id = json_data.get("sentense_id")
    sentense_id = _sentense_id if _sentense_id != -1 else random.randrange(0, 3)
    s = sentenses[sentense_id] 
    a = s.split(' ')
    sent = ''
    i = int(i)
    if (i < len(a)):
        for j,each in enumerate(a):
            if j == i:
                sent = sent+each+' '
            else:
                sent = sent + (len(each)+1)*'_'+' '
        r = templates.TemplateResponse('inplace.html',{'request':request, 'sent':sent})
        content = r.template.render(r.context)
        result = Result()
        result.sentense_id = sentense_id
        result.body =  content
        return jsonable_encoder(result)
    else:
        result = Result()
        result.sentense_id = -1;
        return jsonable_encoder(result) 

class Result:
    sentense_id = -1
    body = ""