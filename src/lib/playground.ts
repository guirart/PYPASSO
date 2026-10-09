import AsyncStorage from '@react-native-async-storage/async-storage';
import { create } from 'zustand';
import { createJSONStorage, persist } from 'zustand/middleware';

export const WELCOME = `# Bem-vindo ao terminal do PyPasso!
# Escreva Python à vontade e toque em Executar.
# As respostas dos input() vão na caixa "Entrada".

nome = input("Qual é o seu nome? ")
print(f"Olá, {nome}! Vamos programar.")

for i in range(1, 4):
    print("Contagem:", i)
`;

export const EXAMPLES: { title: string; files: Record<string, string>; stdin?: string }[] = [
  { title: 'Olá, mundo', files: { 'main.py': WELCOME }, stdin: 'Ana' },
  {
    title: 'Calculadora com input',
    stdin: '8\n3',
    files: {
      'main.py': `a = float(input("Primeiro número: "))
b = float(input("Segundo número: "))

print("Soma:", a + b)
print("Diferença:", a - b)
print("Produto:", a * b)
if b != 0:
    print("Divisão:", round(a / b, 2))
`,
    },
  },
  {
    title: 'Dois arquivos com import',
    files: {
      'main.py': `from matematica import fatorial, eh_primo

for n in range(1, 8):
    print(n, "! =", fatorial(n), "| primo?", eh_primo(n))
`,
      'matematica.py': `def fatorial(n):
    r = 1
    for i in range(2, n + 1):
        r *= i
    return r


def eh_primo(n):
    if n < 2:
        return False
    for d in range(2, int(n ** 0.5) + 1):
        if n % d == 0:
            return False
    return True
`,
    },
  },
  {
    title: 'Classe e objetos',
    files: {
      'main.py': `class ContaBancaria:
    def __init__(self, titular, saldo=0):
        self.titular = titular
        self.saldo = saldo

    def depositar(self, valor):
        self.saldo += valor

    def sacar(self, valor):
        if valor > self.saldo:
            raise ValueError("saldo insuficiente")
        self.saldo -= valor

    def __str__(self):
        return f"{self.titular}: R$ {self.saldo:.2f}"


conta = ContaBancaria("Bia", 100)
conta.depositar(50)
print(conta)

try:
    conta.sacar(500)
except ValueError as erro:
    print("Não deu:", erro)
`,
    },
  },
  {
    title: 'Jogo de adivinhar',
    stdin: '25\n12\n18\n21',
    files: {
      'main.py': `import random

random.seed(7)  # troque ou apague para mudar o número
segredo = random.randint(1, 50)
tentativas = 0

while True:
    palpite = int(input("Seu palpite (1 a 50): "))
    tentativas += 1
    if palpite < segredo:
        print("Mais alto!")
    elif palpite > segredo:
        print("Mais baixo!")
    else:
        print(f"Acertou em {tentativas} tentativas!")
        break
`,
    },
  },
];

type State = {
  files: Record<string, string>;
  order: string[];
  active: string;
  stdin: string;
  favs: string[]; // funções favoritas da Biblioteca
};
type Actions = {
  setCode: (name: string, code: string) => void;
  setActive: (name: string) => void;
  setStdin: (s: string) => void;
  addFile: (name: string) => string | null;
  removeFile: (name: string) => void;
  load: (files: Record<string, string>, stdin?: string) => void;
  /** Abre um exemplo da Biblioteca num arquivo próprio, sem apagar os outros. */
  openExample: (id: string, code: string, stdin?: string) => string;
  toggleFav: (id: string) => void;
};

/** Estado inicial (cada perfil do aparelho começa assim). */
export const initialPlayground = () => ({
  files: { 'main.py': WELCOME } as Record<string, string>,
  order: ['main.py'],
  active: 'main.py',
  stdin: 'Ana',
  favs: [] as string[],
});

export const usePlayground = create<State & Actions>()(
  persist(
    (set, get) => ({
      ...initialPlayground(),
      setCode: (name, code) => set((s) => ({ files: { ...s.files, [name]: code } })),
      setActive: (active) => set({ active }),
      setStdin: (stdin) => set({ stdin }),
      addFile: (raw) => {
        let name = raw.trim().replace(/\s+/g, '_');
        if (!name) return 'Dê um nome ao arquivo.';
        if (!name.endsWith('.py')) name += '.py';
        if (!/^[A-Za-z_][A-Za-z0-9_]*\.py$/.test(name)) return 'Use letras, números e _ (sem começar com número).';
        if (get().files[name] !== undefined) return 'Já existe um arquivo com esse nome.';
        set((s) => ({ files: { ...s.files, [name]: '' }, order: [...s.order, name], active: name }));
        return null;
      },
      removeFile: (name) => set((s) => {
        if (name === 'main.py') return s;
        const files = { ...s.files }; delete files[name];
        const order = s.order.filter((n) => n !== name);
        return { files, order, active: s.active === name ? 'main.py' : s.active };
      }),
      load: (files, stdin = '') => set({ files: { ...files }, order: Object.keys(files), active: 'main.py', stdin }),
      openExample: (id, code, stdin = '') => {
        const name = `exemplo_${id.replace(/[^A-Za-z0-9]+/g, '_').replace(/_+$/, '')}.py`;
        set((s) => ({
          files: { ...s.files, [name]: code + '\n' },
          order: s.order.includes(name) ? s.order : [...s.order, name],
          active: name,
          stdin: stdin || s.stdin,
        }));
        return name;
      },
      toggleFav: (id) => set((s) => ({ favs: s.favs.includes(id) ? s.favs.filter((x) => x !== id) : [...s.favs, id] })),
    }),
    { name: 'pypasso-playground', storage: createJSONStorage(() => AsyncStorage) },
  ),
);
