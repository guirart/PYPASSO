import { Platform } from 'react-native';
import Purchases, { PACKAGE_TYPE, type PurchasesPackage } from 'react-native-purchases';
import type { Ciclo, Resultado } from './plus';

/**
 * Compras no Android (Google Play) e iPhone (App Store) via RevenueCat.
 * As lojas exigem o sistema de pagamento delas para liberar recursos dentro do app.
 *
 * Configuração (veja PAGAMENTOS.md):
 *   EXPO_PUBLIC_RC_ANDROID_KEY, EXPO_PUBLIC_RC_IOS_KEY  — chaves públicas do RevenueCat
 *   Entitlement "plus"; oferta padrão com os pacotes Mensal e Anual.
 * No Expo Go o SDK entra em modo de prévia (sem compras reais): use um development build.
 */
const KEY = Platform.select({ android: process.env.EXPO_PUBLIC_RC_ANDROID_KEY, ios: process.env.EXPO_PUBLIC_RC_IOS_KEY }) ?? '';
const ENTITLEMENT = 'plus';
let pronto: Promise<void> | null = null;

const iniciar = () => {
  if (!pronto) pronto = (async () => { Purchases.configure({ apiKey: KEY }); })();
  return pronto;
};

async function pacote(ciclo: Ciclo): Promise<PurchasesPackage | null> {
  await iniciar();
  const ofertas = await Purchases.getOfferings();
  const pkgs = ofertas.current?.availablePackages ?? [];
  return pkgs.find((p) => p.packageType === (ciclo === 'anual' ? PACKAGE_TYPE.ANNUAL : PACKAGE_TYPE.MONTHLY)) ?? null;
}

export const loja = {
  nome: Platform.OS === 'ios' ? 'App Store' : 'Google Play',
  configurada: () => !!KEY,

  async identificar(userId: string | null) {
    if (!KEY) return;
    await iniciar();
    if (userId) await Purchases.logIn(userId); // compras feitas sem conta passam para a conta
    else if (!(await Purchases.isAnonymous())) await Purchases.logOut();
  },

  async status() {
    await iniciar();
    const info = await Purchases.getCustomerInfo();
    const e = info.entitlements.active[ENTITLEMENT];
    if (!e) return { ativo: false };
    const id = e.productIdentifier.toLowerCase();
    return {
      ativo: true,
      ciclo: (/anual|annual|year/.test(id) ? 'anual' : 'mensal') as Ciclo,
      expiraEm: e.expirationDate ?? null,
      cancelada: !e.willRenew,
    };
  },

  async precos() {
    const out: Partial<Record<Ciclo, string>> = {};
    for (const c of ['mensal', 'anual'] as const) {
      const p = await pacote(c);
      if (p) out[c] = p.product.priceString;
    }
    return out;
  },

  async comprar(ciclo: Ciclo): Promise<Resultado> {
    try {
      const p = await pacote(ciclo);
      if (!p) return { ok: false, mensagem: 'Plano indisponível na loja agora. Tente mais tarde.' };
      const { customerInfo } = await Purchases.purchasePackage(p);
      return customerInfo.entitlements.active[ENTITLEMENT]
        ? { ok: true, mensagem: 'Bem-vindo ao Plus! Vidas ilimitadas liberadas.' }
        : { ok: false, mensagem: 'A compra não foi concluída.' };
    } catch (e) {
      const err = e as { userCancelled?: boolean; message?: string };
      if (err.userCancelled) return { ok: false };
      return { ok: false, mensagem: 'Não foi possível concluir a compra. Nada foi cobrado.' };
    }
  },

  async restaurar(): Promise<Resultado> {
    try { await iniciar(); await Purchases.restorePurchases(); return { ok: true }; }
    catch { return { ok: false, mensagem: 'Não foi possível falar com a loja agora.' }; }
  },

  async gerenciar(): Promise<Resultado> {
    try { await iniciar(); await Purchases.showManageSubscriptions(); return { ok: true }; }
    catch { return { ok: false, mensagem: `Abra a ${Platform.OS === 'ios' ? 'App Store' : 'Google Play'} > Assinaturas para gerenciar.` }; }
  },
};
