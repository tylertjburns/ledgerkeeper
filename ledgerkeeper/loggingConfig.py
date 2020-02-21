import logging

rootLogger = logging.getLogger('')
rootLogger.handlers = []
rootLogger.setLevel(logging.DEBUG)

#formatters
fileFormatter = logging.Formatter('%(name)s -- %(asctime)s : [%(levelname)s] %(message)s (%(filename)s lineno: %(lineno)d)')
consoleFormatter = logging.Formatter('%(name)s -- %(asctime)s : [%(levelname)s] %(message)s (%(filename)s lineno: %(lineno)d)')


#Console Handler
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
console.setFormatter(consoleFormatter)
rootLogger.addHandler(console)

#file Handler
file = logging.FileHandler(filename='..\ledgerKeeper.log', mode='w')
file.setLevel(logging.DEBUG)
file.setFormatter(fileFormatter)
rootLogger.addHandler(file)

