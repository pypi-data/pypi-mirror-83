#!/usr/bin/env python3

# API Helpers

from pydan import jdata
import requests
import urllib

# ejemplos call
# req={
#     "method": "PATCH",
#     "url":"https://graph.microsoft.com/v1.0/users/$azureuserid$",
#     "headers":{ "Authorization":"Bearer $token$", },
#     "data": "$data$"
# }
# ret=api.call(req,{"token":token, "azureuserid":azureuserid, "data":data})


#{{{ call: Realiza una llamada a un servicio REST o HTTP
def call(request=None, data=None):

	# Reemplazamos datos del request si hay variables
	if data is not None:
		#request=jdata.replacevars(request, data, flags={"nullremove"})
		request=jdata.replacevars(request, data)

	# defaults
	enctype="json"
	method="POST"

	# Validamos url
	url=request.get("url")
	if url is None:
		return {"code":"0","data":"Error: url empty"}

	# Procesamos method
	if request.get("method"):
		method=request.get("method")
		if method=="FORM":
			method="POST"
			enctype="form"

	# Procesamos headers
	headers={}
	if request.get("headers"):
		headers=request["headers"]
	if enctype=="json":
		if not headers.get("Content-Type"):
			headers.update({"Content-Type":"application/json"})

	# Procesamos data
	data=None
	if request.get("data"):
		#print(request["data"])
		if method=="GET":
			data=None
			query=None
			for k,v in request["data"].items():
				if query is None: query=""
				else: query=query+"&"
				query=query+k+"="+v
			url=url+"?"+query
		if method=="POST" or method=="PATCH" or method=="PUT":
			if enctype=="form":
				data=request["data"]
			else:
				data=jdata.tojson(request["data"])

	# urlencoding
	url=urllib.parse.quote(url, safe='%:/?=$&+()')

	# do call
	response=requests.request(method, url, headers=headers, data=data)

	# TODO: comprobar {": ?
	respdata=response.content.decode('UTF-8')
	if respdata[0:1]=='{':
		respdata=jdata.fromjson(respdata)

	return {"code":response.status_code, "data":respdata}
