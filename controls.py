import db

def espais_complexos(tipus, clase=None):
    
    lista_ec = db.get_ec()
    
    if tipus == "select":
        
        output = '<select class="' + (clase + ' ' if clase else '') + 'form-control" size="1">\n'
        for ec in lista_ec:
            color = ec['color']
            id = ec['id']
            nom = ec['nom']
            output += '<option value:"%s" style="background-color: %s">%s</option>\n' % (id, color, nom)
        output += '</select>\n'

    return output