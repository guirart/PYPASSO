/**
 * Lógica proposicional: lê fórmulas escritas à mão, monta a tabela de verdade e testa a validade de argumentos
 * (premissas ⊢ conclusão), mostrando um contra-exemplo quando o argumento é inválido.
 *
 * Escrita aceita (qualquer uma): ¬ ~ !  ∧ & ^ e  ∨ | v ou  → -> =>  ↔ <-> <=>  e parênteses.
 * Letras de proposições: P, Q, R, S... (maiúsculas ou minúsculas, sem "v" sozinho, que é "ou").
 * Arquivo puro (sem telas nem imagens) para ser fácil de testar.
 */
export type Formula =
  | { t: 'var'; nome: string }
  | { t: 'nao'; a: Formula }
  | { t: 'e' | 'ou' | 'se' | 'sse'; a: Formula; b: Formula };

type Token = { k: 'var' | 'nao' | 'e' | 'ou' | 'se' | 'sse' | '(' | ')'; v?: string };

/** Quebra o texto em símbolos. Aceita os operadores em símbolo, ASCII ou palavra. */
function tokens(src: string): Token[] {
  const s = src.trim();
  const out: Token[] = [];
  let i = 0;
  while (i < s.length) {
    const resto = s.slice(i);
    const c = s[i];
    if (/\s/.test(c)) { i++; continue; }
    let m: RegExpMatchArray | null;
    if ((m = resto.match(/^(<->|<=>|↔|⇔)/))) { out.push({ k: 'sse' }); i += m[0].length; continue; }
    if ((m = resto.match(/^(->|=>|→|⇒|⊃)/))) { out.push({ k: 'se' }); i += m[0].length; continue; }
    if ((m = resto.match(/^(¬|~|!|-(?!>))/))) { out.push({ k: 'nao' }); i += m[0].length; continue; }
    if ((m = resto.match(/^(∧|&&|&|\^|\.)/))) { out.push({ k: 'e' }); i += m[0].length; continue; }
    if ((m = resto.match(/^(∨|\|\||\|)/))) { out.push({ k: 'ou' }); i += m[0].length; continue; }
    if (c === '(') { out.push({ k: '(' }); i++; continue; }
    if (c === ')') { out.push({ k: ')' }); i++; continue; }
    if ((m = resto.match(/^[A-Za-zÀ-ÿ][A-Za-zÀ-ÿ0-9_]*/))) {
      const w = m[0];
      const baixa = w.toLowerCase();
      if (baixa === 'e' || baixa === 'and') out.push({ k: 'e' });
      else if (baixa === 'ou' || baixa === 'or' || baixa === 'v') out.push({ k: 'ou' });
      else if (baixa === 'nao' || baixa === 'não' || baixa === 'not') out.push({ k: 'nao' });
      else if (baixa === 'se' || baixa === 'entao' || baixa === 'então') { throw new Error('Escreva o condicional com a seta: P -> Q'); }
      else out.push({ k: 'var', v: w.toUpperCase() });
      i += w.length;
      continue;
    }
    throw new Error(`Símbolo inesperado: "${c}"`);
  }
  return out;
}

/**
 * Gramática (da que menos prende para a que mais prende): ↔  →  ∨  ∧  ¬ . O → e o ↔ são associativos à direita.
 */
export function lerFormula(texto: string): Formula {
  const ts = tokens(texto);
  if (!ts.length) throw new Error('Escreva uma fórmula.');
  let p = 0;
  const olha = () => ts[p];
  const come = (k: Token['k']) => { if (olha()?.k !== k) throw new Error(k === ')' ? 'Faltou fechar um parêntese.' : 'Fórmula incompleta.'); return ts[p++]; };

  function sse(): Formula { const a = se(); if (olha()?.k === 'sse') { p++; return { t: 'sse', a, b: sse() }; } return a; }
  function se(): Formula { const a = ou(); if (olha()?.k === 'se') { p++; return { t: 'se', a, b: se() }; } return a; }
  function ou(): Formula { let a = e(); while (olha()?.k === 'ou') { p++; a = { t: 'ou', a, b: e() }; } return a; }
  function e(): Formula { let a = nao(); while (olha()?.k === 'e') { p++; a = { t: 'e', a, b: nao() }; } return a; }
  function nao(): Formula {
    if (olha()?.k === 'nao') { p++; return { t: 'nao', a: nao() }; }
    return atomo();
  }
  function atomo(): Formula {
    const t = olha();
    if (!t) throw new Error('Fórmula incompleta.');
    if (t.k === 'var') { p++; return { t: 'var', nome: t.v! }; }
    if (t.k === '(') { p++; const f = sse(); come(')'); return f; }
    throw new Error('Fórmula incompleta.');
  }
  const f = sse();
  if (p < ts.length) throw new Error(ts[p].k === ')' ? 'Parêntese a mais.' : 'Faltou um conectivo entre duas letras.');
  return f;
}

