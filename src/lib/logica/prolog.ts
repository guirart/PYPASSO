/**
 * Um Prolog pequeno, feito para ensinar: fatos, regras, consultas, listas, aritmética, corte (!), negação (\+),
 * se-então-senão, findall/forall/between, assert/retract e format. Não tem módulos nem restrições (clp), mas roda
 * os programas clássicos de aula (família, listas, filmes, rainhas...). Arquivo puro, sem telas nem imagens.
 */
export class ErroProlog extends Error {}

// ---------------------------------------------------------------- termos
type Atomo = { k: 'a'; n: string };
type Numero = { k: 'n'; v: number };
type Variavel = { k: 'v'; nome: string; id: number; ref: Termo | null };
type Composto = { k: 'c'; f: string; args: Termo[] };
export type Termo = Atomo | Numero | Variavel | Composto;

let contadorVar = 0;
const novaVar = (nome = '_'): Variavel => ({ k: 'v', nome, id: ++contadorVar, ref: null });
const atomo = (n: string): Atomo => ({ k: 'a', n });
const num = (v: number): Numero => ({ k: 'n', v });
const comp = (f: string, ...args: Termo[]): Composto => ({ k: 'c', f, args });
const NIL = atomo('[]');
const cons = (h: Termo, t: Termo) => comp('.', h, t);
const lista = (xs: Termo[], cauda: Termo = NIL): Termo => xs.reduceRight((t, h) => cons(h, t), cauda);

function deref(t: Termo): Termo { while (t.k === 'v' && t.ref) t = t.ref; return t; }

/** Lista de termos de uma lista Prolog completa; null se não for lista (ou se ficar aberta). */
function paraArray(t: Termo): Termo[] | null {
  const out: Termo[] = [];
  let x = deref(t);
  while (x.k === 'c' && x.f === '.' && x.args.length === 2) { out.push(x.args[0]); x = deref(x.args[1]); }
  return x.k === 'a' && x.n === '[]' ? out : null;
}

// ---------------------------------------------------------------- operadores
type Op = { p: number; tipo: 'xfx' | 'xfy' | 'yfx' };
const INFIXOS: Record<string, Op> = {
  ':-': { p: 1200, tipo: 'xfx' }, '-->': { p: 1200, tipo: 'xfx' },
  ';': { p: 1100, tipo: 'xfy' }, '|': { p: 1100, tipo: 'xfy' }, '->': { p: 1050, tipo: 'xfy' }, '*->': { p: 1050, tipo: 'xfy' },
  ',': { p: 1000, tipo: 'xfy' },
  '=': { p: 700, tipo: 'xfx' }, '\\=': { p: 700, tipo: 'xfx' }, '==': { p: 700, tipo: 'xfx' }, '\\==': { p: 700, tipo: 'xfx' },
  '@<': { p: 700, tipo: 'xfx' }, '@>': { p: 700, tipo: 'xfx' }, '@=<': { p: 700, tipo: 'xfx' }, '@>=': { p: 700, tipo: 'xfx' },
  '<': { p: 700, tipo: 'xfx' }, '>': { p: 700, tipo: 'xfx' }, '=<': { p: 700, tipo: 'xfx' }, '>=': { p: 700, tipo: 'xfx' },
  '=:=': { p: 700, tipo: 'xfx' }, '=\\=': { p: 700, tipo: 'xfx' }, 'is': { p: 700, tipo: 'xfx' }, '=..': { p: 700, tipo: 'xfx' },
  '+': { p: 500, tipo: 'yfx' }, '-': { p: 500, tipo: 'yfx' },
  '*': { p: 400, tipo: 'yfx' }, '/': { p: 400, tipo: 'yfx' }, '//': { p: 400, tipo: 'yfx' }, 'mod': { p: 400, tipo: 'yfx' }, 'rem': { p: 400, tipo: 'yfx' },
  '**': { p: 200, tipo: 'xfx' }, '^': { p: 200, tipo: 'xfy' },
};
const PREFIXOS: Record<string, { p: number; tipo: 'fy' | 'fx' }> = {
  'dynamic': { p: 1150, tipo: 'fx' }, 'discontiguous': { p: 1150, tipo: 'fx' }, ':-': { p: 1200, tipo: 'fx' }, '?-': { p: 1200, tipo: 'fx' }, '\\+': { p: 900, tipo: 'fy' }, '-': { p: 200, tipo: 'fy' }, '+': { p: 200, tipo: 'fy' }, '\\': { p: 200, tipo: 'fy' },
};

// ---------------------------------------------------------------- leitura (lexer + parser)
type Tok = { t: 'atom' | 'qatom' | 'var' | 'num' | 'str' | 'punct' | 'fim'; v: string; n?: number; abre?: boolean; linha: number };
const SIMBOLOS = '+-*/\\^<>=~:.?@#&$';

