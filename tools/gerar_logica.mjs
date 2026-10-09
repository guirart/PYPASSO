// Gera src/content/logica.json (trilha "Lógica", em lista simples, sem mapa nem chefes).
// Uso:  node tools/gerar_logica.mjs
// Conteúdo original, baseado nos temas das aulas "Argumentos e Validade" e "Predicados, Normas e Tempo" (MDInf, UMinho)
// e em exemplos de Prolog no espírito do SWISH. Nada é copiado literalmente.
import { writeFileSync } from 'node:fs';

const HOSTS = ['pipo', 'ana', 'caio', 'bia', 'teo'];
let n = 0;
const host = () => HOSTS[n++ % HOSTS.length];

// ---------- construtores de exercícios
const L = (q, body, c, extra = {}) => ({ k: 'learn', q, body, c, out: extra.out ?? '', e: '', ...(extra.rc ? { rc: extra.rc } : {}), ...(extra.ro ? { ro: extra.ro } : {}) });
/** múltipla escolha: a primeira opção é a correta. mono = fonte de código nas opções */
const M = (q, o, e, c, mono = false) => ({ k: 'mc', q, o, e, ...(c ? { c } : {}), mono });
const F = (q, c, b, a, e) => ({ k: 'fill', q, c, b, a, e });
const O = (q, l, e) => ({ k: 'order', q, l, e });
const T = (q, a, e, c = '') => ({ k: 'type', q, c, a, e });

const unidades = [];
const U = (id, title, description, lessons) => unidades.push({ id, title, description, lessons });
const Lic = (title, ex) => ({ title, ex });

// ---------- Unidade 0
U('lg0', 'Argumentos', 'premissas, conclusão e indicadores', [
  Lic('O que é um argumento', [
    L('Argumento = premissas + conclusão', 'Um argumento é um conjunto de enunciados em que alguns (as premissas) são dados como razões a favor de outro (a conclusão). Enunciado é uma frase que pode ser verdadeira ou falsa.', 'Premissa 1: Todo humano é mortal.\nPremissa 2: Sócrates é humano.\nConclusão: Sócrates é mortal.'),
    M('Qual destas frases é um enunciado (pode ser verdadeira ou falsa)?', ['A capital da França é Paris.', 'Feche a porta!', 'Que horas são?', 'Por favor, me ajude.'], 'Ordens, perguntas e pedidos não são nem verdadeiros nem falsos.'),
    M('Em "Todo humano é mortal; Sócrates é humano; logo, Sócrates é mortal", qual é a conclusão?', ['Sócrates é mortal', 'Todo humano é mortal', 'Sócrates é humano', 'Logo'], 'A conclusão é o que o argumento quer provar. Aqui vem depois do "logo".'),
    L('Palavras-pista', 'Palavras como "logo", "portanto", "assim" e "então" costumam anunciar a conclusão. Já "porque", "pois", "já que" e "visto que" anunciam premissas.', 'Está chovendo, portanto a rua está molhada.\nA rua está molhada porque está chovendo.'),
    M('Em "A rua está molhada porque choveu", qual é a conclusão?', ['A rua está molhada', 'Choveu', 'Não há argumento', 'As duas frases'], '"Porque" anuncia a premissa (choveu). A conclusão é a outra parte.'),
    M('Qual destes textos é um argumento?', ['Chove, logo a rua vai ficar molhada.', 'Chove e faz frio.', 'Que dia lindo!', 'Chovia muito naquele dia.'], 'Só o primeiro apresenta uma razão e uma conclusão que decorre dela.'),
    O('Monte o argumento: premissas primeiro, conclusão por último.', ['Todo gato é mamífero.', 'Mimi é um gato.', 'Logo, Mimi é mamífero.'], 'Premissas abrem o caminho; a conclusão fecha.'),
  ]),
  Lic('Dedução e indução', [
    L('Dedutivo x indutivo', 'Num argumento dedutivo a conclusão pretende ser garantida pelas premissas. Num indutivo, ela só é tornada provável. Neste módulo estudamos a lógica dedutiva.', 'Dedutivo:\n  Todo gato é mamífero. Mimi é gato.\n  Logo, Mimi é mamífero.\n\nIndutivo:\n  Todos os corvos que vi eram pretos.\n  Logo, o próximo corvo será preto.'),
    M('"Vi 100 cisnes e todos eram brancos; logo, todos os cisnes são brancos." Esse argumento é:', ['indutivo', 'dedutivo', 'sem conclusão', 'uma pergunta'], 'Generaliza a partir de casos observados: só torna a conclusão provável.'),
    M('Que tipo de argumento pretende garantir a conclusão?', ['dedutivo', 'indutivo', 'retórico', 'emotivo'], 'Na dedução, se as premissas valem, a conclusão tem de valer.'),
    M('Num argumento indutivo, as premissas tornam a conclusão...', ['provável, mas não garantida', 'garantida', 'impossível', 'sempre falsa'], 'Mesmo com premissas verdadeiras, a conclusão indutiva pode falhar.'),
    F('Complete.', 'Argumento ___: a conclusão é garantida pelas premissas.\nArgumento ___: a conclusão é apenas provável.', ['dedutivo', 'indutivo', 'falso', 'livre'], ['dedutivo', 'indutivo'], 'Dedução garante; indução só torna provável.'),
  ]),
]);

