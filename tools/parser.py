def parseResponse( content:str ):
  print('Just applying some AI magic!')
  temp = content[content.lower().find('@s')+2:content.lower().find('@e')]
  one_line_array = temp.replace('\n', ' ')
  return eval(one_line_array)

