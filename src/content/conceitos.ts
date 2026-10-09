import raw from './conceitos.json';

/**
 * Cartão de "Novo conceito" -> entradas da Biblioteca que ele ensina
 * (gerado por tools/gerar_conceitos.py, na ordem das trilhas).
 */
const MAPA = raw as Record<string, string[]>;
export const conceitosDoCartao = (cardId: string) => MAPA[cardId] ?? [];
