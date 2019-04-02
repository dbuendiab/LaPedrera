import datetime

class TiempoError(Exception):
    pass


class Tiempo(datetime.datetime):
    """Acepta todo tipo de formatos: datetime, tuple o lista, texto con varias opciones.
    Si no se pone el año, mes y/o día, se asumen los de la fecha actual."""
    
    @staticmethod
    def _aux_str_to_datetime(t_str):
        
        #print('t_str', t_str)
        
        today = datetime.datetime.now().date()
        day = today.day
        month = today.month
        year = today.year

        patrones = [
            '%Y-%m-%dT%H:%M', 
            '%Y-%m-%d %H:%M',
            '%Y-%m-%dT%H',
            '%Y-%m-%d %H',
            '%m-%dT%H:%M',
            '%m-%d %H:%M',
            '%m-%dT%H',
            '%m-%d %H',
            '%dT%H:%M',
            '%d %H:%M',
            '%dT%H',
            '%d %H',
            '%H:%M',
            '%H'
        ]

        fecha = None
        
        for i, p in enumerate(patrones):
            #print(i, p, t_str)
            #fecha = datetime.datetime.strptime(t_str, p)
            #print('RESULTADO?', fecha)
            try:
                fecha = datetime.datetime.strptime(t_str, p)
                if i in [4, 5, 6, 7]: fecha = fecha.replace(year=year)
                if i in [8, 9, 10, 11]: fecha = fecha.replace(year=year,month=month)
                if i in [12, 13]: fecha = fecha.replace(year=year, month=month, day=day)
                #print('\n', "OK", fecha)
                break
            except:
                continue
        
        return fecha
                
    
    def __new__(cls, *args, **kwargs):
        "Acepta un solo argumento, que puede ser un str o un datetime, o de 3 a 5, que serían argumentos para datetime"

        if 3 <= len(args) <= 5:
            try:
                #self = datetime.datetime(*args)
                self = datetime.datetime.__new__(cls, *args)
            except:
                raise TiempoError("Imposible convertir '%s' a fecha" % (args,))
                
        elif len(args) == 1:
            t = args[0]
            
            if isinstance(t, datetime.datetime):
                self = datetime.datetime.__new__(cls, t.year, t.month, t.day, t.hour, t.minute)

            elif isinstance(t, tuple) or isinstance(t, list):
                try:
                    self = datetime.datetime.__new__(cls, *t)
                except:
                    raise TiempoError("Imposible convertir '%s' a fecha" % t)
                    
            elif isinstance(t, str):
                try:
                    t = Tiempo._aux_str_to_datetime(t)
                    #print('T', t)
                    self = datetime.datetime.__new__(cls, t.year, t.month, t.day, t.hour, t.minute)
                except:
                    raise TiempoError("Imposible convertir '%s' a fecha" % t)
            else:
                raise TiempoError("Formato de '%s' no reconocido" % t)
        else:
            raise TiempoError("Número o tipo de parámetros incorrecto")
                    
        return self
                
    def __str__(self):
        return self.strftime('%Y-%m-%dT%H:%M')
                
    def __repr__(self):
        return '<%s:: %s>' % (self.__class__.__name__, str(self))
    
    def fmt_hora(self):
        return self.strftime('%H:%M')
    
    def fmt_dia(self):
        return self.strftime('%Y-%m-%d')


class ErrorIntervalo(Exception):
    pass

