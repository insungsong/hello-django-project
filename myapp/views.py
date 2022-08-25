import random
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt

nextId = 4

topics = [
    {'id':1, 'title':'routing', 'body':'Routing is ..'},
    {'id':2, 'title':'view', 'body':'View is ..'},
    {'id':3, 'title':'Model', 'body':'Model is ..'},
]

def HTMLTemplete(article,id=None):
    global topics
    contextUI = ''
    if id != None:
        contextUI = f'''<li>
                        <form action = "/delete/" method="post">
                            <input type = "hidden" name = "id" value={id}>
                            <input type = "submit" value="delete">
                        </form>
                        </li>
                        <li><a href="/update/{id}/">update</a></li>
                    '''
    
    ol = ''
    for topic in topics:
        ol += f'<li><a href="/read/{topic["id"]}">{topic["title"]}</a></li>'
    
    
    return f'''
    <html>
        <body>
            <h1>Django</h1>
            <ol>{ol}</ol>
            {article}
            <ul>
                <li><a href = "/create">create</a></li>
                {contextUI}
            </ul>
        </body>    
    </html>
    '''

# Create your views here.
def index(request):
    article = '''
    <h2>welcome</h2>
    Hello, django
    '''
    return HttpResponse(HTMLTemplete(article))

def read(request, id):
    global topics
    article = ''
    
    for topic in topics:
        if str(topic["id"]) == id:
            article = f'<h2>{topic["title"]}</h2>{topic["body"]}'
    return HttpResponse(HTMLTemplete(article, id))        
    

@csrf_exempt
def create(request):
    global nextId
    print("request.body:",request.method)
    print("post: ",request.POST)
    if (request.method == 'GET'):
        article = '''
        <form action="/create/" method="post">
            <p><input type="text" name="title"></p>
            <p><textarea name="body"></textarea></p>
            <p><input type="submit"></p>
        </form>
        '''
        return HttpResponse(HTMLTemplete(article))

    elif request.method == 'POST':
        
        title = request.POST['title']
        body = request.POST['body']
        newTopic = {"id":nextId, "title":title, "body":body}
        url = '/read/' + str(nextId)
        nextId = nextId + 1
        topics.append(newTopic)
        return redirect(url)
        


@csrf_exempt
def delete(request):
    global topics
    if (request.method == 'POST'):
        id = request.POST['id']
        print('id: ', id)
        newTopics = []
        for topic in topics:
            if topic['id'] != int(id):
                newTopics.append(topic)
    topics = newTopics
    
    return redirect('/')
    

@csrf_exempt
def update(request, id):
    global topics

    for topic in topics:
        if topic["id"] == int(id):
            selectTopic = {
                "title": topic["title"],
                "body": topic["body"]
            }
            
    if(request.method == 'GET'):
        article = f'''
        <form action="/update/{id}/" method="post">
            <p><input type="text" name="title" value={selectTopic["title"]}></p>
            <p><textarea name="body">{selectTopic["body"]}</textarea></p>
            <p><input type="submit"></p>
        </form>
        '''
        
        return HttpResponse(HTMLTemplete(article, id))
    
    elif (request.method == 'POST'):
        title = request.POST["title"]
        body = request.POST["body"]
        
        for topic in topics :
            if topic["id"] == int(id):
                topic["title"] = title
                topic["body"] = body

        return redirect('/read/{id}')
    
