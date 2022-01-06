import json
import cherrypy

def write_to_json(data, filename='points.json'):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)




class pointsRecords(object):

    @cherrypy.expose
    def index(self):
        return "Use a specific endpoint, not just the base url"

    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    @cherrypy.expose
    def addPoints(self):

        if cherrypy.request.method == "POST":

            output_json = json.loads(cherrypy.request.json)

            with open('points.json') as json_file:
                data = json.load(json_file)
                data["transactions"].append(output_json)
            write_to_json(data)

            print(output_json)
            return output_json

        else:

            return 'Must be a post request'



if __name__ == '__main__':
    cherrypy.quickstart(pointsRecords())