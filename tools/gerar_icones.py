"""Gera src/components/icones-data.ts só com os ícones que o app usa.

Fontes (instaladas como devDependencies):
- game-icons.net (@iconify-json/game-icons), CC BY 3.0: ícones de jogo (mapa, chefes, relíquias).
  Crédito obrigatório: "Ícones de jogo: game-icons.net (CC BY 3.0)" (está em Perfil → Elenco e no README).
- Phosphor Icons (@iconify-json/ph), MIT: ícones de interface.
Rode:  python3 tools/gerar_icones.py
"""
import json, os
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.join(AQUI, "..")
G = json.load(open(os.path.join(RAIZ, "node_modules/@iconify-json/game-icons/icons.json")))
P = json.load(open(os.path.join(RAIZ, "node_modules/@iconify-json/ph/icons.json")))

ICONES = {
    # mapa (roguelite)
    "batalha": "g:crossed-swords", "elite": "g:horned-skull", "cura": "g:heart-plus", "misterio": "g:swirl-string",
    "tesouro": "g:open-treasure-chest", "bau-fechado": "g:locked-chest", "entrada": "g:entry-door", "chefe": "g:daemon-skull",
    "fogueira": "g:campfire", "pegada": "g:footprint", "mapa": "g:treasure-map", "dado": "g:perspective-dice-six-faces-random",
    # relíquias
    "pato": "g:duck", "cafe": "g:coffee-cup", "teclado": "g:keyboard", "escudo": "g:bolt-shield", "lupa": "g:magnifying-glass",
    # chefes
    "aranha": "g:spider-face", "besouro": "g:beetle-shell", "escaravelho": "g:scarab-beetle", "centopeia": "g:centipede",
    "gosma": "g:gooey-daemon", "diabrete": "g:imp-laugh", "caveira": "g:dread-skull", "dragao": "g:spiked-dragon-head",
    "golem": "g:robot-golem", "lodo": "g:slime",
    # níveis
    "ovo": "g:egg-clutch", "cobra": "g:snake", "terminal": "ph:terminal-window-fill", "cubo": "ph:cube-fill",
    "repetir": "ph:repeat-bold", "varinha": "ph:magic-wand-fill", "flechas": "g:target-arrows", "templo": "g:temple-gate", "coroa": "g:crown",
    # missões, conquistas, loja
    "raio": "ph:lightning-fill", "livro": "ph:book-open-fill", "alvo": "ph:target-fill", "cerebro": "ph:brain-fill",
    "chama": "ph:fire-fill", "fogo": "g:fire", "labareda": "g:flame", "grimorio": "g:spell-book", "play": "ph:play-fill",
    "martelo": "ph:hammer-fill", "broto": "g:sprout", "pilha-livros": "g:book-pile", "formatura": "ph:graduation-cap-fill",
    "mosca": "g:bullseye", "selo": "ph:seal-check-fill", "cometa": "g:energy-arrow", "estrela": "ph:star-fill",
    "medalha-estrela": "g:star-medal", "louros": "g:laurels-trophy", "raios": "g:lightning-trio", "teclado-ui": "ph:keyboard-fill",
    "engrenagem-martelo": "g:gear-hammer", "livros": "ph:books-fill", "pergaminho": "g:scroll-unfurled", "taca": "g:trophy-cup",
    "sacola": "g:swap-bag", "gelo": "g:ice-cube", "pocao": "g:heart-bottle", "gota": "ph:drop-fill", "planeta": "g:ringed-planet",
    "diamante": "g:cut-diamond", "presente": "ph:gift-fill", "confete": "ph:confetti-fill",
    # interface
    "sol": "ph:sun-fill", "lua": "ph:moon-fill", "celular": "ph:device-mobile-fill", "sino": "ph:bell-fill", "frasco": "ph:flask-fill",
    "info": "ph:info-fill", "check": "ph:check-bold", "x": "ph:x-bold", "cadeado": "ph:lock-simple-fill", "brilho": "ph:sparkle-fill",
    "coracao": "ph:heart-fill", "trofeu": "ph:trophy-fill", "lampada": "ph:lightbulb-fill", "olho": "ph:eye-fill",
    "desfazer": "ph:arrow-counter-clockwise-bold", "bandeira": "ph:flag-fill", "usuarios": "ph:users-fill", "lapis": "ph:pencil-simple-fill",
    "calculadora": "ph:calculator-fill", "lista": "ph:list-checks-fill", "pergunta": "ph:question-fill", "controle": "ph:game-controller-fill",
    "forca": "g:hanging-sign", "dados": "g:rolling-dices", "aviso": "ph:warning-fill", "triste": "ph:smiley-sad-fill", "sorriso": "ph:smiley-fill",
    "relogio": "ph:timer-fill", "ampulheta": "ph:hourglass-fill", "porta": "ph:door-open-fill", "copiar": "ph:copy-fill",
    "compartilhar": "ph:share-network-fill", "lixeira": "ph:trash-fill", "seta": "ph:caret-right-bold", "conversa": "ph:chat-circle-dots-fill",
    "inseto": "ph:bug-beetle-fill", "codigo": "ph:code-bold", "calendario": "ph:calendar-check-fill", "lojinha": "ph:storefront-fill",
    "usuario": "ph:user-fill", "estrela4": "ph:star-four-fill", "caveira-ui": "ph:skull-fill", "oculos": "ph:sunglasses-fill",
    "escudo-ui": "ph:shield-fill", "espada": "ph:sword-fill", "cofre": "ph:piggy-bank-fill", "foguete": "ph:rocket-launch-fill",
}

def pega(ref):
    fonte, nome = ref.split(":", 1)
    s = G if fonte == "g" else P
    i = s["icons"].get(nome)
    if i is None and nome in s.get("aliases", {}):
        i = s["icons"][s["aliases"][nome]["parent"]]
    if i is None:
        raise SystemExit(f"ícone não encontrado: {ref}")
    return {"b": i["body"], "w": i.get("width", s.get("width", 16)), "h": i.get("height", s.get("height", 16))}

dados = {k: pega(v) for k, v in ICONES.items()}
ts = ["// Gerado por tools/gerar_icones.py. Não edite à mão.",
      "// game-icons.net (CC BY 3.0, Lorc, Delapouite e outros) e Phosphor Icons (MIT).",
      f"export const ICONES = {json.dumps(dados, ensure_ascii=False)} as const;",
      "export type NomeIcone = keyof typeof ICONES;"]
open(os.path.join(RAIZ, "src/components/icones-data.ts"), "w").write("\n".join(ts) + "\n")
print(f"OK: {len(dados)} ícones, {sum(len(d['b']) for d in dados.values())//1024} KB")