export type Valoracao = Record<string, boolean>;

export function avaliar(f: Formula, v: Valoracao): boolean {
  switch (f.t) {
    case 'var': return !!v[f.nome];
    case 'nao': return !avaliar(f.a, v);
    case 'e': return avaliar(f.a, v) && avaliar(f.b, v);
    case 'ou': return avaliar(f.a, v) || avaliar(f.b, v);
    case 'se': return !avaliar(f.a, v) || avaliar(f.b, v); // condicional material
    case 'sse': return avaliar(f.a, v) === avaliar(f.b, v);
  }
}

export function variaveis(f: Formula, acc: string[] = []): string[] {
  if (f.t === 'var') { if (!acc.includes(f.nome)) acc.push(f.nome); }
  else if (f.t === 'nao') variaveis(f.a, acc);
  else { variaveis(f.a, acc); variaveis(f.b, acc); }
  return acc;
}

/** Escreve a fórmula de volta, com símbolos e só os parênteses necessários. */
export function mostrar(f: Formula, pai = 0): string {
  const PREC = { sse: 1, se: 2, ou: 3, e: 4, nao: 5, var: 6 } as const;
  const p = PREC[f.t];
  let s: string;
  if (f.t === 'var') s = f.nome;
  else if (f.t === 'nao') s = '¬' + mostrar(f.a, p);
  else {
    const op = { e: '∧', ou: '∨', se: '→', sse: '↔' }[f.t];
    // → e ↔ associam à direita: o lado esquerdo do mesmo nível leva parênteses
    const esq = f.t === 'se' || f.t === 'sse' ? mostrar(f.a, p + 0.5) : mostrar(f.a, p);
    s = `${esq} ${op} ${mostrar(f.b, p)}`;
  }
  return p < pai ? `(${s})` : s;
}

/** Todas as linhas da tabela, na ordem usual (V primeiro): 2^n situações. */
export function todasAsValoracoes(vars: string[]): Valoracao[] {
  const n = vars.length;
  const linhas: Valoracao[] = [];
  for (let i = 0; i < 2 ** n; i++) {
    const v: Valoracao = {};
    vars.forEach((nome, k) => { v[nome] = ((i >> (n - 1 - k)) & 1) === 0; });
    linhas.push(v);
  }
  return linhas;
}

export type Tabela = { vars: string[]; colunas: string[]; linhas: { v: Valoracao; valores: boolean[] }[] };

/** Tabela de verdade de uma ou mais fórmulas (uma coluna por fórmula, depois das letras). */
export function tabela(fs: Formula[]): Tabela {
  const vars = [...new Set(fs.flatMap((f) => variaveis(f)))].sort();
  return { vars, colunas: fs.map((f) => mostrar(f)), linhas: todasAsValoracoes(vars).map((v) => ({ v, valores: fs.map((f) => avaliar(f, v)) })) };
}

export type Veredito = {
  valido: boolean;
  vars: string[];
  /** a 1ª linha com todas as premissas V e a conclusão F, se existir (o contra-exemplo) */
  contraExemplo?: Valoracao;
  /** quantas linhas têm todas as premissas verdadeiras */
  linhasComPremissasV: number;
  tabela: Tabela;
};

/** Testa a validade: não pode existir situação com todas as premissas V e a conclusão F. */
export function validade(premissas: Formula[], conclusao: Formula): Veredito {
  const todas = [...premissas, conclusao];
  const tb = tabela(todas);
  let contra: Valoracao | undefined;
  let comPremV = 0;
  for (const l of tb.linhas) {
    const premV = l.valores.slice(0, premissas.length).every(Boolean);
    if (premV) comPremV++;
    if (premV && !l.valores[premissas.length] && !contra) contra = l.v;
  }
  return { valido: !contra, vars: tb.vars, contraExemplo: contra, linhasComPremissasV: comPremV, tabela: tb };
}

/** Duas fórmulas são equivalentes quando têm a mesma tabela. */
export function equivalentes(a: Formula, b: Formula): boolean {
  const vars = [...new Set([...variaveis(a), ...variaveis(b)])];
  return todasAsValoracoes(vars).every((v) => avaliar(a, v) === avaliar(b, v));
}

/** Classifica: tautologia (sempre V), contradição (sempre F) ou contingência. */
export function classificar(f: Formula): 'tautologia' | 'contradicao' | 'contingencia' {
  const vals = todasAsValoracoes(variaveis(f)).map((v) => avaliar(f, v));
  return vals.every(Boolean) ? 'tautologia' : vals.every((x) => !x) ? 'contradicao' : 'contingencia';
}