// ---------- Unidade 1
U('lg1', 'Validade e solidez', 'quando um argumento "funciona"', [
  Lic('Validade', [
    L('Válido = sem contra-exemplo', 'Um argumento é válido quando é impossível as premissas serem todas verdadeiras e a conclusão falsa. Validade fala da forma do raciocínio, não de a conclusão ser verdadeira no mundo real.', 'Todo peixe voa.\nBob é um peixe.\nLogo, Bob voa.', { rc: 'EXEMPLO', ro: 'VEREDITO', out: 'Válido (embora a 1ª premissa seja falsa)' }),
    M('O argumento "Todo peixe voa; Bob é peixe; logo, Bob voa" é:', ['válido', 'inválido', 'indutivo', 'impossível de avaliar'], 'Se as premissas fossem verdadeiras, a conclusão seria obrigada a ser. Isso é validade.'),
    M('Um argumento válido pode ter uma premissa falsa?', ['Sim', 'Não', 'Só se for indutivo', 'Só se a conclusão for falsa'], 'Validade só garante: premissas V ⇒ conclusão V. Com premissa falsa, nada se promete.'),
    M('Premissas todas verdadeiras e conclusão falsa significa que o argumento é:', ['inválido', 'válido', 'sólido', 'indutivo'], 'Essa combinação é exatamente o que a validade proíbe.'),
    M('"Alguns gatos são pretos; Mimi é preta; logo, Mimi é gata." Esse argumento é:', ['inválido', 'válido', 'sólido', 'uma tautologia'], 'Mimi poderia ser uma cachorra preta: premissas V e conclusão F.'),
  ]),
  Lic('Solidez e contra-exemplo', [
    L('Sólido = válido + premissas verdadeiras', 'Um argumento sólido é válido e tem todas as premissas verdadeiras. Só aí a conclusão está mesmo garantida no mundo real.', 'Todo gato é mamífero. (V)\nMimi é um gato. (V)\nLogo, Mimi é mamífero.', { ro: 'VEREDITO', out: 'Válido e sólido' }),
    M('Um argumento sólido é:', ['válido e com premissas verdadeiras', 'qualquer um com conclusão verdadeira', 'inválido com premissas verdadeiras', 'válido com conclusão falsa'], 'Solidez = validade + verdade das premissas.'),
    M('Um argumento é válido, mas uma premissa é falsa. Ele é:', ['válido e não sólido', 'sólido', 'inválido', 'indutivo'], 'A forma está certa, mas falta a verdade das premissas.'),
    L('Contra-exemplo', 'Para mostrar que um argumento é inválido, descreva uma situação em que as premissas são verdadeiras e a conclusão é falsa.', 'Se chove, a rua molha.\nA rua está molhada.\nLogo, choveu.\n\nContra-exemplo: o caminhão-pipa lavou a rua e não choveu.'),
    M('Para refutar a validade de um argumento basta:', ['achar um contra-exemplo', 'achar uma premissa falsa', 'achar que a conclusão é falsa', 'achar uma premissa verdadeira'], 'Premissa falsa não refuta validade. É preciso premissas V e conclusão F ao mesmo tempo.'),
    M('Qual destes argumentos é inválido, mesmo com conclusão verdadeira?', ['Lisboa é capital de Portugal; logo, a Terra é redonda.', 'Todo A é B; x é A; logo, x é B.', 'Se P então Q; P; logo, Q.', 'P ou Q; não P; logo, Q.'], 'Verdade da conclusão não basta: as premissas precisam levar a ela.'),
  ]),
]);