class Intervalo(object):
    def _validar(self):
        #print(self.t_fin - self.t_ini)
        delta = self.t_fin - self.t_ini
        if delta.days < 0:
            raise ErrorIntervalo("La fecha de inicio es posterior a la de finalización")
        else:
            intervalo = delta.days * 86400 + delta.seconds
            if intervalo > 86400:
                raise ErrorIntervalo("El intervalo es mayor de 24 horas")
            self._intervalo = intervalo
        
    def __new__(cls, t_ini, t_fin):
        #print('init Intervalo', t_ini, t_fin)
        self = super().__new__(cls)
        self.t_ini = Tiempo(t_ini)
        self.t_fin = Tiempo(t_fin)
        self._validar()
        return self
        
    def __str__(self):
        return "'" + str(self.t_ini) + "', '" + str(self.t_fin) + "'"
    
    def __repr__(self):
        return self.__str__()
    
    @property
    def intervalo(self):
        return {'horas': self._intervalo//3600, 'minutos': (self._intervalo//60)%60}
    
    @property
    def horas(self):
        return self.intervalo['horas']
    
    @property
    def minutos(self):
        return self.intervalo['minutos']
    
    def _cmp(self, i2):
        "Dos intervalos son iguales (a efectos de mi aplicación) si se superponen de algún modo"
        
        if not isinstance(i2, Intervalo):
            raise TiempoError("No se puede comparar intervalos si uno es del tipo %s" % type(i2))

        if self.t_fin <= i2.t_ini:
            return -1
        
        elif self.t_ini >= i2.t_fin:
            return 1
        
        else:
            return 0
    
    def __ne__(self, i2):
        return self._cmp(i2) != 0

    def __eq__(self, i2):
        return self._cmp(i2) == 0

    def __lt__(self, i2):
        return self._cmp(i2) == -1

    def __le__(self, i2):
        return False     ## A efectos de este objeto, no puede ser menor o igual al mismo tiempo: o son disjuntos o no

    def __gt__(self, i2):
        return self._cmp(i2) == 1

    def __ge__(self, i2):
        return False     ## A efectos de este objeto, no puede ser menor o igual al mismo tiempo: o son disjuntos o no




class EventoSimpleError(Exception):
    pass

class EventoSimple(Intervalo):
    
    def __new__(cls, *args, **kwargs):
        
        id_espacio = kwargs.get('id_espacio')
        t_ini = kwargs.get('t_ini')
        t_fin = kwargs.get('t_fin')
        
        if len(args) == 3:
            id_espacio = args[0]
            t_ini = args[1]
            t_fin = args[2]
        
        if len(args) == 1:
            ## Esperamos texto separado por espacio (fechas con T)
            try:
                id_espacio, t_ini, t_fin = args[0].split(' ')
            except Exception as e:
                raise EventoSimpleError('Texto de entrada malformado (se espera "id t_ini t_fin", sin espacios en las fechas)')
        
        self = super().__new__(cls, t_ini, t_fin)
        self.id_espacio = id_espacio
        return self
        
    def __str__(self):
        return ('%s %s' % (self.id_espacio, super().__str__())).replace("'","").replace(",","")
        #return 'id: %s, t_ini: %s, t_fin: %s, intervalo: %s' % \
        #    (self.id_espacio, self.t_ini, self.t_fin, self.intervalo)
    
    def __repr__(self):
        return '<EventoSimple:: id: %r, t_ini: %r, t_fin: %r, intervalo: %r>' % \
            (self.id_espacio, self.t_ini, self.t_fin, self.intervalo)
        #return self.__str__()
        
    def __eq__(self, otro_evento):
        if self.id_espacio == otro_evento.id_espacio:
            return super().__eq__(otro_evento)
        return False
        
    def __ne__(self, otro_evento):
        if self.id_espacio == otro_evento.id_espacio:
            return super().__ne__(otro_evento)
        return False
 
    def __lt__(self, otro_evento):
        if self.id_espacio == otro_evento.id_espacio:
            return super().__lt__(otro_evento)
        return False

    def __gt__(self, otro_evento):
        if self.id_espacio == otro_evento.id_espacio:
            return super().__gt__(otro_evento)
        return False
    
    def __le__(self, otro_evento):
        if self.id_espacio == otro_evento.id_espacio:
            return super().__le__(otro_evento)
        return False
    
    def __ge__(self, otro_evento):
        if self.id_espacio == otro_evento.id_espacio:
            return super().__ge__(otro_evento)
        return False



class EventosDiaError(Exception):
    pass

class EventosDia(list):
    
    def __init__(self, *args, **kwargs):
        texto = ''
        fecha = kwargs.get('fecha', '0')  ## Si viene fecha, se toma como referencia, si no se creará la del día
        
        largs = len(args)
            
        if largs >= 1:
            texto = args[0]
            
        if largs >= 2:
            fecha = args[1]
            
        self.fecha = Tiempo(fecha)
        self.texto = texto
        self.eventos = EventosDia._construir(texto, fecha)

    @staticmethod
    def _construir(texto, fecha):
        lista_eventos = EventosDia._construir_desde_texto(texto, fecha)
        lista_eventos = EventosDia._validar(lista_eventos)
        return lista_eventos
    
    @staticmethod
    def _construir_desde_texto(texto, fecha):
        lista_eventos = []
        lineas = texto.split('\n')
        for l in lineas:
            if not l: continue
            es = EventoSimple(l)
            lista_eventos.append(EventoSimple(l))
        return lista_eventos
    
    @staticmethod
    def _validar(lista_eventos):
        lista_eventos.sort(key=lambda x: x.id_espacio + str(x.t_ini))
        
        for ev1, ev2 in zip(lista_eventos, lista_eventos[1:]):
            #print('HEY', '\n', ev1, '\n', ev2)
            if ev1.id_espacio != ev2.id_espacio: 
                #print('Espacios diferentes')
                continue
            if(ev1 == ev2):
                raise EventosDiaError('Dos eventos se superponen:', str(ev1), str(ev2))
        return lista_eventos
    

    def append(self, evento):
        lista_tmp = self.eventos[:]
        lista_tmp.append(EventoSimple(evento))
        EventosDia._validar(lista_tmp)
        self.eventos = lista_tmp
    
    def __str__(self):
        out = ''
        for e in self.eventos:
            e1 = e.t_ini
            e2 = e.t_fin
            if e1.date() == e2.date():
                out += 'Espacio %s, fecha: %s - hora_inicio: %s / hora_final: %s' % (e.id_espacio, 
                                                                                     e1.fmt_dia(), e1.fmt_hora(), 
                                                                                     e2.fmt_hora())
            else:
                out += 'Espacio %s, fecha_inicio: %s %s/ fecha_final: %s %s' % (e.id_espacio, 
                                                                               e1.fmt_dia(), e1.fmt_hora(), 
                                                                               e2.fmt_dia(), e2.fmt_hora())
            out += '\n'
        return out
    
    def __repr__(self):
        return '<%s:: %s>' % (self.__class__.__name__, str(self)) 
    
        