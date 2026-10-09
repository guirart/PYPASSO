import { Tabs } from 'expo-router';
import { Icone } from '@/components/Icone';
import { Book, CodeIcon, Path_, Person, Trophy } from '@/components/Icons';
import { useGame } from '@/lib/store';
import { useTheme } from '@/lib/theme';

export default function TabsLayout() {
  const t = useTheme();
  // Contador de conceitos novos (aprendidos nas lições e ainda não abertos na Biblioteca).
  const novos = useGame((s) => Object.keys(s.aprendidos ?? {}).filter((id) => !s.vistosBib?.[id]).length);
  // Peças novas no Inventário (drops de chefe que a pessoa ainda não viu).
  const pecasNovas = useGame((s) => (s.inv ?? []).filter((i) => i.novo).length);
  return (
    <Tabs screenOptions={{
      headerShown: false,
      tabBarActiveTintColor: t.brand,
      tabBarInactiveTintColor: t.muted,
      tabBarStyle: { backgroundColor: t.bg, borderTopColor: t.line, borderTopWidth: 2 },
      tabBarLabelStyle: { fontWeight: '800', fontSize: 10 },
    }}>
      <Tabs.Screen name="index" options={{ title: 'Aprender', tabBarIcon: ({ color }) => <Path_ color={String(color)} size={24} /> }} />
      <Tabs.Screen name="codigo" options={{ title: 'Código', tabBarIcon: ({ color }) => <CodeIcon color={String(color)} size={24} /> }} />
      <Tabs.Screen name="biblioteca" options={{ title: 'Biblioteca', tabBarBadge: novos || undefined, tabBarBadgeStyle: { backgroundColor: t.sun, color: t.sunInk, fontWeight: '900' }, tabBarIcon: ({ color }) => <Book color={String(color)} size={24} /> }} />
      <Tabs.Screen name="inventario" options={{ title: 'Inventário', tabBarBadge: pecasNovas || undefined, tabBarBadgeStyle: { backgroundColor: t.sun, color: t.sunInk, fontWeight: '900' }, tabBarIcon: ({ color }) => <Icone nome="espada" size={24} color={String(color)} /> }} />
      <Tabs.Screen name="ranking" options={{ title: 'Liga', tabBarIcon: ({ color }) => <Trophy color={String(color)} size={24} /> }} />
      <Tabs.Screen name="perfil" options={{ title: 'Perfil', tabBarIcon: ({ color }) => <Person color={String(color)} size={24} /> }} />
    </Tabs>
  );
}