// ---------- Unidade 2
const TAB = 'P Q | ¬P  P∧Q  P∨Q\nV V |  F    V    V\nV F |  F    F    V\nF V |  V    F    V\nF F |  V    F    F';
const TABC = 'P Q | P→Q  P↔Q\nV V |  V    V\nV F |  F    F\nF V |  V    F\nF F |  V    V';
U('lg2', 'Conectivos e tabelas', '¬ ∧ ∨ → ↔ e a tabela de verdade', [
  Lic('Os conectivos', [
    L('Não, e, ou', '¬P (não P) inverte o valor. P ∧ Q (P e Q) só é verdadeiro se os dois forem. P ∨ Q (P ou Q) é verdadeiro se pelo menos um for (o "ou" da lógica é inclusivo).', TAB, { rc: 'TABELA' }),
    T('P = V e Q = F. Quanto vale P ∧ Q? (V ou F)', ['F', 'f'], 'O "e" só é verdadeiro quando os dois são.'),
    T('P = F e Q = V. Quanto vale P ∨ Q? (V ou F)', ['V', 'v'], 'O "ou" basta que um seja verdadeiro.'),
    L('Condicional →', 'P → Q só é falso num caso: P verdadeiro e Q falso. Se P é falso, o condicional é verdadeiro (a promessa não foi quebrada). É o condicional material.', TABC, { rc: 'TABELA' }),
    M('P → Q, com P falso e Q falso, vale:', ['V', 'F', 'depende', 'indefinido'], 'Antecedente falso torna o condicional verdadeiro ("verdade vazia").'),
    M('Quando P → Q é falso?', ['P verdadeiro e Q falso', 'P falso e Q verdadeiro', 'P falso e Q falso', 'P e Q verdadeiros'], 'Só quando a promessa é quebrada: P acontece e Q não.'),
    M('P ↔ Q, com P = V e Q = F, vale:', ['F', 'V', 'depende', 'indefinido'], 'O bicondicional é verdadeiro quando P e Q têm o mesmo valor.'),
    T('P = F e Q = F. Quanto vale P ↔ Q? (V ou F)', ['V', 'v'], 'Mesmo valor nos dois lados ⇒ verdadeiro.'),
  ]),
  Lic('Traduzindo e classificando', [
    L('De português para símbolos', '"Se P então Q" → P → Q. "P somente se Q" → P → Q. "P se Q" → Q → P. "Nem P nem Q" → ¬P ∧ ¬Q. "P a menos que Q" → ¬Q → P.', 'Se chove, eu levo guarda-chuva.   P → Q\nSó saio se fizer sol.             S → X\nNem chove nem venta.              ¬P ∧ ¬Q'),
    M('"Eu passo somente se estudar" (P: passo; Q: estudo) é:', ['P → Q', 'Q → P', 'P ∧ Q', 'P ↔ Q'], '"A somente se B" = A → B.'),
    M('"Nem chove nem venta" (P: chove; Q: venta) é:', ['¬P ∧ ¬Q', '¬(P ∧ Q)', '¬P ∨ ¬Q', 'P ∨ Q'], '"Nem... nem" nega as duas coisas ao mesmo tempo.'),
    M('"Levo guarda-chuva se chover" (P: chove; Q: levo) é:', ['P → Q', 'Q → P', 'P ∧ Q', 'Q ↔ P'], '"B se A" = A → B: chover leva a levar.'),
    T('Quantas linhas tem a tabela de verdade com 3 letras (P, Q, R)? (número)', ['8'], '2 × 2 × 2 = 8 combinações.'),
    T('E com 2 letras? (número)', ['4'], '2 × 2 = 4.'),
    M('Uma fórmula verdadeira em todas as linhas chama-se:', ['tautologia', 'contradição', 'contingência', 'premissa'], 'Tautologia: sempre V. Contradição: sempre F. Contingência: depende.'),
    M('P ∨ ¬P é uma:', ['tautologia', 'contradição', 'contingência', 'premissa'], 'Ou P ou não P: sempre verdadeiro.'),
    M('P ∧ ¬P é uma:', ['contradição', 'tautologia', 'contingência', 'conclusão'], 'Nunca verdadeiro: P e não P juntos.'),
    L('Confira na Calculadora de lógica', 'Na aba Lógica do app há uma Calculadora: digite premissas e conclusão, veja a tabela de verdade e o contra-exemplo quando o argumento for inválido.', 'Premissas:  P -> Q ,  Q\nConclusão:  P\n\nResultado: inválido (P = F, Q = V)'),
  ]),
]);

