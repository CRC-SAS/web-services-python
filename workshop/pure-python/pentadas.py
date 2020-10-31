
import datetime
import calendar


# Funciones para el manejo de péntadas
# Determina a qué pentada del año corresponde una fecha (1-72)
def fecha_a_pentada_año(fecha: datetime):
    dia = fecha.day
    mes = fecha.month
    pentada_mes = 6 if dia > 25 else ( (dia - 1) // 5 ) + 1
    return int(pentada_mes + 6 * (mes - 1))
# FechaAPentadaAno <- function(fecha) {
#   dia         <- lubridate::day(fecha)
#   mes         <- lubridate::month(fecha)
#   pentada.mes <- ifelse(dia > 25, 6, ((dia - 1) %/% 5) + 1)
#   return (pentada.mes + 6 * (mes - 1))
# }


# Determina a qué pentada del mes corresponde una fecha (1-6)
def fecha_a_pentada_mes(fecha: datetime):
  pentada_año = fecha_a_pentada_año(fecha)
  return int(((pentada_año - 1) % 6) + 1)
# FechaAPentadaMes <- function(fecha) {
#   pentada.ano <- FechaAPentadaAno(fecha)
#   return (((pentada.ano - 1) %% 6) + 1)
# }


# Devuelve la fecha de inicio de una péntada de un añó determinado
def pentada_año_a_fecha_inicio(pentada_año: int, año: int):
    pentada_mes = ((pentada_año - 1) % 6) + 1
    dia = 1 + 5 * (pentada_mes - 1)
    mes = ((pentada_año - 1) // 6) + 1
    return datetime.datetime(int(año), int(mes), int(dia))
# PentadaAnoAFechaInicio <- function(pentada.ano, ano) {
#   pentada.mes <- ((pentada.ano - 1) %% 6) + 1
#   dia         <- 1 + 5 * (pentada.mes - 1)
#   mes         <- ((pentada.ano - 1) %/% 6) + 1
#   return (as.Date(sprintf("%d-%d-%d", ano, mes, dia)))
# }


# Obtener la fecha de inicio de péntada de una fecha determinada
def fecha_inicio_pentada(fecha: datetime):
   pentada_mes = fecha_a_pentada_mes(fecha)
   dia_inicio = 1 + 5 * (pentada_mes - 1)
   return datetime.datetime(fecha.year, fecha.month, int(dia_inicio))
# FechaInicioPentada <- function(fecha) {
#   pentada.mes <- FechaAPentadaMes(fecha)
#   dia.inicio  <- 1 + 5 * (pentada.mes - 1)
#   return (as.Date(sprintf("%d-%d-%d", lubridate::year(fecha), lubridate::month(fecha), dia.inicio)))
# }


# Obtener la fecha de fin de péntada de una fecha determinada
def fecha_fin_pentada(fecha: datetime):
    pentada_mes = fecha_a_pentada_mes(fecha)
    _, days_in_month = calendar.monthrange(fecha.year, fecha.month)
    dia_fin = 5 + 5 * (pentada_mes - 1) if pentada_mes < 6 else days_in_month
    return datetime.datetime(fecha.year, fecha.month, int(dia_fin))
# FechaFinPentada <- function(fecha) {
#   pentada.mes <- FechaAPentadaMes(fecha)
#   dia.fin     <- ifelse(pentada.mes < 6, 5 + 5 * (pentada.mes - 1), lubridate::days_in_month(fecha))
#   return (as.Date(sprintf("%d-%d-%d", lubridate::year(fecha), lubridate::month(fecha), dia.fin)))
# }
