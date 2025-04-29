def exibeResposta_GUI(texto, resposta, nome):
    return resposta.replace("Chatbot",nome)
    
def saudacao_GUI(nome):
    import random
    frases = ["Bom dia! Meu nome é " + nome + ". Como vai você?", "Olá!", "Oi, tudo bem?"]
    return frases[random.randint(0,2)]

def salva_sugestao(sugestao):
    with open("BaseDeConhecimento.txt","a+") as conhecimento:
        conhecimento.write("Chatbot: " + sugestao + "\n")
        
def buscaResposta_GUI(texto):
    with open("BaseDeConhecimento.txt","a+") as conhecimento:
        conhecimento.seek(0)
        while True:
            viu = conhecimento.readline()
            if viu != "":
                if jaccard(texto,viu) > 0.3:
                    proximalinha = conhecimento.readline()
                    if "Chatbot: " in proximalinha:
                        return proximalinha
            else:
                conhecimento.write('\n' + texto)
                return "Me desculpe, não sei o que falar"
            
def jaccard(textoUsuario, textoBase):
    textoUsuario = limpa_frase(textoUsuario)
    textoBase = limpa_frase(textoBase)
    if len(textoBase)<1: return 0
    else:
        palavras_em_comum = 0
        for palavra in textoUsuario.split():
            if palavra in textoBase.split():
                palavras_em_comum += 1
        return palavras_em_comum/(len(textoBase.split()))
    
def limpa_frase(frase):
    tirar = ["?","!","...",".",",","Cliente: ", "\n"]
    for t in tirar:
        frase = frase.replace(t,"")
    frase = frase.upper()
    return frase