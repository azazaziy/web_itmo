import json
class HtmlGenerator:
    def __init__(self, input_json):
        data = json.loads(input_json)
        self.page = """
<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Title</title>
    </head>
        {body}
    <body>
    </body>
</html>
        """

    def generate_table(self, table_dict:dict):
        cols = table_dict['cols']
        rows = table_dict['rows']
        table_html = "<table>\n\t{headers}\n\t{body}</table>"

        headers = "<tr>\n{headers_list}\t</tr>\n"
        body = "<tr>\n{body_list}\t</tr>\n"
        headers_list = self.generate_list_tags('td', table_dict['headers'], padding='\t'*2)
        body_list = self.generate_list_tags('td', table_dict['body'], padding='\t'*2)
        headers = headers.format(headers_list=headers_list)
        body = body.format(body_list=body_list)

        return table_html.format(headers=headers, body=body)
    @staticmethod
    def generate_list_tags(tag:str, values_list:list, padding:str):
        item = ''
        for value in values_list:
            tags_html = "{padding}<{tag}>{value}</{tag}>\n"
            item += tags_html.format(value=value, tag=tag, padding=padding)
        return item


if __name__ == "__main__":
    kek = HtmlGenerator
    a = kek.generate_table(kek, {'headers':['a','b','c'], 'rows':3, 'cols':4, 'body':[1,2,3]})
    print(a)