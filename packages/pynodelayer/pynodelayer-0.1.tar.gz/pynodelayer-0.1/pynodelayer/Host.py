from p_listener import sio

@sio.event
def runTask(data):
  func = data['func']
  args = data['args']

  possibles = globals().copy()
  possibles.update(locals())
  method = possibles.get(func)
  if not method:
      raise NotImplementedError("Method %s not implemented" % func)
  method(args)

def install(a):
  print("In install")
  print(a)