function lexer(src: string): Tok[] {
  const toks: Tok[] = [];
  let i = 0, linha = 1;
  const erro = (m: string): never => { throw new ErroProlog(`Erro de sintaxe na linha ${linha}: ${m}`); };
  while (i < src.length) {
    const c = src[i];
    if (c === '\n') { linha++; i++; continue; }
    if (/\s/.test(c)) { i++; continue; }
    if (c === '%') { while (i < src.length && src[i] !== '\n') i++; continue; }
    if (c === '/' && src[i + 1] === '*') { const f = src.indexOf('*/', i + 2); const trecho = src.slice(i, f < 0 ? src.length : f + 2); linha += (trecho.match(/\n/g) ?? []).length; i = f < 0 ? src.length : f + 2; continue; }
    // número
    if (/[0-9]/.test(c)) {
      const m = /^[0-9]+(\.[0-9]+)?([eE][+-]?[0-9]+)?/.exec(src.slice(i))!;
      toks.push({ t: 'num', v: m[0], n: Number(m[0]), linha }); i += m[0].length; continue;
    }
    // variável
    if (/[A-Z_]/.test(c)) {
      const m = /^[A-Za-z0-9_À-ÿ]+/.exec(src.slice(i))!;
      toks.push({ t: 'var', v: m[0], linha }); i += m[0].length; continue;
    }
    // átomo alfanumérico
    if (/[a-zà-ÿ]/.test(c)) {
      const m = /^[A-Za-z0-9_À-ÿ]+/.exec(src.slice(i))!;
      toks.push({ t: 'atom', v: m[0], abre: src[i + m[0].length] === '(', linha }); i += m[0].length; continue;
    }
    // átomo ou texto entre aspas
    if (c === "'" || c === '"') {
      let j = i + 1, s = '';
      while (j < src.length && src[j] !== c) {
        if (src[j] === '\\' && j + 1 < src.length) { const e = src[j + 1]; s += e === 'n' ? '\n' : e === 't' ? '\t' : e; j += 2; continue; }
        if (src[j] === '\n') linha++;
        s += src[j++];
      }
      if (j >= src.length) erro('aspas sem fechar');
      toks.push({ t: c === "'" ? 'qatom' : 'str', v: s, abre: src[j + 1] === '(', linha }); i = j + 1; continue;
    }
    if ('()[]{},|;!'.includes(c)) {
      if (c === '!' || c === ';') toks.push({ t: 'atom', v: c, abre: src[i + 1] === '(', linha });
      else toks.push({ t: 'punct', v: c, linha });
      i++; continue;
    }
    if (SIMBOLOS.includes(c)) {
      // o ponto final: "." seguido de espaço, fim ou %
      if (c === '.' && (i + 1 >= src.length || /\s|%/.test(src[i + 1]))) { toks.push({ t: 'fim', v: '.', linha }); i++; continue; }
      let j = i;
      while (j < src.length && SIMBOLOS.includes(src[j])) j++;
      const v = src.slice(i, j);
      toks.push({ t: 'atom', v, abre: src[j] === '(', linha }); i = j; continue;
    }
    erro(`símbolo inesperado "${c}"`);
  }
  return toks;
}

class Leitor {
  p = 0;
  mapaVars = new Map<string, Variavel>();
  constructor(private ts: Tok[]) {}
  get fimDoTexto() { return this.p >= this.ts.length; }
  private olha(): Tok | undefined { return this.ts[this.p]; }
  private erro(m: string): never { const t = this.ts[Math.min(this.p, this.ts.length - 1)]; throw new ErroProlog(`Erro de sintaxe${t ? ` na linha ${t.linha}` : ''}: ${m}`); }

  /** Lê uma cláusula (até o ponto final). Devolve null no fim do texto. */
  lerClausula(exigePonto = true): Termo | null {
    if (this.fimDoTexto) return null;
    this.mapaVars = new Map();
    const t = this.termo(1200);
    const f = this.olha();
    if (f?.t === 'fim') this.p++;
    else if (exigePonto) this.erro('faltou o ponto final "." no fim da cláusula');
    return t;
  }

  /** Salta até depois do próximo ponto final (recuperação depois de um erro). */
  pulaClausula() { while (this.p < this.ts.length && this.ts[this.p].t !== 'fim') this.p++; this.p++; }

  private ehInicioDeTermo(t?: Tok): boolean {
    if (!t) return false;
    if (t.t === 'fim') return false;
    if (t.t === 'punct') return t.v === '(' || t.v === '[' || t.v === '{';
    if (t.t === 'atom' && INFIXOS[t.v] && !PREFIXOS[t.v] && !t.abre) return false;
    return true;
  }

  termo(max: number): Termo {
    let [esq, pe] = this.primario(max);
    for (;;) {
      const t = this.olha();
      if (!t) break;
      let nome: string | null = null;
      if (t.t === 'atom' && INFIXOS[t.v]) nome = t.v;
      else if (t.t === 'punct' && (t.v === ',' || t.v === '|')) nome = t.v;
      if (!nome) break;
      const op = INFIXOS[nome];
      if (op.p > max) break;
      const maxEsq = op.tipo === 'yfx' ? op.p : op.p - 1;
      if (pe > maxEsq) break;
      this.p++;
      const maxDir = op.tipo === 'xfy' ? op.p : op.p - 1;
      const dir = this.termo(maxDir);
      esq = comp(nome === '|' ? ';' : nome, esq, dir);
      pe = op.p;
    }
    return esq;
  }

  private primario(max: number): [Termo, number] {
    const t = this.olha();
    if (!t) return this.erro('a consulta terminou antes da hora');
    this.p++;
    switch (t.t) {
      case 'num': return [num(t.n!), 0];
      case 'var': {
        if (t.v === '_') return [novaVar('_'), 0];
        let v = this.mapaVars.get(t.v);
        if (!v) { v = novaVar(t.v); this.mapaVars.set(t.v, v); }
        return [v, 0];
      }
      case 'str': return [atomo(t.v), 0];
      case 'punct': {
        if (t.v === '(') { const x = this.termo(1200); this.esperar(')'); return [x, 0]; }
        if (t.v === '[') {
          if (this.olha()?.t === 'punct' && this.olha()!.v === ']') { this.p++; return [NIL, 0]; }
          const itens: Termo[] = [this.termo(999)];
          let cauda: Termo = NIL;
          for (;;) {
            const n = this.olha();
            if (n?.t === 'punct' && n.v === ',') { this.p++; itens.push(this.termo(999)); continue; }
            if (n?.t === 'punct' && n.v === '|') { this.p++; cauda = this.termo(999); break; }
            break;
          }
          this.esperar(']');
          return [lista(itens, cauda), 0];
        }
        if (t.v === '{') { if (this.olha()?.v === '}') { this.p++; return [atomo('{}'), 0]; } const x = this.termo(1200); this.esperar('}'); return [comp('{}', x), 0]; }
        return this.erro(`"${t.v}" aqui não faz sentido`);
      }
      case 'fim': return this.erro('o ponto final apareceu cedo demais');
      case 'atom': case 'qatom': {
        if (t.abre) { // nome(args)
          this.p++; // "("
          const args: Termo[] = [this.termo(999)];
          while (this.olha()?.t === 'punct' && this.olha()!.v === ',') { this.p++; args.push(this.termo(999)); }
          this.esperar(')');
          return [comp(t.v, ...args), 0];
        }
        // número negativo: "-" colado num número
        if (t.t === 'atom' && t.v === '-' && this.olha()?.t === 'num') { const n = this.olha()!; this.p++; return [num(-n.n!), 0]; }
        const pre = t.t === 'atom' ? PREFIXOS[t.v] : undefined;
        if (pre && this.ehInicioDeTermo(this.olha())) {
          let p = pre.p; if (p > max) p = 999;
          const arg = this.termo(pre.tipo === 'fy' ? p : p - 1);
          return [comp(t.v, arg), p];
        }
        // operador usado como átomo simples (ex.: X = (+))
        const pe = t.t === 'atom' && (INFIXOS[t.v] || PREFIXOS[t.v]) ? 0 : 0;
        return [atomo(t.v), pe];
      }
    }
  }

