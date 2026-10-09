/** Pipo local: analisa erros e sugere correções (roda no Python do aparelho). */
export const PY_ASSISTANT = String.raw`
# Pipo, o assistente de código do PyPasso.
# Recebe os arquivos, o arquivo executado e o erro (traceback) e devolve, em
# português, onde está o problema, por que acontece, como corrigir, dicas de
# melhoria e, quando é seguro, uma versão corrigida do arquivo.
import ast, builtins, difflib, json, keyword, re

_BUILTINS = set(dir(builtins))
_SHADOW = {"list", "str", "dict", "set", "tuple", "int", "float", "sum", "max", "min",
           "input", "print", "len", "type", "id", "range", "open", "sorted", "map", "filter"}
_JS = {"push": "append", "length": None, "toUpperCase": "upper", "toLowerCase": "lower",
       "trim": "strip", "indexOf": "index", "includes": None, "size": None, "add": "append"}


def _lines(code):
    return code.split("\n")


def _line(code, n):
    ls = _lines(code)
    return ls[n - 1] if n and 0 < n <= len(ls) else ""


def _indent(s):
    return len(s) - len(s.lstrip(" "))


def _split_comment(s):
    """Separa o código do comentário (#) fora de strings."""
    q = None
    for i, ch in enumerate(s):
        if q:
            if ch == q:
                q = None
        elif ch in "\"'":
            q = ch
        elif ch == "#":
            return s[:i].rstrip(), s[i:]
    return s.rstrip(), ""


def _names_in(code):
    """Nomes que o código define (variáveis, funções, classes, parâmetros, imports)."""
    out = set()
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return set(re.findall(r"^\s*([A-Za-z_]\w*)\s*=", code, re.M)) | set(re.findall(r"def\s+(\w+)", code))
    for n in ast.walk(tree):
        if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Store):
            out.add(n.id)
        elif isinstance(n, (ast.FunctionDef, ast.ClassDef)):
            out.add(n.name)
        elif isinstance(n, ast.arg):
            out.add(n.arg)
        elif isinstance(n, ast.alias):
            out.add((n.asname or n.name).split(".")[0])
    return out


def _parse_error(error_text, entry):
    """Tira do traceback: tipo, mensagem, arquivo e linha."""
    if not error_text:
        return None
    lines = [l for l in error_text.strip().split("\n") if l.strip()]
    last = lines[-1].strip()
    m = re.match(r"^([A-Za-z_][\w.]*(?:Error|Exception|Exit|Interrupt|Warning)):?\s*(.*)$", last)
    etype, msg = (m.group(1), m.group(2)) if m else (None, last)
    fname, lineno = None, None
    for f, n in re.findall(r'File "([^"]+)", line (\d+)', error_text):
        fname, lineno = f, int(n)
    # Preferir a última linha do arquivo executado quando o erro nasce em outro módulo
    return {"tipo": etype, "msg": msg, "arquivo": fname or entry, "linha": lineno, "texto": error_text}


def _input_vars(code, upto=None):
    """Variáveis atribuídas direto de input() (sem int/float)."""
    out = {}
    for i, l in enumerate(_lines(code), 1):
        if upto and i > upto:
            break
        m = re.match(r"^(\s*)([A-Za-z_]\w*)\s*=\s*(input\(.*\))\s*$", _split_comment(l)[0])
        if m:
            out[m.group(2)] = i
    return out


def _P(linha, codigo, titulo, explicacao, como, arquivo=None):
    return {"linha": linha, "codigo": codigo.strip() if codigo else "", "titulo": titulo,
            "explicacao": explicacao, "como_corrigir": como, "arquivo": arquivo}


# ---------------------------------------------------------------- correções
def _fix_line(code, n, new_line):
    ls = _lines(code)
    ls[n - 1] = new_line
    return "\n".join(ls)


def _fix_syntax(code, err):
    """Tenta corrigir um SyntaxError. Devolve (código, descrição) ou (None, None)."""
    n, msg = err.lineno, err.msg or ""
    if not n:
        return None, None
    line = _line(code, n)
    body, comment = _split_comment(line)
    sp = " " + comment if comment else ""
    if msg.startswith("expected ':'"):
        return _fix_line(code, n, body + ":" + sp), f"Linha {n}: coloquei os dois-pontos que faltavam."
    if "Maybe you meant '==' or ':='" in msg or "cannot assign to" in msg and re.match(r"\s*(if|elif|while)\b", body):
        nb = re.sub(r"(?<![=!<>])=(?!=)", "==", body, count=1)
        if nb != body:
            return _fix_line(code, n, nb + sp), f"Linha {n}: troquei = por == na comparação."
    if msg.startswith("Missing parentheses in call to 'print'"):
        m = re.match(r"^(\s*)print\s+(.+)$", body)
        if m:
            return _fix_line(code, n, f"{m.group(1)}print({m.group(2)})" + sp), f"Linha {n}: coloquei os parênteses do print."
    if msg.startswith("unterminated string literal"):
        col = (err.offset or 1) - 1
        q = line[col] if 0 <= col < len(line) and line[col] in "\"'" else '"'
        if body.endswith(")") and body.count("(") <= body.count(")"):
            nb = body[:-1] + q + ")"
        else:
            nb = body + q
        return _fix_line(code, n, nb), f"Linha {n}: fechei as aspas da string."
    m = re.match(r"'([(\[{])' was never closed", msg)
    if m:
        close = {"(": ")", "[": "]", "{": "}"}[m.group(1)]
        missing = body.count(m.group(1)) - body.count(close)
        if missing > 0:
            return _fix_line(code, n, body + close * missing + sp), f"Linha {n}: fechei o '{m.group(1)}' que estava aberto."
    if msg.startswith("expected an indented block"):
        prev = n - 1
        while prev > 0 and not _line(code, prev).strip():
            prev -= 1
        base = _indent(_line(code, prev))
        return _fix_line(code, n, " " * (base + 4) + line.lstrip()), f"Linha {n}: recuei a linha para dentro do bloco."
    if msg.startswith("unexpected indent") or msg.startswith("unindent does not match"):
        prev = n - 1
        while prev > 0 and not _line(code, prev).strip():
            prev -= 1
        target = _indent(_line(code, prev)) if msg.startswith("unexpected") else (_indent(line) // 4) * 4
        return _fix_line(code, n, " " * target + line.lstrip()), f"Linha {n}: acertei o recuo da linha."
    if "invalid character" in msg:
        trans = str.maketrans({"“": '"', "”": '"', "‘": "'", "’": "'", "–": "-", "—": "-"})
        nl = line.translate(trans)
        if nl != line:
            return _fix_line(code, n, nl), f"Linha {n}: troquei aspas/traços tipográficos pelos do teclado."
    return None, None


def _wrap_str_concat(line):
    """print("Idade: " + idade) -> print("Idade: " + str(idade))"""
    stripped = line.strip()
    try:
        tree = ast.parse(stripped)
    except SyntaxError:
        return None
    spans = []

    def is_str(e):
        return (isinstance(e, ast.Constant) and isinstance(e.value, str)) or isinstance(e, ast.JoinedStr) or \
               (isinstance(e, ast.Call) and isinstance(e.func, ast.Name) and e.func.id == "str")

    def walk_add(e, acc):
        # Cadeias de + são aninhadas à esquerda; um + à direita veio de parênteses
        # e deve ser tratado como um bloco só: "a" + (x + 1) -> "a" + str(x + 1)
        if isinstance(e, ast.BinOp) and isinstance(e.op, ast.Add):
            walk_add(e.left, acc)
            acc.append(e.right)
        else:
            acc.append(e)

    inner = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add) and id(node) not in inner:
            parts = []
            walk_add(node, parts)
            n = node.left
            while isinstance(n, ast.BinOp) and isinstance(n.op, ast.Add):
                inner.add(id(n)); n = n.left
            if any(is_str(p) for p in parts):
                for p in parts:
                    if not is_str(p) and isinstance(p, (ast.Name, ast.Attribute, ast.Subscript, ast.Call, ast.BinOp, ast.Constant)):
                        spans.append((p.col_offset, p.end_col_offset))
    if not spans:
        return None
    off = len(line) - len(stripped)
    raw = stripped.encode("utf-8")
    ch = lambda byte_off: len(raw[:byte_off].decode("utf-8"))  # ast usa offsets em bytes UTF-8
    out = line
    for a, b in sorted({(ch(a), ch(b)) for a, b in spans}, reverse=True):
        out = out[:off + a] + "str(" + out[off + a:off + b] + ")" + out[off + b:]
    return out


def _fix_runtime(code, info, all_names):
    """Correções seguras para erros de execução no arquivo executado."""
    n, t, msg = info["linha"], info["tipo"], info["msg"]
    line = _line(code, n)
    if t == "NameError":
        m = re.search(r"name '(\w+)' is not defined", msg)
        if m:
            bad = m.group(1)
            sug = re.search(r"Did you mean: '(\w+)'", msg)
            cand = sug.group(1) if sug else None
            if not cand:
                pool = [x for x in all_names | _BUILTINS if not x.startswith("_")]
                close = difflib.get_close_matches(bad, pool, n=1, cutoff=0.75)
                cand = close[0] if close else None
            if cand and cand != bad:
                nl = re.sub(rf"\b{re.escape(bad)}\b", cand, line)
                return _fix_line(code, n, nl), f"Linha {n}: troquei {bad} por {cand}."
            m2 = re.match(rf"^(\s*print\()\s*{re.escape(bad)}\s*(\).*)$", line)
            if m2 and bad not in all_names:
                return _fix_line(code, n, f'{m2.group(1)}"{bad}"{m2.group(2)}'), f'Linha {n}: coloquei {bad} entre aspas para virar texto.'
    iv = _input_vars(code, n)
    used_iv = [v for v in re.findall(r"\b([A-Za-z_]\w*)\b", line) if v in iv]
    if t == "TypeError" and used_iv and ("can only concatenate str" in msg or "'str'" in msg):
        v = used_iv[0]
        i = iv[v]
        ls = _lines(code)
        m = re.match(r"^(\s*)([A-Za-z_]\w*)\s*=\s*(input\(.*\))\s*$", _split_comment(ls[i - 1])[0])
        ls[i - 1] = f"{m.group(1)}{m.group(2)} = int({m.group(3)})"
        desc = f"Linha {i}: converti o input() de {v} para número com int()."
        if "can only concatenate str" in msg and i != n:
            nl = _wrap_str_concat(ls[n - 1])
            if nl:
                ls[n - 1] = nl
                desc += f" Na linha {n}, converti o resultado para texto com str()."
        return "\n".join(ls), desc
    if t == "TypeError" and "can only concatenate str" in msg:
        nl = _wrap_str_concat(line)
        if nl and nl != line:
            return _fix_line(code, n, nl), f"Linha {n}: converti os números para texto com str() antes de juntar."
    if t == "TypeError" and ("unsupported operand" in msg and "'str'" in msg or "not supported between instances of 'str'" in msg
                             or "'str' object cannot be interpreted as an integer" in msg):
        used = set(re.findall(r"\b([A-Za-z_]\w*)\b", line))
        ls = _lines(code)
        for i, l in enumerate(ls, 1):
            m = re.match(r"^(\s*)([A-Za-z_]\w*)\s*=\s*(input\(.*\))\s*$", _split_comment(l)[0])
            if m and m.group(2) in used and i <= n:
                ls[i - 1] = f"{m.group(1)}{m.group(2)} = int({m.group(3)})"
                return "\n".join(ls), f"Linha {i}: converti o input() para número com int()."
    if t == "AttributeError":
        m = re.search(r"'(\w+)' object has no attribute '(\w+)'", msg)
        if m and _JS.get(m.group(2)):
            nl = line.replace("." + m.group(2) + "(", "." + _JS[m.group(2)] + "(")
            if nl != line:
                return _fix_line(code, n, nl), f"Linha {n}: em Python o método se chama {_JS[m.group(2)]}()."
    return None, None


# ---------------------------------------------------------------- explicações
def _explain(info, code, all_names, entry):
    t, msg, n = info["tipo"], info["msg"], info["linha"]
    arq = info["arquivo"]
    em_outro = arq and arq not in (entry, "<stdin>")
    linha_txt = _line(code, n) if not em_outro else ""
    onde = f" (no arquivo {arq})" if em_outro else ""
    if t is None and "demorou demais" in msg:
        loops = [i for i, l in enumerate(_lines(code), 1) if re.match(r"\s*while\b", l)]
        ln = loops[0] if loops else None
        return _P(ln, _line(code, ln) if ln else "", "O programa não terminou",
                  "Ele rodou por tempo demais, o que quase sempre é um laço infinito: a condição do while nunca fica falsa.",
                  "Confira se alguma variável da condição muda dentro do laço (por exemplo contador += 1) ou se existe um break.")
    if t in ("SyntaxError", "IndentationError", "TabError"):
        base = {"titulo": "Erro de escrita (sintaxe)",
                "exp": "O Python nem começou a rodar: ele não entendeu como esta linha está escrita."}
        tips = [
            ("expected ':'", "Faltou o dois-pontos", "Linhas que abrem um bloco (if, elif, else, for, while, def, class, try) terminam com :.", "Coloque : no fim da linha."),
            ("Maybe you meant '=='", "= no lugar de ==", "Um = sozinho guarda um valor. Para comparar, use ==.", "Troque = por == na condição."),
            ("Missing parentheses in call to 'print'", "print sem parênteses", "No Python 3, print é uma função e sempre leva parênteses.", "Escreva print(...)."),
            ("unterminated string literal", "Aspas sem fechar", "Uma string começou com aspas e a linha acabou sem fechar.", "Feche com o mesmo tipo de aspas que abriu."),
            ("was never closed", "Parêntese (ou colchete) aberto", "Algo foi aberto e não foi fechado.", "Conte os ( ) [ ] { } da linha: cada um que abre precisa fechar."),
            ("unmatched", "Parêntese sobrando", "Tem um fechamento ) ] ou } sem a abertura correspondente.", "Apague o que sobrou ou abra o que falta."),
            ("expected an indented block", "Faltou recuar o bloco", "Depois de uma linha que termina com :, as linhas de dentro precisam de 4 espaços a mais.", "Recue a linha com 4 espaços (ou Tab)."),
            ("unexpected indent", "Recuo sem motivo", "A linha está mais para dentro do que deveria e não pertence a nenhum bloco.", "Alinhe a linha com as de cima."),
            ("unindent does not match", "Recuo desalinhado", "O recuo desta linha não bate com nenhum nível anterior.", "Use múltiplos de 4 espaços, sempre alinhados."),
            ("invalid character", "Caractere estranho", "Tem um símbolo que o Python não aceita, como aspas curvas “ ” copiadas de um texto.", "Digite as aspas e sinais direto no teclado."),
            ("inconsistent use of tabs", "Tabs e espaços misturados", "O recuo mistura Tab e espaços.", "Use só espaços (o editor do PyPasso já faz isso)."),
            ("invalid decimal literal", "Número colado em letras", "Nomes de variáveis não podem começar com número, e números não podem ter letras grudadas.", "Renomeie a variável (ex.: idade1 em vez de 1idade)."),
            ("cannot assign to", "Atribuição inválida", "O lado esquerdo do = precisa ser um nome de variável.", "Coloque a variável à esquerda: resultado = 2 + 3."),
        ]
        for key, tit, exp, como in tips:
            if key in msg:
                return _P(n, linha_txt, tit, exp, como, arq if em_outro else None)
        return _P(n, linha_txt, base["titulo"], base["exp"] + f" Detalhe do Python: {msg}.",
                  "Olhe esta linha e a de cima: faltou fechar algo ou sobrou algum símbolo?", arq if em_outro else None)
    if t == "NameError":
        m = re.search(r"name '(\w+)' is not defined", msg)
        bad = m.group(1) if m else "?"
        sug = re.search(r"Did you mean: '(\w+)'", msg)
        cand = sug.group(1) if sug else (difflib.get_close_matches(bad, list(all_names | _BUILTINS), n=1, cutoff=0.75) or [None])[0]
        como = f"Você quis dizer {cand}? Corrija o nome." if cand else \
            f"Crie a variável antes de usar (ex.: {bad} = ...) ou, se era um texto, coloque entre aspas: \"{bad}\"."
        return _P(n, linha_txt, f"O Python não conhece {bad}{onde}",
                  f"{bad} está sendo usado, mas nunca foi criado antes desta linha. Pode ser um erro de digitação, uma variável criada mais abaixo, ou um texto sem aspas.",
                  como, arq if em_outro else None)
    if t == "TypeError":
        iv = _input_vars(code, n) if not em_outro else {}
        used_iv = [v for v in re.findall(r"\b([A-Za-z_]\w*)\b", linha_txt) if v in iv]
        if used_iv and ("can only concatenate str" in msg or "'str'" in msg):
            v = used_iv[0]
            return _P(n, linha_txt, f"{v} é texto, não número",
                      f"{v} veio de um input() na linha {iv[v]}, e input() sempre devolve texto. Por isso a conta não funciona.",
                      f"Converta na hora de ler: {v} = int(input(...)).")
        if "can only concatenate str" in msg:
            return _P(n, linha_txt, "Juntando texto com número",
                      "O + só junta texto com texto. Aqui uma das partes é número, e o Python não converte sozinho.",
                      'Converta com str(numero), ou use f-string: f"Idade: {idade}".', arq if em_outro else None)
        if "unsupported operand" in msg and "'str'" in msg or "not supported between instances of 'str'" in msg:
            return _P(n, linha_txt, "Conta com texto",
                      "Você está fazendo uma conta (ou comparação) entre texto e número. Lembre: input() sempre devolve texto, mesmo que a pessoa digite um número.",
                      "Converta o valor com int(...) ou float(...) antes da conta.", arq if em_outro else None)
        if "'str' object cannot be interpreted as an integer" in msg:
            return _P(n, linha_txt, "Texto onde precisava de número inteiro",
                      "range() e índices precisam de int, mas recebeu texto (provavelmente vindo do input()).",
                      "Converta com int(...).", arq if em_outro else None)
        m = re.search(r"(\w+)\(\) (?:missing|takes) (.+)", msg)
        if m:
            return _P(n, linha_txt, f"Quantidade errada de argumentos em {m.group(1)}()",
                      f"A função foi chamada com argumentos diferentes do que ela espera ({m.group(2)}).",
                      "Compare a chamada com a linha def da função: cada parâmetro precisa de um valor.", arq if em_outro else None)
        if "object is not callable" in msg:
            return _P(n, linha_txt, "Chamando algo que não é função",
                      "Tem parênteses depois de algo que não é função. Às vezes uma variável foi criada com o nome de uma função, como list = [...] ou print = ...",
                      "Confira o nome antes dos parênteses e evite dar a variáveis nomes de funções do Python.", arq if em_outro else None)
        if "not subscriptable" in msg:
            return _P(n, linha_txt, "Usando [ ] em algo que não é lista",
                      "Colchetes servem para listas, strings, tuplas e dicionários. Este valor não é nenhum deles.",
                      "Confira o tipo do valor com print(type(valor)).", arq if em_outro else None)
        return _P(n, linha_txt, "Tipos que não combinam",
                  f"Uma operação recebeu um tipo de valor que ela não aceita. Detalhe do Python: {msg}.",
                  "Use print(type(valor)) para ver o tipo de cada valor envolvido.", arq if em_outro else None)
    if t == "ZeroDivisionError":
        return _P(n, linha_txt, "Divisão por zero", "Não existe divisão por zero em matemática nem em Python.",
                  "Verifique antes: if divisor != 0: ... ou trate com try/except ZeroDivisionError.", arq if em_outro else None)
    if t == "IndexError":
        return _P(n, linha_txt, "Posição que não existe",
                  "Você pediu um índice fora da lista ou string. Lembre que os índices começam em 0: numa lista de 3 itens, vão de 0 a 2.",
                  "Use len(lista) para saber o tamanho, ou lista[-1] para o último item.", arq if em_outro else None)
    if t == "KeyError":
        return _P(n, linha_txt, f"Chave {msg} não existe no dicionário",
                  "Você buscou uma chave que não está no dicionário.",
                  f"Use dic.get({msg}) para receber None em vez de erro, ou teste antes: if {msg} in dic:", arq if em_outro else None)
    if t == "ValueError":
        if "invalid literal for int()" in msg or "could not convert string to float" in msg:
            return _P(n, linha_txt, "Texto que não é número",
                      "int() e float() só convertem textos que parecem números, como \"42\". Outros textos dão erro.",
                      "Confira o valor digitado ou proteja com try/except ValueError.", arq if em_outro else None)
        return _P(n, linha_txt, "Valor inválido", f"O tipo está certo, mas o valor não serve aqui. Detalhe: {msg}.",
                  "Imprima o valor com print() antes desta linha para ver o que chegou.", arq if em_outro else None)
    if t == "AttributeError":
        m = re.search(r"'(\w+)' object has no attribute '(\w+)'", msg)
        if m:
            tipo, attr = m.groups()
            dica = _JS.get(attr)
            if attr in ("length", "size") or attr == "includes":
                como = "Em Python o tamanho é len(valor), e para ver se contém algo use: item in valor."
            elif dica:
                como = f"Em Python o método se chama {dica}()."
            else:
                sug = re.search(r"Did you mean: '(\w+)'", msg)
                como = f"Você quis dizer .{sug.group(1)}?" if sug else f"Veja o que existe com dir({tipo})."
            return _P(n, linha_txt, f"{tipo} não tem {attr}",
                      f"Valores do tipo {tipo} não têm .{attr}. Pode ser um nome trocado ou um costume de outra linguagem.",
                      como, arq if em_outro else None)
    if t == "EOFError":
        return _P(n, linha_txt, "Faltou resposta para o input()",
                  "O programa pediu um input() a mais do que as respostas escritas na caixa Entrada.",
                  "Abra a caixa Entrada e escreva uma resposta por linha, uma para cada input().", arq if em_outro else None)
    if t in ("ModuleNotFoundError", "ImportError"):
        return _P(n, linha_txt, "Módulo não encontrado",
                  "O PyPasso tem a biblioteca padrão do Python (math, random, datetime…). Módulos externos ou arquivos que você não criou não existem aqui.",
                  "Confira o nome. Para importar um arquivo seu, crie-o com o + nas abas (ex.: utils.py).", arq if em_outro else None)
    if t == "RecursionError":
        return _P(n, linha_txt, "A função chamou a si mesma sem parar",
                  "Uma função recursiva precisa de um caso base que encerre as chamadas.",
                  "Adicione um if que devolve um valor sem chamar a função de novo (ex.: if n == 0: return 1).", arq if em_outro else None)
    if t == "UnboundLocalError":
        return _P(n, linha_txt, "Variável usada antes de ganhar valor dentro da função",
                  "Dentro de uma função, se você atribui a uma variável, ela vira local, e não dá para usá-la antes dessa atribuição.",
                  "Passe o valor como parâmetro e devolva com return, em vez de mexer na variável de fora.", arq if em_outro else None)
    if t == "RuntimeError" and "input()" in msg:
        return _P(n, linha_txt, "input() não funciona aqui", msg, "Use valores fixos no código.", arq if em_outro else None)
    return _P(n, linha_txt, f"{t or 'Erro'}", f"O Python parou com este erro: {msg}.",
              "Leia a linha indicada e use print() antes dela para ver os valores.", arq if em_outro else None)


# ---------------------------------------------------------------- dicas de estilo
def _tips(code):
    out = []
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return out
    ls = _lines(code)
    loaded = {n.id for n in ast.walk(tree) if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load)}
    fstr_vars = set()
    for n in ast.walk(tree):
        if isinstance(n, ast.JoinedStr):
            for v in ast.walk(n):
                if isinstance(v, ast.Name):
                    fstr_vars.add(v.id)
    defined = _names_in(code)
    for n in ast.walk(tree):
        if isinstance(n, ast.Constant) and isinstance(n.value, str):
            fstr_vars.update(re.findall(r"\{([A-Za-z_]\w*)\}", n.value))

    def add(node_or_line, titulo, explicacao, antes=None, depois=None, bug=False):
        ln = node_or_line if isinstance(node_or_line, int) else getattr(node_or_line, "lineno", None)
        if any(t["titulo"] == titulo for t in out):
            return
        out.append({"linha": ln, "titulo": titulo, "explicacao": explicacao, "antes": antes, "depois": depois, "bug": bug})

    for node in ast.walk(tree):
        if isinstance(node, ast.Compare):
            for op, right in zip(node.ops, node.comparators):
                if isinstance(right, ast.Constant) and right.value is None and isinstance(op, (ast.Eq, ast.NotEq)):
                    add(node, "Compare com None usando is", "Para None, o jeito certo em Python é is None ou is not None.",
                        "x == None", "x is None")
                if isinstance(right, ast.Constant) and isinstance(right.value, bool) and isinstance(op, (ast.Eq, ast.NotEq)):
                    add(node, "Não precisa comparar com True/False", "A condição já é verdadeira ou falsa sozinha.",
                        "if ativo == True:", "if ativo:")
            if isinstance(node.left, ast.Call) and isinstance(node.left.func, ast.Name) and node.left.func.id == "type":
                add(node, "Prefira isinstance()", "isinstance(x, int) é o jeito idiomático de checar tipos.", "type(x) == int", "isinstance(x, int)")
            if isinstance(node.left, ast.Call) and isinstance(node.left.func, ast.Name) and node.left.func.id == "len" \
                    and len(node.comparators) == 1 and isinstance(node.comparators[0], ast.Constant) and node.comparators[0].value == 0:
                add(node, "Lista vazia é falsa", "Não precisa medir o tamanho para saber se está vazia.", "if len(lista) == 0:", "if not lista:")
        if isinstance(node, ast.BoolOp) and isinstance(node.op, ast.Or):
            if any(isinstance(v, ast.Constant) and not isinstance(v.value, bool) for v in node.values[1:]) and isinstance(node.values[0], ast.Compare):
                add(node, "Esta condição é sempre verdadeira", "x == 1 or 2 não testa se x é 1 ou 2: o 2 sozinho já conta como verdadeiro.",
                    "if x == 1 or 2:", "if x in (1, 2):", bug=True)
        if isinstance(node, ast.For) and isinstance(node.iter, ast.Call) and getattr(node.iter.func, "id", "") == "range" \
                and len(node.iter.args) == 1 and isinstance(node.iter.args[0], ast.Call) and getattr(node.iter.args[0].func, "id", "") == "len":
            add(node, "Percorra a lista direto", "Em Python dá para passar pelos itens sem índice. Se precisar do índice também, use enumerate().",
                "for i in range(len(nomes)):\n    print(nomes[i])", "for nome in nomes:\n    print(nome)")
        if isinstance(node, ast.ExceptHandler) and node.type is None:
            add(node, "Evite except sozinho", "Um except sem tipo esconde qualquer erro, até os que você não esperava.",
                "except:", "except ValueError:")
        if isinstance(node, (ast.FunctionDef,)):
            for d in node.args.defaults:
                if isinstance(d, (ast.List, ast.Dict, ast.Set)):
                    add(node, "Padrão mutável no parâmetro", "Uma lista como valor padrão é compartilhada entre chamadas e acumula itens.",
                        "def f(itens=[]):", "def f(itens=None):\n    if itens is None:\n        itens = []", bug=True)
        if isinstance(node, ast.While) and isinstance(node.test, ast.Constant) and node.test.value is True:
            if not any(isinstance(x, (ast.Break, ast.Return)) for x in ast.walk(node)):
                add(node, "while True sem break", "Este laço não tem como terminar.", None, None, bug=True)
        if isinstance(node, (ast.Assign,)):
            for tgt in node.targets:
                if isinstance(tgt, ast.Name):
                    if tgt.id in _SHADOW:
                        add(node, f"Evite chamar a variável de {tgt.id}", f"{tgt.id} já é uma função do Python; usando esse nome você perde acesso a ela.",
                            f"{tgt.id} = ...", f"meu_{tgt.id} = ...")
                    elif re.match(r"^[a-z]+[A-Z]\w*$", tgt.id):
                        snake = re.sub(r"([A-Z])", lambda m: "_" + m.group(1).lower(), tgt.id)
                        add(node, "Nomes no estilo Python", "Em Python, variáveis usam letras minúsculas separadas por _ (snake_case).",
                            tgt.id, snake)
                    if isinstance(node.value, ast.BinOp) and isinstance(node.value.left, ast.Name) and node.value.left.id == tgt.id \
                            and isinstance(node.value.op, (ast.Add, ast.Sub, ast.Mult)):
                        sym = {ast.Add: "+", ast.Sub: "-", ast.Mult: "*"}[type(node.value.op)]
                        add(node, f"Use {sym}=", "Existe um atalho para atualizar a própria variável.",
                            f"{tgt.id} = {tgt.id} {sym} 1", f"{tgt.id} {sym}= 1")
        if isinstance(node, ast.Call) and getattr(node.func, "id", "") == "print":
            for a in node.args:
                if isinstance(a, ast.BinOp) and isinstance(a.op, ast.Add):
                    segs = ast.get_source_segment(code, a) or ""
                    if "str(" in segs or re.search(r"""["']\s*\+|\+\s*["']""", segs):
                        add(node, "Use f-string", "Juntar textos com + e str() funciona, mas a f-string é mais curta e legível.",
                            'print("Olá, " + nome + "! Idade: " + str(idade))', 'print(f"Olá, {nome}! Idade: {idade}")')
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            inside = re.findall(r"\{([A-Za-z_]\w*)\}", node.value)
            if inside and all(v in defined for v in inside):
                add(node, "Faltou o f da f-string?", f"O texto tem {{{inside[0]}}}, mas sem f antes das aspas as chaves aparecem literalmente.",
                    f'print("Oi, {{{inside[0]}}}")', f'print(f"Oi, {{{inside[0]}}}")', bug=True)
    # variáveis criadas e nunca usadas (só no nível de cima)
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            name = node.targets[0].id
            if name not in loaded and not name.startswith("_") and name not in fstr_vars:
                add(node, f"{name} nunca é usada", "A variável é criada, mas nada no código lê o valor dela. Talvez falte usá-la, ou ela possa ser apagada.")
    for i, l in enumerate(ls, 1):
        if len(l) > 99:
            add(i, "Linha muito longa", "Linhas curtas (até ~80 caracteres) são mais fáceis de ler. Quebre em partes ou crie variáveis intermediárias.")
        ind = _indent(l)
        if l.strip() and ind % 4:
            add(i, "Recuo fora do padrão", "O padrão do Python é recuar de 4 em 4 espaços.")
    out.sort(key=lambda t: (not t["bug"], t["linha"] or 0))
    return out[:6]


def _style_fixes(code):
    """Melhorias seguras, linha a linha (e o f esquecido em f-strings)."""
    changes = []
    ls = _lines(code)
    defined = _names_in(code)

    def add_f(m):
        if m.group(1):
            return m.group(0)
        names = re.findall(r"\{([A-Za-z_]\w*)(?:[!:][^}]*)?\}", m.group(3))
        if names and all(x in defined for x in names):
            return "f" + m.group(2) + m.group(3) + m.group(2)
        return m.group(0)

    for i, l in enumerate(ls):
        body, com = _split_comment(l)
        sp = " " + com if com else ""
        nb = re.sub(r"""([A-Za-z_])?(["'])((?:(?!\2).)*\{[A-Za-z_]\w*(?:[!:][^}]*)?\}(?:(?!\2).)*)\2""", add_f, body)
        nb = re.sub(r"(\w|\))\s*==\s*None\b", r"\1 is None", nb)
        nb = re.sub(r"(\w|\))\s*!=\s*None\b", r"\1 is not None", nb)
        m = re.match(r"^(\s*)(if|elif|while)\s+(.+?)\s*==\s*True\s*:$", nb)
        if m:
            nb = f"{m.group(1)}{m.group(2)} {m.group(3)}:"
        m = re.match(r"^(\s*)(if|elif|while)\s+(.+?)\s*==\s*False\s*:$", nb)
        if m and " " not in m.group(3).strip():
            nb = f"{m.group(1)}{m.group(2)} not {m.group(3)}:"
        m = re.match(r"^(\s*)([A-Za-z_]\w*)\s*=\s*\2\s*([+\-*])\s*(.+)$", nb)
        if m and not re.search(r"[+\-*/%<>=]", m.group(4).replace("**", "")) or (m and re.match(r"^[\w.()\[\]\"' ]+$", m.group(4))):
            nb = f"{m.group(1)}{m.group(2)} {m.group(3)}= {m.group(4)}"
        if nb != body:
            ls[i] = nb + sp
            changes.append(f"Linha {i + 1}: {body.strip()}  →  {nb.strip()}")
    new = "\n".join(ls)
    try:
        ast.parse(new)
    except SyntaxError:
        return code, []
    return new, changes


def __pypasso_analyze(files_json, entry, error_text):
    files = json.loads(files_json)
    code = files.get(entry, "")
    all_names = set()
    for src in files.values():
        all_names |= _names_in(src)
    info = _parse_error(error_text, entry)
    problemas, mudancas = [], []
    fixed = code

    if info:
        problemas.append(_explain(info, code, all_names, entry))
        # Correções: primeiro o erro de execução, depois rodadas de sintaxe
        if info["tipo"] not in ("SyntaxError", "IndentationError", "TabError") and info["arquivo"] in (entry,):
            nc, desc = _fix_runtime(fixed, info, all_names)
            if nc:
                fixed, mudancas = nc, [desc]
    for _ in range(5):
        try:
            compile(fixed, entry, "exec")
            break
        except SyntaxError as e:
            nc, desc = _fix_syntax(fixed, e)
            if not nc or nc == fixed:
                break
            fixed = nc
            mudancas.append(desc)
    try:
        compile(fixed, entry, "exec")
        ok_syntax = True
    except SyntaxError:
        ok_syntax = False
    if ok_syntax:
        fixed2, ch = _style_fixes(fixed)
        if ch:
            fixed = fixed2
            mudancas += ["Melhoria: " + c for c in ch]
    try:
        ast.parse(code)
        dicas = _tips(code)
    except SyntaxError:
        dicas = _tips(fixed) if ok_syntax else []
    if info:
        n = problemas[0]["linha"]
        arq = problemas[0].get("arquivo")
        titulo = (f"Achei o problema na linha {n} de {arq}!" if arq else f"Achei o problema na linha {n}!") if n else "Achei o problema!"
        humor = "sad"
    elif any(d.get("bug") for d in dicas):
        titulo = "Rodou, mas acho que tem um erro escondido."
        humor = "think"
    elif dicas:
        titulo = "Funcionou! E dá para deixar ainda melhor."
        humor = "think"
    else:
        titulo = "Código limpo! Não achei nada para corrigir."
        humor = "cheer"
    return json.dumps({
        "titulo": titulo, "humor": humor, "problemas": problemas, "dicas": dicas,
        "corrigido": fixed if fixed != code and ok_syntax else None,
        "mudancas": mudancas if fixed != code and ok_syntax else [],
    }, ensure_ascii=False)


def __pypasso_syntax(code):
    try:
        compile(code, "codigo.py", "exec")
        return json.dumps({"ok": True, "stdout": "", "error": None})
    except SyntaxError as e:
        return json.dumps({"ok": False, "stdout": "", "error": f"linha {e.lineno}: {e.msg}"})

`;