// ---------- Unidade 3
U('lg3', 'Formas válidas e falácias', 'modus ponens, tollens e os erros clássicos', [
  Lic('Formas válidas', [
    L('Modus ponens', 'Se o condicional é verdadeiro e o antecedente é verdadeiro, o consequente tem de ser verdadeiro.', 'P → Q\nP\n―――――\nQ'),
    M('Se chove, a rua molha. Chove. Logo...', ['a rua molha', 'não chove', 'a rua seca', 'nada se conclui'], 'É modus ponens: afirma o antecedente e conclui o consequente.'),
    L('Modus tollens', 'Se o condicional é verdadeiro e o consequente é falso, o antecedente também tem de ser falso.', 'P → Q\n¬Q\n―――――\n¬P'),
    M('Se estudo, passo. Não passei. Logo...', ['não estudei', 'estudei', 'passei', 'nada se conclui'], 'Modus tollens: negar o consequente nega o antecedente.'),
    L('Silogismos', 'Hipotético: encadeia condicionais. Disjuntivo: se uma das alternativas cai, a outra fica.', 'P → Q\nQ → R\n―――――\nP → R\n\nP ∨ Q\n¬P\n―――――\nQ'),
    M('P ∨ Q e ¬Q. Conclui-se:', ['P', '¬P', 'Q', 'P ∧ Q'], 'Silogismo disjuntivo: se Q cai, sobra P.'),
    M('Qual é o nome desta forma?  P → Q ; ¬Q ⊢ ¬P', ['modus tollens', 'modus ponens', 'silogismo hipotético', 'silogismo disjuntivo'], 'Nega o consequente para negar o antecedente.'),
    O('Ordene este modus ponens.', ['Se há fumaça, há fogo.', 'Há fumaça.', 'Logo, há fogo.'], 'Condicional, antecedente, consequente.'),
  ]),
  Lic('Falácias e equivalências', [
    L('Afirmar o consequente', 'De P → Q e Q não se conclui P. Contra-exemplo: P falso e Q verdadeiro torna as premissas verdadeiras e a conclusão falsa.', 'P → Q\nQ\n―――――\nP        ← inválido!', { ro: 'CONTRA-EXEMPLO', out: 'P = F, Q = V' }),
    M('"Se chove, a rua molha. A rua está molhada. Logo, choveu." Qual é o erro?', ['afirmação do consequente', 'modus ponens', 'modus tollens', 'silogismo disjuntivo'], 'A rua pode ter molhado por outro motivo.'),
    L('Negar o antecedente', 'De P → Q e ¬P não se conclui ¬Q. Outras causas podem levar a Q.', 'P → Q\n¬P\n―――――\n¬Q        ← inválido!', { ro: 'CONTRA-EXEMPLO', out: 'P = F, Q = V' }),
    M('"Se estudo, passo. Não estudei. Logo, não passei." É:', ['negação do antecedente (inválido)', 'modus tollens (válido)', 'modus ponens (válido)', 'silogismo hipotético'], 'Pode-se passar sem estudar (por sorte, por talento).'),
    M('Qual destas formas é VÁLIDA?', ['P → Q ; ¬Q ⊢ ¬P', 'P → Q ; Q ⊢ P', 'P → Q ; ¬P ⊢ ¬Q', 'P ∨ Q ; P ⊢ ¬Q'], 'Só a primeira é válida (modus tollens).'),
    M('Por que P ∨ Q ; P ⊢ ¬Q é inválido?', ['o "ou" é inclusivo: P e Q podem ser os dois verdadeiros', 'o "ou" é exclusivo', 'P é falso', 'Q é falso'], 'Com P = V e Q = V as premissas são V e a conclusão ¬Q é F.'),
    L('Equivalências úteis', 'Duas fórmulas equivalentes têm a mesma tabela de verdade. Podemos trocar uma pela outra.', 'P → Q  ≡  ¬P ∨ Q\nP → Q  ≡  ¬Q → ¬P      (contrapositiva)\n¬(P ∧ Q)  ≡  ¬P ∨ ¬Q   (De Morgan)\n¬(P ∨ Q)  ≡  ¬P ∧ ¬Q   (De Morgan)'),
    M('A contrapositiva de "Se chove, molha" é:', ['Se não molha, não chove', 'Se molha, chove', 'Se não chove, não molha', 'Chove e não molha'], 'Contrapositiva: inverte e nega os dois lados. É equivalente.'),
    M('¬(P ∧ Q) equivale a:', ['¬P ∨ ¬Q', '¬P ∧ ¬Q', 'P ∨ Q', 'P → Q'], 'De Morgan: negar um "e" vira um "ou" de negações.'),
    M('"Se P então Q" e "Se Q então P" são:', ['não equivalentes', 'equivalentes', 'contraditórias', 'iguais'], 'A recíproca não é equivalente ao condicional original.'),
  ]),
]);