  private esperar(v: string) {
    const t = this.olha();
    if (t?.t === 'punct' && t.v === v) { this.p++; return; }
    this.erro(`faltou "${v}"`);
  }
}

// ---------------------------------------------------------------- escrita de termos
const ATOMO_SIMPLES = /^[a-zà-ÿ][A-Za-z0-9_À-ÿ]*$/;
function textoAtomo(n: string, aspas: boolean): string {
  if (!aspas) return n;
  if (ATOMO_SIMPLES.test(n) || n === '[]' || n === '!' || n === ';' || n === ',' || n === '{}' || (n.length > 0 && [...n].every((c) => SIMBOLOS.includes(c)))) return n;
  return `'${n.replace(/\\/g, '\\\\').replace(/'/g, "\\'")}'`;
}
export function mostrarTermo(t0: Termo, aspas = true, max = 1200): string {
  const t = deref(t0);
  if (t.k === 'n') return Number.isInteger(t.v) ? String(t.v) : String(t.v);
  if (t.k === 'a') return textoAtomo(t.n, aspas);
  if (t.k === 'v') return `_G${t.id}`;
  if (t.f === '.' && t.args.length === 2) {
    const itens: string[] = [];
    let x: Termo = t;
    while (x.k === 'c' && x.f === '.' && x.args.length === 2) { itens.push(mostrarTermo(x.args[0], aspas, 999)); x = deref(x.args[1]); }
    if (x.k === 'a' && x.n === '[]') return `[${itens.join(',')}]`;
    return `[${itens.join(',')}|${mostrarTermo(x, aspas, 999)}]`;
  }
  if (t.args.length === 2 && INFIXOS[t.f]) {
    const op = INFIXOS[t.f];
    const e = mostrarTermo(t.args[0], aspas, op.tipo === 'yfx' ? op.p : op.p - 1);
    const d = mostrarTermo(t.args[1], aspas, op.tipo === 'xfy' ? op.p : op.p - 1);
    const s = t.f === ',' ? `${e},${d}` : /^[a-z]/.test(t.f) || t.f === '->' || t.f === ':-' ? `${e} ${t.f} ${d}` : `${e}${t.f}${d}`;
    return op.p > max ? `(${s})` : s;
  }
  if (t.args.length === 1 && PREFIXOS[t.f]) {
    const s = `${t.f}${/^[a-z]/.test(t.f) ? ' ' : ''}${mostrarTermo(t.args[0], aspas, PREFIXOS[t.f].p)}`;
    return PREFIXOS[t.f].p > max ? `(${s})` : s;
  }
  return `${textoAtomo(t.f, aspas)}(${t.args.map((a) => mostrarTermo(a, aspas, 999)).join(',')})`;
}

// ---------------------------------------------------------------- a máquina
type Clausula = { cabeca: Termo; corpo: Termo };
type Ctx = { cortou: boolean };
type Resultado = { solucoes: Record<string, string>[]; saida: string; mais: boolean };

