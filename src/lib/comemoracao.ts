import type { Pose } from '@/components/pipo-poses';

/** Como o Pipo comemora o fim da lição: visual, título e uma frase engraçada (sorteada). */
export type Comemoracao = { pose: Pose; titulo: string; frase: string; confete: boolean };

const sortear = <T,>(xs: T[]) => xs[Math.floor(Math.random() * xs.length)];

const PERFEITO = [
  '0 erros. Tive que pôr os óculos escuros: você tá brilhando demais.',
  'Nenhum bug. O compilador ficou até sem graça.',
  'Código tão limpo que o PEP 8 mandou um abraço.',
  'Já pode pôr "Python" no LinkedIn com estrelinha.',
  "print('lenda')  # saída: você",
  'Zero erros? Vou contar pros outros Pipos.',
];
const PERFEITO_RAPIDO = [
  'Perfeito E rápido. Isso não é lição, é demo de palestra.',
  '0 erros em tempo recorde. Os óculos são pra esconder minha emoção.',
];
const RAPIDO = [
  'Rápido assim, nem deu tempo de eu piscar.',
  'Isso foi O(1): instantâneo.',
  'Você responde mais rápido que o Python roda um print.',
];
const QUASE = (n: number) => [
  n === 1 ? '1 errinho? Isso não é bug, é feature.' : `${n} errinhos e todos corrigidos. Isso é debugar com estilo!`,
  'Errar pouco é humano. Errar zero é Pipo... mas tá quase!',
  'Os erros voltaram no fim e você venceu todos. Festa!',
];
const SUADO = [
  'Foi suado, mas foi! Todo programador já brigou com o próprio código.',
  'Isso foi um while True de persistência. E deu break no final!',
  'Cada erro de hoje é um bug a menos amanhã.',
  'Até o Python já foi versão 0.9. Bora pra próxima!',
  'Errou, voltou, acertou. Isso tem nome: aprender.',
];

export function escolherComemoracao(o: { erros: number; segundos: number; exercicios: number; pratica?: boolean }): Comemoracao {
  if (o.pratica) return { pose: 'festa', titulo: 'VIDA DE VOLTA', frase: 'Treino pago: uma vida voltou pro seu bolso.', confete: true };
  const rapido = o.segundos <= Math.max(25, o.exercicios * 7);
  if (o.erros === 0) {
    return { pose: 'oculos', titulo: sortear(['MR. PERFEITO', 'ZERO BUGS', 'NÍVEL SÊNIOR']), frase: sortear(rapido ? PERFEITO_RAPIDO : PERFEITO), confete: true };
  }
  if (o.erros <= 2 && rapido) return { pose: 'raio', titulo: sortear(['SPEEDRUN!', 'MODO TURBO']), frase: sortear(RAPIDO), confete: false };
  if (o.erros <= 2) return { pose: 'festa', titulo: sortear(['QUASE PERFEITO', 'MANDOU BEM']), frase: sortear(QUASE(o.erros)), confete: true };
  return { pose: 'suor', titulo: sortear(['NA RAÇA', 'PERSISTÊNCIA 100%']), frase: sortear(SUADO), confete: false };
}
