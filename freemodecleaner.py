import re
map = {}
with open('natives.hpp', 'r') as f:
    line = f.readline()
    while line:
        try:
            try:
                namespace = re.search('namespace (.*?)$', line).group(1)
            except:
                pass
            lol = re.search('NATIVE_DECL (.*?) (.*?)\((.*?)\) \{ return invoke<(.*?)>\((.*?)\); \}', line)
            map[namespace+"::"+lol.group(2)] = {'old_hash': lol.group(5).split(',', 1)[0]}
        except:
            pass
        line = f.readline()
print('Finished native map')
crossmap = {}
with open('crossmap.hpp', 'r') as f:
    line = f.readline()
    while line:
        try:
            hashes = re.search('\{ (.*?), (.*?) \},', line)
            crossmap[hashes.group(1)] = hashes.group(2)
        except:
            pass
        line = f.readline()
print('Finished crossmap')
for x in map:
    try:
        map[x]['new_hash'] = crossmap[map[x]['old_hash']]
    except:
        print(f'Crossmap for {x} is missing.')

print('Mapping completed, cleaning freemode.ysc.c')
with open('freemode.ysc.c', 'r') as f:
    freemode = f.read()
with open('freemode.ysc.clean.c', 'w+') as f:
    for x in map:
        try:
            print(f'Replacing {x}')
            freemode = freemode.replace(f'unk_{map[x]["new_hash"]}', x)
        except:
            pass
    f.write(freemode)
print('Finished cleaning freemode.ysc.c')