const PRELUDIO = `
append([], L, L).
append([H|T], L, [H|R]) :- append(T, L, R).
member(X, [X|_]).
member(X, [_|T]) :- member(X, T).
memberchk(X, L) :- member(X, L), !.
reverse(L, R) :- reverse_(L, [], R).
reverse_([], A, A).
reverse_([H|T], A, R) :- reverse_(T, [H|A], R).
nth0(I, L, E) :- nth_(L, 0, I, E).
nth1(I, L, E) :- nth_(L, 1, I, E).
nth_([H|_], B, B, H).
nth_([_|T], B0, I, E) :- B1 is B0+1, nth_(T, B1, I, E).
last([X], X).
last([_|T], X) :- last(T, X).
select(X, [X|T], T).
select(X, [H|T], [H|R]) :- select(X, T, R).
selectchk(X, L, R) :- select(X, L, R), !.
permutation([], []).
permutation(L, [H|T]) :- select(H, L, R), permutation(R, T).
delete([], _, []).
delete([H|T], X, R) :- ( H = X -> delete(T, X, R) ; R = [H|R1], delete(T, X, R1) ).
exclude(_, [], []).
exclude(G, [H|T], R) :- ( call(G, H) -> R = R1 ; R = [H|R1] ), exclude(G, T, R1).
include(_, [], []).
include(G, [H|T], R) :- ( call(G, H) -> R = [H|R1] ; R = R1 ), include(G, T, R1).
maplist(_, []).
maplist(G, [A|As]) :- call(G, A), maplist(G, As).
maplist(_, [], []).
maplist(G, [A|As], [B|Bs]) :- call(G, A, B), maplist(G, As, Bs).
maplist(_, [], [], []).
maplist(G, [A|As], [B|Bs], [C|Cs]) :- call(G, A, B, C), maplist(G, As, Bs, Cs).
foldl(G, L, A0, A) :- foldl_(L, G, A0, A).
foldl_([], _, A, A).
foldl_([X|Xs], G, A0, A) :- call(G, X, A0, A1), foldl_(Xs, G, A1, A).
sum_list(L, S) :- sum_list_(L, 0, S).
sum_list_([], S, S).
sum_list_([H|T], A, S) :- A1 is A+H, sum_list_(T, A1, S).
sumlist(L, S) :- sum_list(L, S).
max_list([H|T], M) :- foldl_max_(T, H, M).
foldl_max_([], M, M).
foldl_max_([H|T], A, M) :- A1 is max(A, H), foldl_max_(T, A1, M).
min_list([H|T], M) :- foldl_min_(T, H, M).
foldl_min_([], M, M).
foldl_min_([H|T], A, M) :- A1 is min(A, H), foldl_min_(T, A1, M).
numlist(L, H, []) :- L > H, !.
numlist(L, H, [L|T]) :- L1 is L+1, numlist(L1, H, T).
list_to_set(L, S) :- lts_(L, [], S).
lts_([], _, []).
lts_([H|T], V, R) :- ( memberchk(H, V) -> R = R1 ; R = [H|R1] ), lts_(T, [H|V], R1).
subtract([], _, []).
subtract([H|T], L, R) :- ( memberchk(H, L) -> R = R1 ; R = [H|R1] ), subtract(T, L, R1).
intersection([], _, []).
intersection([H|T], L, R) :- ( memberchk(H, L) -> R = [H|R1] ; R = R1 ), intersection(T, L, R1).
union([], L, L).
union([H|T], L, R) :- ( memberchk(H, L) -> R = R1 ; R = [H|R1] ), union(T, L, R1).
exclude_one_(_, [], []).
flatten([], []) :- !.
flatten([H|T], F) :- !, flatten(H, FH), flatten(T, FT), append(FH, FT, F).
flatten(X, [X]).
sumlist_(L, S) :- sum_list(L, S).
prefix(P, L) :- append(P, _, L).
suffix(S, L) :- append(_, S, L).
sublist_(S, L) :- suffix(X, L), prefix(S, X).
last_([X], X).
once(G) :- call(G), !.
ignore(G) :- ( call(G) -> true ; true ).
not(G) :- \\+ call(G).
forall(C, A) :- \\+ ( call(C), \\+ call(A) ).
`;

const MAX_PASSOS = 400000;
const MAX_PROFUNDIDADE = 100000;

export class Prolog {
  private db = new Map<string, Clausula[]>();
  private biblioteca = new Set<string>(); // chaves definidas pelo prelúdio (o programa pode substituí-las)
  private dinamicos = new Set<string>();
  private trilha: Variavel[] = [];
  private saida = '';
  private passos = 0;
  private profundidade = 0;
  private ops = INFIXOS;

  constructor() { this.carregar(PRELUDIO, true); }

  // ---- banco de dados
  private chave(t: Termo): string {
    const d = deref(t);
    if (d.k === 'a') return `${d.n}/0`;
    if (d.k === 'c') return `${d.f}/${d.args.length}`;
    throw new ErroProlog('Isso não é um fato nem uma regra.');
  }

  private adicionar(t: Termo, fim = true, lib = false) {
    let cab = deref(t), corpo: Termo = atomo('true');
    if (cab.k === 'c' && cab.f === ':-' && cab.args.length === 2) { corpo = cab.args[1]; cab = deref(cab.args[0]); }
    if (cab.k === 'v') throw new ErroProlog('A cabeça de uma regra não pode ser uma variável.');
    const k = this.chave(cab);
    if (['=/2', ',/2', ';/2', '->/2', 'is/2', '!/0'].includes(k)) throw new ErroProlog(`Não dá para redefinir ${k}.`);
    if (!lib && this.biblioteca.has(k)) { this.db.delete(k); this.biblioteca.delete(k); } // o programa substitui o da biblioteca
    if (lib) this.biblioteca.add(k);
    const lista = this.db.get(k) ?? [];
    const c = this.copiarResolvido({ k: 'c', f: ':-', args: [cab, corpo] } as Composto) as Composto;
    const cl = { cabeca: c.args[0], corpo: c.args[1] };
    if (fim) lista.push(cl); else lista.unshift(cl);
    this.db.set(k, lista);
  }

  /** Lê um programa (fatos, regras e diretivas). Devolve os erros de sintaxe encontrados, sem parar no primeiro. */
  carregar(texto: string, lib = false): string[] {
    const erros: string[] = [];
    let leitor: Leitor;
    try { leitor = new Leitor(lexer(texto)); } catch (e) { return [(e as Error).message]; }
    while (!leitor.fimDoTexto) {
      try {
        const t = leitor.lerClausula();
        if (!t) break;
        const d = deref(t);
        if (d.k === 'c' && d.f === ':-' && d.args.length === 1) { this.diretiva(d.args[0]); continue; }
        this.adicionar(d, true, lib);
      } catch (e) {
        erros.push((e as Error).message);
        if (e instanceof ErroProlog && /sintaxe/.test(e.message)) leitor.pulaClausula();
      }
    }
    return erros;
  }

