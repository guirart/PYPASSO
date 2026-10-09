/** Na web não dá para agendar avisos com o site fechado: os lembretes ficam para o app do celular. */
export const LEMBRETES_SUPORTADOS = false;
export async function pedirPermissao() { return false; }
export async function agendarLembretes() {}
export async function testarLembrete() { return false; }