// ---------- Unidade 4
U('lg4', 'Predicados e quantificadores', '∀ (para todo) e ∃ (existe)', [
  Lic('Predicados', [
    L('Predicados descrevem propriedades', 'A lógica proposicional não enxerga dentro da frase. Com predicados escrevemos Humano(sócrates). Com ∀x ("para todo x") e ∃x ("existe x") dizemos sobre quantos indivíduos vale algo.', 'Humano(sócrates)\n∀x (Humano(x) → Mortal(x))\n∃x Gato(x)'),
    M('Como escrever "Todo humano é mortal"?', ['∀x (Humano(x) → Mortal(x))', '∀x (Humano(x) ∧ Mortal(x))', '∃x (Humano(x) → Mortal(x))', '∃x (Humano(x) ∧ Mortal(x))'], 'Com ∀ usa-se o condicional →.'),
    M('Como escrever "Algum gato é preto"?', ['∃x (Gato(x) ∧ Preto(x))', '∃x (Gato(x) → Preto(x))', '∀x (Gato(x) ∧ Preto(x))', '∀x (Gato(x) → Preto(x))'], 'Com ∃ usa-se a conjunção ∧.'),
    L('A regra de ouro', 'Com ∀ use →. Com ∃ use ∧. ∀x (Gato(x) ∧ Preto(x)) diria que TUDO é gato preto. ∃x (Gato(x) → Preto(x)) fica verdadeiro só porque existe algo que não é gato.', '∀ ...  →\n∃ ...  ∧'),
    M('∀x (Humano(x) ∧ Mortal(x)) diz que:', ['tudo é humano e mortal', 'todo humano é mortal', 'algum humano é mortal', 'nenhum humano é mortal'], 'O ∧ sob o ∀ afirma as duas coisas de tudo que existe.'),
    M('Por que ∃x (Gato(x) → Preto(x)) não serve para "algum gato é preto"?', ['fica verdadeiro com qualquer coisa que não seja gato', 'porque ∃ não aceita →', 'porque Gato é falso', 'serve, sim'], 'Se algo não é gato, o antecedente é falso e o condicional é verdadeiro.'),
  ]),
  Lic('Negação e silogismo', [
    L('Negando quantificadores', 'Para negar "todos", basta um que não. Para negar "existe", nenhum pode.', '¬∀x P(x)  ≡  ∃x ¬P(x)\n¬∃x P(x)  ≡  ∀x ¬P(x)'),
    M('A negação de "todo aluno passou" é:', ['algum aluno não passou', 'nenhum aluno passou', 'todo aluno não passou', 'algum aluno passou'], '¬∀ vira ∃¬.'),
    M('A negação de "algum político é honesto" é:', ['nenhum político é honesto', 'algum político não é honesto', 'todo político é honesto', 'alguns são honestos'], '¬∃ vira ∀¬: nenhum é honesto.'),
    M('∀x ¬Dragão(x) significa:', ['não existem dragões', 'todos são dragões', 'existe um não-dragão', 'existe um dragão'], 'Para todo x, x não é dragão.'),
    T('∀x (Ave(x) → Voa(x)) e Ave(tweety). Pelo silogismo, vale Voa(?) — digite o nome:', ['tweety'], 'Instancia o ∀ com tweety e aplica modus ponens.'),
    M('Em Prolog, "mortal(X) :- humano(X)." corresponde a:', ['∀x (Humano(x) → Mortal(x))', '∃x (Humano(x) ∧ Mortal(x))', '∀x (Humano(x) ∧ Mortal(x))', '¬Humano(x)'], 'Uma regra Prolog é um ∀ com condicional.'),
  ]),
]);