  private diretiva(g: Termo) {
    const d = deref(g);
    if (d.k === 'c' && (d.f === 'dynamic' || d.f === 'discontiguous') && d.args.length === 1) {
      if (d.f === 'dynamic') this.declararDinamicos(d.args[0]);
      return;
    }
    // outras diretivas (ex.: :- initialization(main).) são ignoradas; uma consulta comum roda
    if (d.k === 'c' && d.f === 'initialization') return;
    try { for (const _ of this.resolver(d, { cortou: false })) { break; } } catch { /* diretivas com erro não derrubam o programa */ }
  }
  private declararDinamicos(t: Termo) {
    const d = deref(t);
    if (d.k === 'c' && (d.f === ',' || d.f === '/')) {
      if (d.f === ',') { this.declararDinamicos(d.args[0]); this.declararDinamicos(d.args[1]); return; }
      const n = deref(d.args[0]), a = deref(d.args[1]);
      if (n.k === 'a' && a.k === 'n') { const k = `${n.n}/${a.v}`; this.dinamicos.add(k); if (!this.db.has(k)) this.db.set(k, []); }
    }
  }

  limpar() { this.db.clear(); this.dinamicos.clear(); this.biblioteca.clear(); this.carregar(PRELUDIO, true); }

  // ---- unificação
  private ligar(v: Variavel, t: Termo) { v.ref = t; this.trilha.push(v); }
  private desfazer(marca: number) { while (this.trilha.length > marca) this.trilha.pop()!.ref = null; }
  private unificar(a0: Termo, b0: Termo): boolean {
    const a = deref(a0), b = deref(b0);
    if (a === b) return true;
    if (a.k === 'v') { this.ligar(a, b); return true; }
    if (b.k === 'v') { this.ligar(b, a); return true; }
    if (a.k === 'a' && b.k === 'a') return a.n === b.n;
    if (a.k === 'n' && b.k === 'n') return a.v === b.v;
    if (a.k === 'c' && b.k === 'c') {
      if (a.f !== b.f || a.args.length !== b.args.length) return false;
      for (let i = 0; i < a.args.length; i++) if (!this.unificar(a.args[i], b.args[i])) return false;
      return true;
    }
    return false;
  }

  /** Cópia com variáveis novas (renomear) e com as ligações atuais já aplicadas. */
  private copiarResolvido(t0: Termo, mapa = new Map<number, Variavel>()): Termo {
    const t = deref(t0);
    if (t.k === 'v') { let n = mapa.get(t.id); if (!n) { n = novaVar(t.nome); mapa.set(t.id, n); } return n; }
    if (t.k === 'c') return { k: 'c', f: t.f, args: t.args.map((a) => this.copiarResolvido(a, mapa)) };
    return t;
  }

  private passo() { if (++this.passos > MAX_PASSOS) throw new ErroProlog('Passos demais: o programa pode estar em um laço infinito.'); }

  // ---- aritmética
  private calc(t0: Termo): number {
    const t = deref(t0);
    if (t.k === 'n') return t.v;
    if (t.k === 'v') throw new ErroProlog('Falta um valor: há uma variável sem valor na conta.');
    if (t.k === 'a') {
      if (t.n === 'pi') return Math.PI; if (t.n === 'e') return Math.E; if (t.n === 'inf' || t.n === 'infinite') return Infinity;
      throw new ErroProlog(`"${t.n}" não é um número.`);
    }
    const a = t.args.map((x) => this.calc(x));
    const f = t.f;
    if (a.length === 2) {
      const [x, y] = a;
      switch (f) {
        case '+': return x + y; case '-': return x - y; case '*': return x * y;
        case '/': if (y === 0) throw new ErroProlog('Divisão por zero.'); return Number.isInteger(x) && Number.isInteger(y) && x % y === 0 ? x / y : x / y;
        case '//': if (y === 0) throw new ErroProlog('Divisão por zero.'); return Math.trunc(x / y);
        case 'mod': if (y === 0) throw new ErroProlog('Divisão por zero.'); return ((x % y) + y) % y;
        case 'rem': if (y === 0) throw new ErroProlog('Divisão por zero.'); return x % y;
        case 'min': return Math.min(x, y); case 'max': return Math.max(x, y);
        case '**': case '^': return x ** y;
      }
    }
    if (a.length === 1) {
      const [x] = a;
      switch (f) {
        case '-': return -x; case '+': return x; case 'abs': return Math.abs(x); case 'sign': return Math.sign(x);
        case 'sqrt': if (x < 0) throw new ErroProlog('Raiz de número negativo.'); return Math.sqrt(x);
        case 'truncate': return Math.trunc(x); case 'round': return Math.round(x); case 'ceiling': return Math.ceil(x); case 'floor': return Math.floor(x);
        case 'float': return x; case 'integer': return Math.round(x);
      }
    }
    throw new ErroProlog(`Não sei calcular ${f}/${a.length}.`);
  }

  // ---- ordem padrão dos termos (para sort e @<)
  private comparar(a0: Termo, b0: Termo): number {
    const a = deref(a0), b = deref(b0);
    const rank = (t: Termo) => (t.k === 'v' ? 0 : t.k === 'n' ? 1 : t.k === 'a' ? 3 : 4);
    if (rank(a) !== rank(b)) return rank(a) - rank(b);
    if (a.k === 'v' && b.k === 'v') return a.id - b.id;
    if (a.k === 'n' && b.k === 'n') return a.v - b.v;
    if (a.k === 'a' && b.k === 'a') return a.n < b.n ? -1 : a.n > b.n ? 1 : 0;
    if (a.k === 'c' && b.k === 'c') {
      if (a.args.length !== b.args.length) return a.args.length - b.args.length;
      if (a.f !== b.f) return a.f < b.f ? -1 : 1;
      for (let i = 0; i < a.args.length; i++) { const c = this.comparar(a.args[i], b.args[i]); if (c) return c; }
    }
    return 0;
  }

  private textoDe(t: Termo): string {
    const d = deref(t);
    if (d.k === 'a') return d.n;
    if (d.k === 'n') return String(d.v);
    const itens = paraArray(d);
    if (itens) return itens.map((x) => this.textoDe(x)).join('');
    throw new ErroProlog('Era esperado um texto ou um átomo.');
  }

