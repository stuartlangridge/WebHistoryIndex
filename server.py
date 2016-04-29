import os, datetime, urlparse
from flask import Flask, render_template, request, jsonify
from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, DATETIME, ID
from whoosh.qparser import QueryParser
from whoosh.writing import AsyncWriter
from bs4 import BeautifulSoup

app = Flask(__name__)

def get_index():
    ixname = "search-index"
    if os.path.isdir(ixname):
        from whoosh.index import open_dir
        ix = open_dir(ixname)
    else:
        schema = Schema(title=TEXT(stored=True), url=ID(stored=True, unique=True),
            content=TEXT(stored=True), modified=DATETIME(sortable=True))
        os.mkdir(ixname)
        ix = create_in(ixname, schema)
    return ix


@app.route("/")
def index():
    q = request.args.get("q")
    if not q:
        return render_template("index.html")
    ix = get_index()
    with ix.searcher() as searcher:
        query = QueryParser("content", ix.schema).parse(unicode(q))
        results = searcher.search(query)
        ret = []
        for result in results:
            ret.append({"title": result["title"], "url": result["url"],
                "extract": result.highlights("content"), "dt": result["modified"]})
        return render_template("index.html", results=ret, q=q)

@app.route("/add", methods=["POST"])
def add():
    d = request.get_json(force=True)
    url = d.get("url")
    content = d.get("content")
    if not url or not content: return jsonify({"status": "missing parameters"})
    if urlparse.urlparse(url).netloc.startswith("localhost"): return  jsonify({"status": "ignored"})
    ix = get_index()
    writer = AsyncWriter(ix)
    soup = BeautifulSoup(content)
    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()    # rip it out
    # get text
    text = soup.get_text()
    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)

    writer.update_document(title=d.get("title", "Untitled"),
        url=url,
        content=text,
        modified=datetime.datetime.now())
    writer.commit()
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(port=5150, debug=True)
