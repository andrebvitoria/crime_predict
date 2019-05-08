import pdf2txt
import Arquivo
import json

def main():
    lote = 'lote.txt'
    json_dir = 'JSON'
    cat_dir = 'BOLETIM'
    CAT = pdf2txt.Diretorio(cat_dir)
    JSON = pdf2txt.Diretorio(json_dir)
    JSON.listar(lote)

    pastas = Arquivo.abrir(json_dir + '/' + lote)[:-1]
    cat = dict()
    desc = dict()
    for pasta in pastas:
        print('Carregando ' + pasta)
        arquivo = json_dir + '/' + pasta + '/' + pasta + '.json'
        arq = open(arquivo, 'rt', encoding='cp1252')
        boletins = json.load(arq)
        for boletim in boletins:
            key = boletim.get('codigo')[:3]
            if not key in cat:
                cat[key] = list()
            if not boletim.get('codigo') in desc:
                desc[boletim.get('codigo')] = boletim.get('descricao')
            cat[key].append(json.dumps(boletim) + ',')

    
    lst_desc = list()
    keys = sorted(desc.keys())
    for key in keys:
        lst_desc.append( '"'+ key + '":"' + desc.get(key) + '",')
    lst_desc[-1] = lst_desc[-1][:-1]
    lst_desc = ['{'] + lst_desc + ['}']
    Arquivo.sobrescrever('codigo.json', lst_desc)

    keys = sorted(cat.keys())
    print(keys)
    for key in keys:
        print('Salvando ' + key)
        if len(key) > 1:
            CAT.criar(CAT.concatena(key[0], key))
            lst = cat.get(key)
            lst[-1] = lst[-1][:-1]
            lst = ['['] + lst + [']']
            Arquivo.sobrescrever(cat_dir + '/' + key[0] + '/' + key + '/' + 'boletim.json', lst)
        else:
            CAT.criar(key)
            lst = cat.get(key)
            lst[-1] = lst[-1][:-1]
            lst = ['['] + lst + [']']
            Arquivo.sobrescrever(cat_dir + '/' + key + '/' + 'boletim.json', lst)
    return


if __name__ == '__main__':
    main()