  private formatar(fmt: string, args: Termo[]): string {
    let out = '', k = 0;
    for (let i = 0; i < fmt.length; i++) {
      const c = fmt[i];
      if (c !== '~') { out += c; continue; }
      const d = fmt[++i];
      const pega = () => { if (k >= args.length) throw new ErroProlog('format/2: faltam argumentos.'); return args[k++]; };
      if (d === 'w' || d === 'p') out += mostrarTermo(pega(), false);
      else if (d === 'q') out += mostrarTermo(pega(), true);
      else if (d === 'a') out += this.textoDe(pega());
      else if (d === 'd') { const v = deref(pega()); if (v.k !== 'n' || !Number.isInteger(v.v)) throw new ErroProlog('format/2: ~d pede um inteiro.'); out += String(v.v); }
      else if (d === 's') out += this.textoDe(pega());
      else if (d === 'n') out += '\n';
      else if (d === '~') out += '~';
      else if (d === 't' || d === '|' || d === '+') { /* colunas: ignoradas */ }
      else throw new ErroProlog(`format/2: não conheço ~${d}.`);
    }
    return out;
  }

  // ---- o coração: resolver um objetivo (gerador: cada yield é uma solução)
  private *resolver(meta: Termo, ctx: Ctx): Generator<void, void, void> {
    const g = deref(meta);
    if (g.k === 'v') throw new ErroProlog('Falta definir qual objetivo executar (variável sem valor).');
    if (g.k === 'n') throw new ErroProlog('Um número não é um objetivo.');
    const nome = g.k === 'a' ? g.n : g.f;
    const args = g.k === 'a' ? [] : g.args;
    const chave = `${nome}/${args.length}`;
    this.passo();
    if (++this.profundidade > MAX_PROFUNDIDADE) { this.profundidade = 0; throw new ErroProlog('Recursão funda demais.'); }
    try {
      const m = this.trilha.length;
      switch (chave) {
        case 'true/0': yield; return;
        case 'fail/0': case 'false/0': return;
        case '!/0': yield; ctx.cortou = true; return;
        case ',/2':
          for (const _ of this.resolver(args[0], ctx)) {
            for (const __ of this.resolver(args[1], ctx)) yield;
            if (ctx.cortou) return;
          }
          return;
        case ';/2': {
          const c = deref(args[0]);
          if (c.k === 'c' && c.f === '->' && c.args.length === 2) { // (Se -> Então ; Senão)
            let achou = false;
            for (const _ of this.resolver(c.args[0], { cortou: false })) { achou = true; break; }
            if (achou) { yield* this.resolver(c.args[1], ctx); this.desfazer(m); return; }
            this.desfazer(m);
            yield* this.resolver(args[1], ctx);
            return;
          }
          yield* this.resolver(args[0], ctx);
          if (ctx.cortou) return;
          yield* this.resolver(args[1], ctx);
          return;
        }
        case '->/2': {
          let achou = false;
          for (const _ of this.resolver(args[0], { cortou: false })) { achou = true; break; }
          if (achou) { yield* this.resolver(args[1], ctx); this.desfazer(m); }
          return;
        }
        case '\\+/1': {
          let achou = false;
          for (const _ of this.resolver(args[0], { cortou: false })) { achou = true; break; }
          this.desfazer(m);
          if (!achou) yield;
          return;
        }
        case 'findall/3': {
          const res: Termo[] = [];
          for (const _ of this.resolver(args[1], { cortou: false })) res.push(this.copiarResolvido(args[0]));
          if (this.unificar(args[2], lista(res))) yield;
          this.desfazer(m);
          return;
        }
        case 'between/3': {
          const lo = this.calc(args[0]);
          const hiT = deref(args[1]);
          const hi = hiT.k === 'a' && (hiT.n === 'inf' || hiT.n === 'infinite') ? Infinity : this.calc(hiT);
          const x = deref(args[2]);
          if (x.k === 'n') { if (x.v >= lo && x.v <= hi) yield; return; }
          for (let i = lo; i <= hi; i++) { if (this.unificar(x, num(i))) yield; this.desfazer(m); }
          return;
        }
        case 'length/2': {
          const itens = paraArray(args[0]);
          if (itens) { if (this.unificar(args[1], num(itens.length))) yield; this.desfazer(m); return; }
          // lista aberta: gera tamanhos
          let pref = 0, x = deref(args[0]);
          while (x.k === 'c' && x.f === '.') { pref++; x = deref(x.args[1]); }
          if (x.k !== 'v') return;
          const n = deref(args[1]);
          if (n.k === 'n') { if (n.v >= pref && this.unificar(x, lista(Array.from({ length: n.v - pref }, () => novaVar())))) yield; this.desfazer(m); return; }
          for (let extra = 0; extra < 1000; extra++) {
            if (this.unificar(x, lista(Array.from({ length: extra }, () => novaVar()))) && this.unificar(n, num(pref + extra))) yield;
            this.desfazer(m);
          }
          return;
        }
        case 'retract/1': {
          const t = deref(args[0]);
          let cab: Termo = t, corpo: Termo | null = null;
          if (t.k === 'c' && t.f === ':-' && t.args.length === 2) { cab = t.args[0]; corpo = t.args[1]; }
          const k = this.chave(cab);
          const cls = this.db.get(k);
          if (!cls) return;
          for (const c of [...cls]) {
            const r = this.copiarResolvido({ k: 'c', f: ':-', args: [c.cabeca, c.corpo] } as Composto) as Composto;
            if (this.unificar(cab, r.args[0]) && (corpo === null ? true : this.unificar(corpo, r.args[1]))) {
              const lst = this.db.get(k)!; const i = lst.indexOf(c); if (i >= 0) lst.splice(i, 1);
              yield;
            }
            this.desfazer(m);
          }
          return;
        }
        case 'clause/2': {
          const k = this.chave(args[0]);
          for (const c of [...(this.db.get(k) ?? [])]) {
            const r = this.copiarResolvido({ k: 'c', f: ':-', args: [c.cabeca, c.corpo] } as Composto) as Composto;
            if (this.unificar(args[0], r.args[0]) && this.unificar(args[1], r.args[1])) yield;
            this.desfazer(m);
          }
          return;
        }
        case 'sort/2': case 'msort/2': case 'predsort_/0': {
          const xs = paraArray(args[0]);
          if (!xs) throw new ErroProlog('sort/2 espera uma lista completa.');
          let ord = [...xs].sort((p, q) => this.comparar(p, q));
          if (nome === 'sort') ord = ord.filter((x, i) => i === 0 || this.comparar(ord[i - 1], x) !== 0);
          if (this.unificar(args[1], lista(ord))) yield;
          this.desfazer(m);
          return;
        }
        case 'sort/4': {
          const key = deref(args[0]), ordem = deref(args[1]);
          const xs = paraArray(args[2]);
          if (!xs || key.k !== 'n' || ordem.k !== 'a') throw new ErroProlog('sort/4: argumentos inválidos.');
          const chaveDe = (t: Termo) => { if (key.v === 0) return t; const d = deref(t); if (d.k !== 'c') throw new ErroProlog('sort/4: elemento sem argumentos.'); return d.args[key.v - 1]; };
          const desc = ordem.n === '@>' || ordem.n === '@>=';
          let ord = [...xs].sort((p, q) => (desc ? -1 : 1) * this.comparar(chaveDe(p), chaveDe(q)));
          if (ordem.n === '@<' || ordem.n === '@>') ord = ord.filter((x, i) => i === 0 || this.comparar(chaveDe(ord[i - 1]), chaveDe(x)) !== 0);
          if (this.unificar(args[3], lista(ord))) yield;
          this.desfazer(m);
          return;
        }
        case 'call/1': yield* this.resolver(args[0], { cortou: false }); return;
      }
      if (nome === 'call' && args.length > 1) {
        const f = deref(args[0]);
        const extra = args.slice(1);
        const alvo: Termo = f.k === 'a' ? comp(f.n, ...extra) : f.k === 'c' ? comp(f.f, ...f.args, ...extra) : (() => { throw new ErroProlog('call/N: objetivo inválido.'); })();
        yield* this.resolver(alvo, { cortou: false });
        return;
      }

      // predicados determinísticos embutidos
      const det = this.determinismo(chave, args);
      if (det !== undefined) { if (det) yield; this.desfazer(m); return; }

      // predicados do usuário
      const cls = this.db.get(chave);
      if (!cls) {
        if (this.dinamicos.has(chave)) return;
        throw new ErroProlog(`Não existe o predicado ${nome}/${args.length}. Confira o nome e o número de argumentos.`);
      }
      for (const c of [...cls]) {
        const marca = this.trilha.length;
        const mapa = new Map<number, Variavel>();
        const cab = this.copiarResolvido(c.cabeca, mapa);
        if (this.unificar(cab, g)) {
          const corpo = this.copiarResolvido(c.corpo, mapa);
          const ctx2: Ctx = { cortou: false };
          for (const _ of this.resolver(corpo, ctx2)) yield;
          this.desfazer(marca);
          if (ctx2.cortou) return;
        } else this.desfazer(marca);
      }
    } finally { this.profundidade--; }
  }