// ---------- Unidade 5
U('lg5', 'Modal e deôntica', 'necessário, possível, obrigatório, proibido', [
  Lic('Necessidade e possibilidade', [
    L('□ e ◇', 'A lógica modal acrescenta □P ("necessariamente P") e ◇P ("possivelmente P"). Elas se definem uma pela outra: é possível o que não é necessariamente falso.', '□P  P é necessário\n◇P  P é possível\n◇P ≡ ¬□¬P\n□P ≡ ¬◇¬P'),
    M('◇P equivale a:', ['¬□¬P', '□¬P', '¬□P', '□P'], 'Possível = não é necessário que seja falso.'),
    M('"É impossível que P" se escreve:', ['¬◇P', '◇¬P', '□P', '¬□P'], 'Impossível = não é possível. E ¬◇P ≡ □¬P.'),
    L('Mundos possíveis', 'Na semântica de Kripke há vários mundos ligados por uma relação de acessibilidade. □P vale num mundo se P vale em todos os mundos acessíveis. ◇P vale se P vale em algum.', 'mundo w → acessíveis: w1, w2\n□P em w: P em w1 e em w2\n◇P em w: P em w1 ou em w2'),
    M('◇P é verdadeiro num mundo quando:', ['P vale em algum mundo acessível', 'P vale em todos os mundos acessíveis', 'P vale só neste mundo', 'P é falso em todos'], '◇ = existe; □ = todos.'),
    M('□P é verdadeiro num mundo quando:', ['P vale em todos os mundos acessíveis', 'P vale em algum mundo acessível', 'P vale só neste mundo', 'P é falso em algum'], '□ = em todos os acessíveis.'),
  ]),
  Lic('Lógica deôntica', [
    L('Obrigação, permissão, proibição', 'A lógica deôntica (SDL) fala de normas. O(a) é "a é obrigatório". Permitido e proibido se definem a partir dele.', 'O(a)  obrigatório\nP(a)  permitido  ≡ ¬O(¬a)\nF(a)  proibido   ≡ O(¬a)'),
    M('"Proibido fumar" em termos de obrigação:', ['O(não fumar)', '¬O(fumar)', 'O(fumar)', 'P(fumar)'], 'Proibido a = obrigatório não-a.'),
    M('"Permitido a" equivale a:', ['¬O(¬a)', 'O(¬a)', 'O(a)', '¬O(a)'], 'Permitido = não é obrigatório não fazer.'),
    M('O axioma D diz O(a) → P(a). Ele afirma que:', ['o que é obrigatório é permitido', 'tudo é obrigatório', 'nada é proibido', 'o que é permitido é obrigatório'], 'Evita normas que obriguem algo proibido.'),
    M('Paradoxo de Ross: de O(enviar a carta) o SDL deriva O(enviar a carta ∨ queimá-la). Por que é estranho?', ['parece que queimar a carta cumpre a obrigação', 'a dedução é inválida', 'a carta some', 'não é estranho'], 'A disjunção é verdadeira se qualquer lado for: queimar "cumpriria" a norma.'),
    M('O que é um dilema normativo?', ['O(a) e O(¬a) ao mesmo tempo', 'uma permissão', 'um erro de sintaxe', 'uma tautologia'], 'Duas obrigações em conflito. O axioma D proíbe isso.'),
  ]),
]);

// ---------- Unidade 6
U('lg6', 'Lógica temporal', 'sempre, um dia, próximo, até', [
  Lic('Operadores temporais', [
    L('G, F, X e U', 'A lógica temporal fala de sequências de estados. G p: p vale sempre. F p: p vale em algum momento futuro. X p: p vale no próximo estado. p U q: p vale até q acontecer.', 'G p    sempre p\nF p    um dia p\nX p    no próximo passo, p\np U q  p até q'),
    M('"Em algum momento o semáforo ficará verde":', ['F verde', 'G verde', 'X verde', 'verde U vermelho'], 'F = eventualmente.'),
    M('"A porta nunca fica aberta e trancada ao mesmo tempo":', ['G ¬(aberta ∧ trancada)', 'F ¬(aberta ∧ trancada)', 'X (aberta ∧ trancada)', 'aberta U trancada'], 'Nunca = em todo instante, não.'),
    M('"pedido U resposta" pode ser lido como:', ['pedido vale até a resposta acontecer', 'pedido vale sempre', 'resposta vale sempre', 'pedido vale no próximo estado'], 'U = until.'),
    M('G p equivale a:', ['¬F ¬p', 'F p', '¬G p', 'X p'], 'Sempre p = nunca acontece ¬p.'),
    M('Uma propriedade de vivacidade ("algo bom acontece") usa tipicamente:', ['F', 'G ¬', 'X', 'nenhum operador'], 'Vivacidade pede que algo aconteça, cedo ou tarde.'),
  ]),
  Lic('Normas e tempo', [
    L('Obrigações com prazo', 'Combinando deôntica e temporal: "depois de multado, é obrigatório pagar".', 'G (multa → F pago)\n"sempre que há multa, um dia há pagamento"'),
    M('"Sempre que há pedido, a resposta vem depois":', ['G (pedido → F resposta)', 'F (pedido → G resposta)', 'pedido → resposta', 'X pedido'], 'G para todo instante e F para "depois".'),
    M('Em "se o aluguel atrasar, o inquilino deve pagar multa", o "deve" é:', ['deôntico', 'temporal', 'modal alético', 'proposicional'], 'Dever é norma: lógica deôntica.'),
    M('Em "sempre que atrasar, depois haverá multa", o "depois" é:', ['temporal', 'deôntico', 'quantificador', 'um conectivo'], 'Fala de tempo: F.'),
  ]),
]);

