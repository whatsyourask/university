def get_file_data(filename):
  f    = open(filename, 'r')
  data = f.read()
  return data
  

def count_all(data):
  points = 0
  edges  = 0
  for elem in data:
    points += 1 if 'v' in elem else 0
    edges  += 1 if 'f' in elem else 0
  return points, edges


def get_max_min(data):
  x = []
  y = []
  z = []
  for elem in data:
    if 'v' in elem:
      x.append(elem[1])
      y.append(elem[2])
      z.append(elem[3])
  max_x = max(x)
  min_x = min(x)
  max_y = max(y)
  min_y = min(y)
  max_z = max(z)
  min_z = min(z)
  return max_x, min_x, max_y, min_y, max_z, min_z
  
  
def main():
  filename      = 'teapot.obj'
  data          = get_file_data(filename).split('\n')
  data          = [elem.split(' ') for elem in data]
  points, edges = count_all(data)
  print(f'points count: {points}')
  print(f'edges count: {edges}')
  max_min = get_max_min(data)
  print(f'max x = {max_min[0]}')
  print(f'min x = {max_min[1]}')
  print(f'max y = {max_min[2]}')
  print(f'min y = {max_min[3]}')
  print(f'max z = {max_min[4]}')
  print(f'min z = {max_min[5]}')


if __name__=='__main__':
  main()