  /** Embutidos que dão certo ou erram uma vez só. undefined = não é um embutido determinístico. */
  private determinismo(chave: string, a: Termo[]): boolean | undefined {
    switch (chave) {
      case '=/2': return this.unificar(a[0], a[1]);
      case '\\=/2': { const m = this.trilha.length; const r = this.unificar(a[0], a[1]); this.desfazer(m); return !r; }
      case '==/2': return this.comparar(a[0], a[1]) === 0;
      case '\\==/2': return this.comparar(a[0], a[1]) !== 0;
      case '@</2': return this.comparar(a[0], a[1]) < 0;
      case '@>/2': return this.comparar(a[0], a[1]) > 0;
      case '@=</2': return this.comparar(a[0], a[1]) <= 0;
      case '@>=/2': return this.comparar(a[0], a[1]) >= 0;
      case 'is/2': return this.unificar(a[0], num(this.calc(a[1])));
      case '=:=/2': return this.calc(a[0]) === this.calc(a[1]);
      case '=\\=/2': return this.calc(a[0]) !== this.calc(a[1]);
      case '</2': return this.calc(a[0]) < this.calc(a[1]);
      case '>/2': return this.calc(a[0]) > this.calc(a[1]);
      case '=</2': return this.calc(a[0]) <= this.calc(a[1]);
      case '>=/2': return this.calc(a[0]) >= this.calc(a[1]);
      case 'var/1': return deref(a[0]).k === 'v';
      case 'nonvar/1': return deref(a[0]).k !== 'v';
      case 'atom/1': return deref(a[0]).k === 'a';
      case 'number/1': return deref(a[0]).k === 'n';
      case 'integer/1': { const d = deref(a[0]); return d.k === 'n' && Number.isInteger(d.v); }
      case 'atomic/1': { const d = deref(a[0]); return d.k === 'a' || d.k === 'n'; }
      case 'compound/1': return deref(a[0]).k === 'c';
      case 'is_list/1': return paraArray(a[0]) !== null;
      case 'succ/2': { const x = deref(a[0]); if (x.k === 'n') return this.unificar(a[1], num(x.v + 1)); const y = deref(a[1]); if (y.k === 'n' && y.v > 0) return this.unificar(a[0], num(y.v - 1)); throw new ErroProlog('succ/2: falta um valor.'); }
      case 'plus/3': return this.unificar(a[2], num(this.calc(a[0]) + this.calc(a[1])));
      case 'assert/1': case 'assertz/1': this.adicionarDinamico(a[0], true); return true;
      case 'asserta/1': this.adicionarDinamico(a[0], false); return true;
      case 'retractall/1': {
        const t = deref(a[0]); const k = this.chave(t);
        if (!this.db.has(k)) { this.dinamicos.add(k); this.db.set(k, []); return true; }
        const lst = this.db.get(k)!;
        this.db.set(k, lst.filter((c) => { const m = this.trilha.length; const r = this.copiarResolvido(c.cabeca); const ok = this.unificar(t, r); this.desfazer(m); return !ok; }));
        return true;
      }
      case 'dynamic/1': this.declararDinamicos(a[0]); return true;
      case 'discontiguous/1': return true;
      case 'halt/0': return true;
      case 'write/1': case 'print/1': this.saida += mostrarTermo(a[0], false); return true;
      case 'writeq/1': case 'write_canonical/1': this.saida += mostrarTermo(a[0], true); return true;
      case 'writeln/1': this.saida += mostrarTermo(a[0], false) + '\n'; return true;
      case 'nl/0': this.saida += '\n'; return true;
      case 'tab/1': this.saida += ' '.repeat(Math.max(0, this.calc(a[0]))); return true;
      case 'format/1': this.saida += this.formatar(this.textoDe(a[0]), []); return true;
      case 'format/2': { const l = paraArray(a[1]); this.saida += this.formatar(this.textoDe(a[0]), l ?? [a[1]]); return true; }
      case 'atom_length/2': return this.unificar(a[1], num(this.textoDe(a[0]).length));
      case 'atom_chars/2': { const d = deref(a[0]); if (d.k !== 'v') return this.unificar(a[1], lista([...this.textoDe(d)].map(atomo))); const l = paraArray(a[1]); if (!l) throw new ErroProlog('atom_chars/2: falta a lista.'); return this.unificar(a[0], atomo(l.map((x) => this.textoDe(x)).join(''))); }
      case 'atom_concat/3': return this.unificar(a[2], atomo(this.textoDe(a[0]) + this.textoDe(a[1])));
      case 'upcase_atom/2': return this.unificar(a[1], atomo(this.textoDe(a[0]).toUpperCase()));
      case 'downcase_atom/2': return this.unificar(a[1], atomo(this.textoDe(a[0]).toLowerCase()));
      case 'atom_number/2': { const d = deref(a[0]); if (d.k === 'a') { const n = Number(d.n); return d.n.trim() !== '' && !Number.isNaN(n) && this.unificar(a[1], num(n)); } const nn = deref(a[1]); return nn.k === 'n' && this.unificar(a[0], atomo(String(nn.v))); }
      case 'functor/3': { const d = deref(a[0]); if (d.k === 'c') return this.unificar(a[1], atomo(d.f)) && this.unificar(a[2], num(d.args.length)); if (d.k === 'v') { const n = deref(a[1]), ar = deref(a[2]); if (n.k === 'a' && ar.k === 'n') return this.unificar(d, ar.v === 0 ? n : comp(n.n, ...Array.from({ length: ar.v }, () => novaVar()))); throw new ErroProlog('functor/3: faltam valores.'); } return this.unificar(a[1], d) && this.unificar(a[2], num(0)); }
      case 'arg/3': { const n = deref(a[0]), t = deref(a[1]); if (n.k !== 'n' || t.k !== 'c') throw new ErroProlog('arg/3: argumentos inválidos.'); return n.v >= 1 && n.v <= t.args.length && this.unificar(a[2], t.args[n.v - 1]); }
      case '=../2': { const d = deref(a[0]); if (d.k === 'c') return this.unificar(a[1], lista([atomo(d.f), ...d.args])); if (d.k !== 'v') return this.unificar(a[1], lista([d])); const l = paraArray(a[1]); if (!l || !l.length) throw new ErroProlog('=../2: falta a lista.'); const f = deref(l[0]); return this.unificar(d, l.length === 1 ? f : comp(this.textoDe(f), ...l.slice(1))); }
      case 'copy_term/2': return this.unificar(a[1], this.copiarResolvido(a[0]));
      case 'tab/2': return true;
    }
    return undefined;
  }

