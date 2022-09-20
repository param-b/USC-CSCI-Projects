class WriterFuncs:
  filename = ''
  def __init__(self, filename):
    self.filename = filename

  def write_labels(self, string1, string2, score, time, memory):
    with open(self.filename, 'w') as f:
        f.write(string1[:50] + " " + string1[-50:])
        f.write('\n')
        f.write(string2[:50] + " " + string2[-50:])
        f.write('\n')
        f.write(str(float(score)))
        f.write('\n')
        f.write(str(float(time)))
        f.write('\n')
        f.write(str(float(memory)))
        f.write('\n')
