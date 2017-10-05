import web, logging

# @app.before_request
# def before_request():
# 	if web.request.url.startswith('http://'):
# 		url = web.request.url.replace('http://', 'https://', 1)
# 		code = 301
# 		return web.redirect(url, code=code)

if __name__ == "__main__":
	logging.basicConfig(filename='omf.log',level=logging.DEBUG)
	template_files = ["templates/"+ x  for x in web.safeListdir("templates")]
	model_files = ["models/" + x for x in web.safeListdir("models")]
	web.app.run(debug=False, host="0.0.0.0", port=80, extra_files=template_files + model_files, processes=4)