// ---------- Unidade 7 (Prolog)
U('lg7', 'Prolog: fatos e consultas', 'base de conhecimento e perguntas', [
  Lic('Fatos e consultas', [
    L('Programa = base de conhecimento', 'Em Prolog você descreve fatos e regras e depois faz perguntas. Cada cláusula termina com ponto. Nomes começam com letra minúscula; variáveis, com maiúscula.', 'gosta(maria, joao).\ngosta(joao, vinho).\ngosta(maria, vinho).', { rc: 'PROGRAMA' }),
    L('Consultas', 'Uma consulta pergunta se algo é verdade. Com variável, o Prolog procura todos os valores que servem, um por vez.', '?- gosta(maria, joao).\n?- gosta(maria, X).', { ro: 'RESPOSTAS', out: 'true.\n\nX = joao ;\nX = vinho.' }),
    M('Qual destes é uma variável em Prolog?', ['Quem', 'quem', "'quem'", 'quem()'], 'Variáveis começam com maiúscula ou _.', undefined, true),
    M('Qual fato está escrito corretamente?', ['pai(joao, maria).', 'Pai(joao, maria).', 'pai(joao, maria)', 'pai(Joao, maria).'], 'Nome em minúscula e ponto final.', undefined, true),
    M('Com gosta(maria, joao). e gosta(maria, vinho)., a consulta gosta(maria, X) devolve:', ['X = joao e depois X = vinho', 'só false', 'X = maria', 'erro'], 'Cada resposta é uma solução; ";" pede a próxima.'),
    M('Uma consulta sobre algo que não está na base devolve:', ['false', 'true', 'erro', 'null'], 'Mundo fechado: o que não se prova, é falso para o Prolog.'),
    T('Se a base tem 3 fatos gosta/2, quantas respostas dá ?- gosta(X, Y)? (número)', ['3'], 'Uma por fato.'),
  ]),
  Lic('Regras', [
    L('Regras com :-', 'Uma regra tem cabeça :- corpo, e se lê "a cabeça vale se o corpo valer". A vírgula significa "e"; o ponto e vírgula, "ou".', 'humano(socrates).\nmortal(X) :- humano(X).\n\n?- mortal(socrates).', { ro: 'RESPOSTA', out: 'true.' }),
    M('Em "avo(X,Z) :- pai(X,Y), pai(Y,Z)." a vírgula significa:', ['e', 'ou', 'então', 'não'], 'Conjunção: as duas condições têm de valer.', undefined, true),
    M('O símbolo :- lê-se:', ['"se"', '"e"', '"não"', '"atribui"'], 'cabeça :- corpo ≈ cabeça SE corpo.', undefined, true),
    F('Complete: todo gato é mamífero.', 'mamifero(X) :- ___(X).', ['gato', 'Gato', 'mamifero', 'X'], ['gato'], 'A regra diz: X é mamífero se X é gato.'),
    O('Monte um programa: fatos, regra, consulta.', ['pai(joao, maria).', 'pai(maria, ana).', 'avo(X, Z) :- pai(X, Y), pai(Y, Z).', '?- avo(joao, ana).'], 'Fatos primeiro, depois a regra, depois a pergunta.'),
    M('Com pai(joao,maria). pai(maria,ana). e avo(X,Z) :- pai(X,Y), pai(Y,Z)., a consulta avo(joao, Z) responde:', ['Z = ana', 'Z = maria', 'false', 'Z = joao'], 'joao é pai de maria, que é pai de ana.'),
  ]),
  Lic('Ciúmes e negação', [
    L('Variáveis compartilhadas', 'A mesma variável numa regra tem o mesmo valor em todo lugar. \\= exige que dois valores sejam diferentes.', 'gosta(maria, joao).\ngosta(ana, joao).\nciumento(X, Y) :-\n    gosta(X, Z), gosta(Y, Z), X \\= Y.\n\n?- ciumento(maria, Y).', { ro: 'RESPOSTA', out: 'Y = ana.' }),
    M('O que faz X \\= Y numa regra?', ['exige X e Y diferentes', 'atribui Y a X', 'soma X e Y', 'compara números'], 'Sem ele, cada pessoa seria ciumenta de si mesma.', undefined, true),
    L('Negação por falha: \\+', '\\+ meta é verdadeira quando o Prolog NÃO consegue provar a meta. É "não consegui provar", não "é falso no mundo".', 'solteiro(X) :- pessoa(X), \\+ casado(X).'),
    M('\\+ casado(joao) é verdadeiro quando:', ['o Prolog não consegue provar casado(joao)', 'joao é solteiro no mundo real', 'casado(joao) é um fato', 'joao não existe'], 'Negação por falha só olha a base de conhecimento.', undefined, true),
  ]),
]);