  private adicionarDinamico(t: Termo, fim: boolean) {
    const d = deref(t);
    const k = this.chave(d.k === 'c' && d.f === ':-' && d.args.length === 2 ? d.args[0] : d);
    this.dinamicos.add(k);
    this.adicionar(d, fim);
  }

  // ---- consultas
  /** Roda uma consulta ("pai(X, joao)." ou "membro(X, [a,b]), X \\= a"). Devolve até `max` soluções. */
  consultar(texto: string, max = 10): Resultado & { erro?: string } {
    this.saida = ''; this.passos = 0; this.profundidade = 0;
    let leitor: Leitor, meta: Termo | null;
    try {
      leitor = new Leitor(lexer(texto.trim().replace(/^\?-\s*/, '')));
      meta = leitor.lerClausula(false);
      if (!meta) return { solucoes: [], saida: '', mais: false, erro: 'Escreva uma consulta, por exemplo: pai(X, joao).' };
    } catch (e) { return { solucoes: [], saida: '', mais: false, erro: (e as Error).message }; }
    const nomes = [...leitor.mapaVars.entries()].filter(([n]) => !n.startsWith('_'));
    const solucoes: Record<string, string>[] = [];
    let mais = false;
    const marca = this.trilha.length;
    try {
      for (const _ of this.resolver(meta, { cortou: false })) {
        if (solucoes.length >= max) { mais = true; break; }
        const s: Record<string, string> = {};
        for (const [n, v] of nomes) s[n] = deref(v).k === 'v' ? '_' : mostrarTermo(v, true);
        solucoes.push(s);
      }
    } catch (e) {
      this.desfazer(marca);
      const msg = e instanceof ErroProlog ? e.message : e instanceof RangeError ? 'Recursão funda demais.' : (e as Error).message;
      return { solucoes, saida: this.saida, mais: false, erro: msg };
    }
    this.desfazer(marca);
    return { solucoes, saida: this.saida, mais };
  }
}
