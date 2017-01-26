import subprocess

p = subprocess.Popen(['transmission-show', 'Vinyl - Temporada 1  [HDTV 720p][Cap.103][V.O. Subt. Castellano].torrent'], stdout=subprocess.PIPE)
output, err = p.communicate()



for line in output.stdout:
    print line

class Foo:
    def __init__(self):
        vars=('tx', 'ty', 'tz')  # plus plenty more
        for v in vars:
            setattr(Foo, v, 0)

b=Foo()