// ---------- Unidade 8
U('lg8', 'Prolog: listas e recursão', '[Cabeça|Cauda], contas e findall', [
  Lic('Listas', [
    L('[Cabeça|Cauda]', 'Uma lista é [] (vazia) ou uma cabeça seguida de uma cauda. Dá para separar as partes por unificação. _ ignora um valor.', '?- [1,2,3] = [H|T].\n\nmembro(X, [X|_]).\nmembro(X, [_|T]) :- membro(X, T).', { ro: 'RESPOSTA', out: 'H = 1,\nT = [2, 3].' }),
    M('[a,b,c] = [H|T] dá:', ['H = a, T = [b,c]', 'H = c, T = [a,b]', 'H = [a], T = b', 'false'], 'Cabeça é o primeiro; cauda é o resto.', undefined, true),
    M('Qual é a lista vazia?', ['[]', '()', '{}', 'nil'], 'Em Prolog: [].', undefined, true),
    M('length([a,b,c], N) dá:', ['N = 3', 'N = 2', 'N = [3]', 'false'], 'length conta os elementos.', undefined, true),
    M('?- append(X, Y, [1,2]) devolve quantas soluções?', ['3', '1', '2', '4'], 'Todas as divisões: []+[1,2], [1]+[2], [1,2]+[].'),
    T('Quanto vale S em sum_list([1,2,3,4], S)? (número)', ['10'], '1+2+3+4.'),
  ]),
  Lic('Recursão', [
    L('Caso base e passo', 'Para percorrer uma lista, escreva o caso base (lista vazia) e o passo (cabeça + cauda). "is" faz a conta.', 'tamanho([], 0).\ntamanho([_|T], N) :-\n    tamanho(T, M),\n    N is M + 1.'),
    M('Todo predicado recursivo precisa de:', ['um caso base', 'um corte', 'assert', 'findall'], 'Sem caso base a recursão não termina.'),
    M('"is" serve para:', ['calcular uma conta', 'comparar listas', 'declarar um fato', 'negar'], 'X is 2+3 calcula e guarda 5 em X. O = só unifica.', undefined, true),
    F('Complete o fatorial.', 'fatorial(0, 1).\nfatorial(N, F) :-\n    N > 0, M is N - 1,\n    fatorial(M, G),\n    F is N * ___.', ['G', 'M', 'F', 'N'], ['G'], 'G é o fatorial de N-1; multiplica por N.'),
    M('Sem o caso base, a recursão:', ['nunca termina (estoura)', 'termina com true', 'devolve false', 'é ignorada'], 'O Prolog fica chamando a regra sem parar.'),
    L('findall e corte', 'findall(X, meta, L) junta todas as soluções em uma lista. O corte ! diz ao Prolog: não volte atrás daqui.', 'findall(X, gosta(maria, X), L).', { ro: 'RESPOSTA', out: 'L = [joao, vinho].' }),
    M('findall(X, pai(joao, X), L) faz:', ['junta todas as soluções numa lista', 'devolve só a primeira', 'apaga fatos', 'conta linhas'], 'findall coleta todos os X que satisfazem a meta.', undefined, true),
  ]),
]);

// ---------- monta o curso
const course = {
  units: unidades.map((u) => ({
    id: u.id, title: u.title, description: u.description,
    lessons: u.lessons.map((l, li) => ({
      id: `${u.id}l${li}`, title: l.title,
      exercises: l.ex.map((e, ei) => {
        const base = { ...e, id: `${u.id}l${li}${e.k === 'learn' ? 'c' : 'e'}${ei}`, host: host() };
        if (base.e === undefined) base.e = '';
        return base;
      }),
    })),
  })),
};
writeFileSync(new URL('../src/content/logica.json', import.meta.url), JSON.stringify(course));

console.log(`unidades: ${course.units.length}, lições: ${course.units.reduce((a, u) => a + u.lessons.length, 0)}, exercícios: ${course.units.reduce((a, u) => a + u.lessons.reduce((b, l) => b + l.exercises.length, 0), 0)}`);
